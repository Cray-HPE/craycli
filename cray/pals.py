#
#  MIT License
#
#  (C) Copyright 2020-2023 Hewlett Packard Enterprise Development LP
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.
#
""" pals.py - Common functions for launching applications with PALS. """
# pylint: disable=fixme
import base64
import errno
import fcntl
import json
import os
import resource
import signal
import socket
import ssl
import stat
import sys
import threading
import time
import uuid
import websocket
import click
from six.moves import urllib

from cray import atp
from cray import mpir
from cray.echo import echo
from cray.echo import LOG_DEBUG
from cray.echo import LOG_INFO
from cray.echo import LOG_RAW
from cray.echo import LOG_WARN
from cray.errors import BadResponseError
from cray.rest import request
from cray.utils import get_hostname
from cray.utils import open_atomic

SIGNAL_RECEIVED = 0  # Last signal number received
PING_INTERVAL = 20  # WebSocket ping interval
MPIR_ATTACH_INTERVAL = 1  # Check for MPIR attach variable


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


def make_ws_url(route: str, url: str = '') -> urllib.parse.ParseResult:
    """ Make a websocket URL (using wss scheme). Based on make_url in rest.py """
    # If no URL given, use the configured hostname
    if not url:
        url = get_hostname()

    # If no protocol/scheme is set, urllib will confuse anything before the
    # port number as the scheme, and set the path to the port. To prevent
    # this ensure that `//` is at the beginning of the string if none is
    # set, this way urllib can work without us paying concession to a
    # protocol (e.g. // is agnostic to http|https|etc).
    if '//' not in url:
        url = f'//{url}'

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


def get_ws_headers() -> list:
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


def parse_hostfile(hostfile):
    """ Parse a host list from a host file """
    hostlist = []
    for line in hostfile:
        # Ignore leading/trailing whitespace
        line = line.strip()

        # Ignore empty lines, and lines that start with #
        if line and line[0] != "#":
            hostlist.append(line)

    return hostlist


def signal_handler(signum, *_):
    # pylint: disable=global-statement
    """ Signal handler that stores the signal value in a global """
    global SIGNAL_RECEIVED
    SIGNAL_RECEIVED = signum


