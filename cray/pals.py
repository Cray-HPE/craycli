"""
pals.py - Common functions for launching applications with PALS
Copyright 2020 Cray Inc. All Rights Reserved.
"""
import base64
import errno
import fcntl
import json
import signal
import socket
import ssl
import stat
import sys
import threading
import time
import os
import uuid

import click
import websocket
from six.moves import urllib

from cray.echo import echo, LOG_INFO, LOG_WARN, LOG_DEBUG, LOG_RAW
from cray.rest import request
from cray.utils import get_hostname, open_atomic

from cray import atp

SIGNAL_RECEIVED = 0  # Last signal number received
PING_INTERVAL = 20  # WebSocket ping interval


def split_mpmd_args(args):
    """ Split a list of arguments by the MPMD separator : """
    cmdargs = []
    cmdidx = 0
    for idx, arg in enumerate(args):
        if arg == ":":
            cmdargs.append(args[cmdidx:idx])
            cmdidx = idx + 1
    cmdargs.append(args[cmdidx:])

    return cmdargs


def make_ws_url(route, url=None):
    """ Make a websocket URL (using wss scheme). Based on make_url in rest.py """
    # If no URL given, use the configured hostname
    if not url:
        url = get_hostname()

    # Split into components
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)

    # Override scheme with secure WebSocket protocol
    scheme = "wss"

    # If URL didn't start with a scheme, set netloc to the first part of the path
    if not netloc and path:
        netloc, _, path = path.partition("/")

    # Append route to path
    path = urllib.parse.urljoin(path, route)

    # Join everything back together
    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))


def get_ws_headers():
    """ Get a list of HTTP headers to send in WebSocket request """
    ctx = click.get_current_context()
    auth = ctx.obj["auth"]

    # If we have an access token in the session, use it
    if auth and auth.session and auth.session.access_token:
        return ["Authorization: Bearer " + auth.session.access_token]

    return []


def find_executable(executable):
    """ Get a path to an executable file """
    # Use given file if it contains a slash or no PATH set
    if "/" in executable or "PATH" not in os.environ:
        return executable

    # Split PATH and search for an executable with the right name
    for dirname in os.environ["PATH"].split(os.pathsep):
        exefile = os.path.join(dirname, executable)
        if os.path.isfile(exefile) and os.access(exefile, os.X_OK):
            return exefile

    # Couldn't find one
    return None


def signal_handler(signum, _):
    # pylint: disable=global-statement
    """ Signal handler that stores the signal value in a global """
    global SIGNAL_RECEIVED
    SIGNAL_RECEIVED = signum


def setup_signals():
    # pylint: disable=bad-continuation
    """ Set up signal handlers and return a signal wakeup read fd """
    # Create a pipe that we can use to determine when we've got a signal
    sig_read, sig_write = os.pipe()

    # Make the write end non-blocking (required for set_wakeup_fd)
    flags = fcntl.fcntl(sig_write, fcntl.F_GETFL)
    fcntl.fcntl(sig_write, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    signal.set_wakeup_fd(sig_write)

    # Set up signal handlers
    for signum in [
        signal.SIGHUP,
        signal.SIGINT,
        signal.SIGQUIT,
        signal.SIGABRT,
        signal.SIGALRM,
        signal.SIGTERM,
        signal.SIGUSR1,
        signal.SIGUSR2,
    ]:
        signal.signal(signum, signal_handler)

    return sig_read


def get_rpc(method, rpcid=None, **params):
    """ Create a JSONRPC request """
    rpc = {"jsonrpc": "2.0", "method": method}
    if params:
        rpc["params"] = params
    if rpcid:
        rpc["id"] = rpcid
    return json.dumps(rpc)


def send_rpc(websock, method, reqid=None, **params):
    """ Send an RPC over the socket """
    req = get_rpc(method, reqid, **params)
    echo("Sending RPC %s" % req, level=LOG_RAW)
    websock.send(req)


def forward_stdin(websock, stdin=sys.stdin):
    """ Read stdin content and write to application """
    while True:
        # Wait for content on stdin
        content = os.read(stdin.fileno(), 4096)
        if not content:
            # Empty read signifies EOF
            send_rpc(websock, "stdin", eof=True)
            break

        # Attempt to decode UTF-8
        try:
            encoding = "UTF-8"
            decoded = content.decode("utf-8")
        except UnicodeError:
            # Fall back on base64
            encoding = "base64"
            decoded = base64.b64encode(content).decode("utf-8")

        # Send content over socket
        send_rpc(websock, "stdin", content=decoded, encoding=encoding)


def forward_signals(websock, sig_pipe):
    """ Forward signals to the application """
    while True:
        # Block until a signal arrives
        os.read(sig_pipe, 4096)

        # Send it to the app
        send_rpc(websock, "signal", str(uuid.uuid4()), signum=SIGNAL_RECEIVED)


def send_pings(websock):
    """ Avoid connection drops by sending periodic pings """
    while True:
        time.sleep(PING_INTERVAL)
        echo("Sending keepalive ping", level=LOG_RAW)
        websock.ping()


def spawn_threads(websock):
    """ Spawn threads to handle stdin, signals, and pings """
    stdin_thread = threading.Thread(target=forward_stdin, args=(websock,))
    stdin_thread.daemon = True
    stdin_thread.start()

    sig_read = setup_signals()
    signal_thread = threading.Thread(target=forward_signals, args=(websock, sig_read))
    signal_thread.daemon = True
    signal_thread.start()

    ping_thread = threading.Thread(target=send_pings, args=(websock,))
    ping_thread.daemon = True
    ping_thread.start()


def get_exit_code(status):
    """ Translate an exit status (as returned by wait) into an exit code """
    if os.WIFEXITED(status):
        return os.WEXITSTATUS(status)
    if os.WIFSIGNALED(status):
        return 128 + os.WTERMSIG(status)
    return 255


def print_output(params, a_file, label):
    """ Print output from a stdout/stderr RPC to the given file """
    content = params.get("content")
    if not content:
        return

    encoding = params.get("encoding")
    if encoding == "base64":
        # Decode and output base64 content
        click.echo(base64.b64decode(content), nl=False, file=a_file)
    elif label and "host" in params and "rankid" in params:
        # Label each line if requested and host/rank available
        host = params["host"]
        rankid = int(params["rankid"])
        for line in content.splitlines():
            click.echo("%s %d: %s" % (host, rankid, line), file=a_file)
    else:
        # Otherwise, print without processing
        click.echo(content, nl=False, file=a_file)


def log_rank_exit(rankid, host, status):
    """ Log a rank exit """
    if rankid == -1:
        rank = "shepherd"
    else:
        rank = "rank %d" % rankid

    extra = ""
    level = LOG_INFO
    if os.WIFEXITED(status):
        action = "exited with code"
        code = os.WEXITSTATUS(status)
        if code == 0:
            level = LOG_RAW
    elif os.WIFSIGNALED(status):
        action = "died from signal"
        code = os.WTERMSIG(status)
        if os.WCOREDUMP(status):
            extra = " and dumped core"
    else:
        action = "invalid status"
        code = status

    echo("%s: %s %s %d%s" % (host, rank, action, code, extra), level=level)


def write_procinfo_file(result, procinfo_file):
    """ Dump the procinfo result to the given file """
    try:
        with open_atomic(procinfo_file) as procinfo_fp:
            json.dump(result, procinfo_fp)
    except (IOError, OSError) as err:
        echo("Couldn't write %s: %s" % (procinfo_file, str(err)), level=LOG_WARN)


def get_executables(req, transfer):
    """ Get the set of local paths to binaries """
    executables = set()
    for cmd in req["cmds"]:
        executable = find_executable(cmd["argv"][0])
        if executable:
            executables.add(executable)
            if transfer:
                cmd["argv"][0] = os.path.basename(executable)

    return executables


class PALSApp(object):
    """ Class representing a running PALS application """

    def __init__(self):
        """ Initialize this application """
        self.apid = ""
        self.exit_codes = set()
        self.stream_rpcid = str(uuid.uuid4())
        self.start_rpcid = str(uuid.uuid4())
        self.procinfo_rpcid = str(uuid.uuid4())
        self.complete = False

    def launch(self, launchreq, transfer=False, label=False, procinfo_file=None):
        """ Launch this application, transfer binaries, and run """
        executables = get_executables(launchreq, transfer)

        # Launch ATP frontend if enabled
        # returns list of environment variables to set for job
        (atp_frontend_handle, atp_envlist) = atp.launch_atp_frontend(executables)
        if atp_envlist:
            launchreq["environment"] += atp_envlist

        try:
            # Send launch request
            resp = request("POST", "apis/pals/v1/apps", json=launchreq)
            self.apid = resp.json().get("apid")
            echo("Launched application %s" % self.apid, level=LOG_INFO)

            # Send newly-launched apid to ATP frontend to monitor
            if atp_frontend_handle:
                atp.send_launched_apid(atp_frontend_handle, self.apid)

            # Transfer executables
            if transfer:
                for executable in executables:
                    self.transfer(executable)

            return self.run(label, procinfo_file)
        finally:
            # Terminate frontend on error and rethrow exception
            if atp_frontend_handle:
                atp.terminate_frontend(atp_frontend_handle)

    def transfer(self, executable):
        """ Transfer a file to application compute nodes """
        try:
            mode = stat.S_IMODE(os.stat(executable).st_mode)
            params = {"mode": "0%o" % mode, "name": os.path.basename(executable)}
            headers = {"Content-Type": "application/octet-stream"}
            with open(executable, "rb") as a_execfile:
                resp = request(
                    "POST",
                    "apis/pals/v1/apps/%s/files" % self.apid,
                    params=params,
                    headers=headers,
                    data=a_execfile,
                )
                path = resp.json().get("path")
                echo("Transferred executable to %s" % path, level=LOG_DEBUG)
        except (OSError, IOError) as err:
            raise click.ClickException("Couldn't transfer binary: %s" % str(err))

    def handle_rpc(self, websock, rpc, label=False, procinfo_file=None):
        """ Handle a received RPC. Return True if complete. """
        # Parse the RPC
        method = rpc.get("method")
        params = rpc.get("params", {})
        errmsg = rpc.get("error", {}).get("message")
        rpcid = rpc.get("id")
        result = rpc.get("result")

        # Handle stdout notification
        if method == "stdout":
            print_output(params, sys.stdout, label)

        # Handle stderr notification
        elif method == "stderr":
            print_output(params, sys.stderr, label)

        # Handle exit notification
        elif method == "exit":
            rankid = int(params.get("rankid", -1))
            host = params.get("host", "unknown")
            status = int(params.get("status", 0))
            self.exit_codes.add(get_exit_code(status))
            log_rank_exit(rankid, host, status)

        # Handle complete notification
        elif method == "complete":
            self.complete = True

        # Handle unknown RPC method
        elif method:
            echo("Received unknown %s RPC" % method, level=LOG_WARN)

        # Handle error responses
        elif errmsg:
            raise click.ClickException(errmsg)

        # Handle stream response
        elif rpcid == self.stream_rpcid:
            send_rpc(websock, "start", self.start_rpcid)

        # Handle start response
        elif rpcid == self.start_rpcid:
            if procinfo_file:
                # Add delay before procinfo if requested
                # This is needed until the startup barrier works correctly
                if "PALS_PROCINFO_DELAY" in os.environ:
                    time.sleep(float(os.environ["PALS_PROCINFO_DELAY"]))
                send_rpc(websock, "procinfo", self.procinfo_rpcid)

        # Handle procinfo response
        elif rpcid == self.procinfo_rpcid and procinfo_file:
            write_procinfo_file(result, procinfo_file)

    def run(self, label=False, procinfo_file=None):
        """ Run this application """

        # Connect the websocket
        url = make_ws_url("apis/pals/v1/apps/%s/stdio" % self.apid)
        headers = get_ws_headers()
        # TODO: enable SSL verification
        sslopt = {"cert_reqs": ssl.CERT_NONE}
        echo("Connecting to %s" % url, level=LOG_DEBUG)
        websock = websocket.create_connection(
            url, header=headers, sslopt=sslopt, enable_multithread=True
        )

        # Spawn threads to handle signals, stdin, and pings
        spawn_threads(websock)

        # First send the stream RPC to start things off
        send_rpc(websock, "stream", self.stream_rpcid)

        while not self.complete:
            try:
                # Read an RPC off the socket
                rpc = json.loads(websock.recv())
                echo("Received RPC %s" % rpc, level=LOG_RAW)

                # Handle the RPC
                self.handle_rpc(websock, rpc, label, procinfo_file)

            except websocket.WebSocketException as err:
                raise click.ClickException(
                    "Error reading from application: %s" % str(err)
                )
            except ValueError as err:
                raise click.ClickException(
                    "Error decoding application message: %s" % str(err)
                )
            except socket.error as err:
                if err.errno != errno.EINTR:
                    raise click.ClickException("Connection error: %s" % str(err))

        # Clean up after ourselves
        websock.close()

        return self.exit_codes