def setup_signals():
    # pylint: disable=c-extension-no-member
    """ Set up signal handlers and return a signal wakeup read fd """
    # Create a pipe that we can use to determine when we've got a signal
    sig_read, sig_write = os.pipe()

    # Make the write end non-blocking (required for set_wakeup_fd)
    flags = fcntl.fcntl(sig_write, fcntl.F_GETFL)
    fcntl.fcntl(sig_write, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    signal.set_wakeup_fd(sig_write)

    # Set up signal handlers
    for signum in [signal.SIGHUP, signal.SIGINT, signal.SIGQUIT,
                   signal.SIGABRT, signal.SIGALRM, signal.SIGTERM,
                   signal.SIGUSR1,
                   signal.SIGUSR2, ]:
        signal.signal(signum, signal_handler)

    # Ignore SIGTTIN so we don't stop in the background
    signal.signal(signal.SIGTTIN, signal.SIG_IGN)

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
    echo(f"Sending RPC {req}", level=LOG_RAW)
    websock.send(req)


def forward_stdin(websock, stdin=sys.stdin):
    """ Read stdin content and write to application """
    try:
        while True:
            try:
                # Wait for content on stdin
                content = os.read(stdin.fileno(), 4096)

                # Empty read signifies EOF
                if not content:
                    send_rpc(websock, "stdin", eof=True)
                    break

                # Attempt to decode UTF-8
                content = content.decode("utf-8")
                send_rpc(websock, "stdin", content=content, encoding="UTF-8")
            except OSError:
                # I/O error, send EOF
                send_rpc(websock, "stdin", eof=True)
                break
            except UnicodeError:
                # Fall back on base64
                content = base64.b64encode(content).decode("utf-8")
                send_rpc(websock, "stdin", content=content, encoding="base64")
    except websocket.WebSocketException:
        pass


def forward_signals(websock, sig_pipe):
    """ Forward signals to the application """
    try:
        while True:
            # Block until a signal arrives
            os.read(sig_pipe, 4096)

            # Send it to the app
            send_rpc(
                websock, "signal", str(uuid.uuid4()), signum=SIGNAL_RECEIVED
            )
    except (OSError, websocket.WebSocketException):
        pass


def send_pings(websock):
    """ Avoid connection drops by sending periodic pings """
    try:
        while True:
            time.sleep(PING_INTERVAL)
            echo("Sending keepalive ping", level=LOG_RAW)
            websock.ping()
    except websocket.WebSocketException:
        pass


def spawn_threads(websock):
    """ Spawn threads to handle stdin, signals, and pings """
    sig_read = setup_signals()

    stdin_thread = threading.Thread(target=forward_stdin, args=(websock,))
    stdin_thread.daemon = True
    stdin_thread.start()

    signal_thread = threading.Thread(
        target=forward_signals, args=(websock, sig_read)
    )
    signal_thread.daemon = True
    signal_thread.start()

    ping_thread = threading.Thread(target=send_pings, args=(websock,))
    ping_thread.daemon = True
    ping_thread.start()


def monitor_mpir(ctx, apid):
    """ Wait on MPIR variable to fill in proctable """
    while True:
        # Look for MPIR debug flag
        if mpir.get_MPIR_being_debugged():
            # If proctable is not already filled, use procinfo to fill
            if not mpir.MPIR_proctable_filled():
                # Make request to procinfo endpoint
                with ctx:
                    resp = request(
                        "GET", "apis/pals/v1/apps/" + apid + "/procinfo"
                    )
                procinfo = resp.json()
                # Extract MPIR information
                proctable_elems = []
                for rank in range(len(procinfo["cmdidxs"])):
                    hostname = procinfo["nodes"][procinfo["placement"][rank]]
                    executable = procinfo["executables"][
                        procinfo["cmdidxs"][rank]]
                    pid = procinfo["pids"][rank]
                    proctable_elems.append((hostname, executable, pid))
                # Call C library to set C MPIR variables
                mpir.fill_MPIR_proctable(proctable_elems)
                mpir.call_MPIR_Breakpoint()
                # Now that MPIR proctable is set, exit the monitoring thread
                return
        time.sleep(MPIR_ATTACH_INTERVAL)


def spawn_mpir_thread(ctx, apid):
    """ Create MPIR watcher thread """
    mpir_thread = threading.Thread(target=monitor_mpir, args=(ctx, apid))
    mpir_thread.daemon = True
    mpir_thread.start()


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
            click.echo(f"{host} {rankid:d}: {line}", file=a_file)
    else:
        # Otherwise, print without processing
        click.echo(content, nl=False, file=a_file)


def log_rank_exit(rankid, host, status):
    """ Log a rank exit """
    if rankid == -1:
        rank = "shepherd"
    else:
        rank = f"rank {rankid:d}"

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

    echo(f"{host}: {rank} {action} {code:d}{extra}", level=level)


def write_procinfo_file(result, procinfo_file):
    """ Dump the procinfo result to the given file """
    try:
        with open_atomic(procinfo_file) as procinfo_fp:
            json.dump(result, procinfo_fp)
    except (IOError, OSError) as err:
        echo(
            f"Couldn't write {procinfo_file}: {str(err)}", level=LOG_WARN
        )


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


def get_resource_limits(limitnames):
    # pylint: disable=c-extension-no-member
    """ Given a list of resource names, fetch and format their limits """
    limits = {}
    for limitname in limitnames:
        try:
            limit = getattr(resource, "RLIMIT_" + limitname)
            soft, hard = resource.getrlimit(limit)
            limits[limitname] = f"{soft:d} {hard:d}"
        except (AttributeError, resource.error):
            pass

    return limits


def connect_websock(apid):
    # pylint: disable=no-member
    """ Connect to the application websocket """
    try:
        url = make_ws_url(f"apis/pals/v1/apps/{apid}/stdio")
        headers = get_ws_headers()
        # TODO: enable SSL verification
        sslopt = {"cert_reqs": ssl.CERT_NONE}
        echo(f"Connecting to {url}", level=LOG_DEBUG)
        return websocket.create_connection(
            url, header=headers, sslopt=sslopt, enable_multithread=True
        )
    except (websocket.WebSocketException, socket.error) as err:
        raise click.ClickException(f"Connection error: {str(err)}")


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
        self.started = False

    def launch(
            self, launchreq, transfer=False, label=False, procinfo_file=None
    ):
        """ Launch this application, transfer binaries, and run """
        executables = get_executables(launchreq, transfer)

        # Launch ATP frontend if enabled
        # returns list of environment variables to set for job
        (atp_frontend_handle, atp_envlist) = atp.launch_atp_frontend(
            executables
        )
        if atp_envlist:
            launchreq["environment"] += atp_envlist

        # Set custom fanout if requested
        if "PALS_FANOUT" in os.environ:
            launchreq["fanout"] = int(os.environ["PALS_FANOUT"])

        # Set RPC timeout if requested
        if "PALS_RPC_TIMEOUT" in os.environ:
            launchreq["rpc_timeout"] = int(os.environ["PALS_RPC_TIMEOUT"])

        try:
            # Send launch request
            resp = request("POST", "apis/pals/v1/apps", json=launchreq)
            self.apid = resp.json().get("apid")
            mpir.set_current_apid(self.apid)
            echo(f"Launched application {self.apid}", level=LOG_INFO)

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

            # Delete application from the PALS database
            if self.apid:
                try:
                    request("DELETE", "apis/pals/v1/apps/" + self.apid)
                except BadResponseError:
                    # Ignore 404 errors
                    pass

    def transfer(self, executable):
        """ Transfer a file to application compute nodes """
        try:
            mode: int = stat.S_IMODE(os.stat(executable).st_mode)
            params = {
                "mode": f"0{mode:o}", "name": os.path.basename(executable)
            }
            headers = {"Content-Type": "application/octet-stream"}
            with open(executable, "rb") as a_execfile:
                resp = request(
                    "POST",
                    f"apis/pals/v1/apps/{self.apid}/files",
                    params=params,
                    headers=headers,
                    data=a_execfile, )
                path = resp.json().get("path")
                echo(f"Transferred executable to {path}", level=LOG_DEBUG)
        except (OSError, IOError) as err:
            raise click.ClickException(
                f"Couldn't transfer binary: {str(err)}"
            )

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
            echo(f"Received unknown {method} RPC", level=LOG_WARN)

        # Handle error responses
        elif errmsg:
            raise click.ClickException(errmsg)

        # Handle stream response
        elif rpcid == self.stream_rpcid:
            if not self.started:
                send_rpc(websock, "start", self.start_rpcid)

        # Handle start response
        elif rpcid == self.start_rpcid:
            self.started = True
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

        connected = False
        spawn_mpir_thread(click.get_current_context(), self.apid)

        while not self.complete:
            try:
                if not connected:
                    # Connect to stdio websocket endpoint
                    websock = connect_websock(self.apid)
                    connected = True

                    # Spawn threads to handle signals, stdin, and pings
                    spawn_threads(websock)

                    # Send the stream RPC to start things off
                    send_rpc(websock, "stream", self.stream_rpcid)

                # Read an RPC off the socket
                rpc = json.loads(websock.recv())
                echo(f"Received RPC {rpc}", level=LOG_RAW)

                # Handle the RPC
                self.handle_rpc(websock, rpc, label, procinfo_file)

            except websocket.WebSocketException as err:
                echo(
                    f"Lost application connection ({str(err)}), reconnecting",
                    level=LOG_WARN, )
                websock.close()
                connected = False
            except socket.error as err:  # pylint: disable=no-member
                if err.errno != errno.EINTR:
                    echo(
                        f"Lost application connection ({str(err)}), reconnecting",
                        level=LOG_WARN, )
                    websock.close()
                    connected = False
            except ValueError as err:
                echo(
                    f"Error decoding application message: {str(err)}",
                    level=LOG_WARN
                )

        # Clean up after ourselves
        websock.close()
        mpir.free_MPIR_proctable()

        return self.exit_codes
