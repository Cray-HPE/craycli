# MIT License
#
# (C) Copyright [2020-2022] Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
"""
test_pals.py - Unit tests for the pals module
"""

import io
import json
import os
import resource
import signal
import tempfile

import click
import pytest

from cray import pals
from ..utils.utils import compare_dicts


def test_signals():
    # pylint: disable=comparison-with-callable
    """ Test signal handling setup """
    pals.signal_handler(signal.SIGTERM, None)
    assert pals.SIGNAL_RECEIVED == signal.SIGTERM

    assert pals.setup_signals() >= 0
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
        assert signal.getsignal(signum) == pals.signal_handler


def test_make_ws_url():
    """ Test making a websocket URL from an API gateway URL """
    wsurl = pals.make_ws_url("test", "https://api-gw-service-nmn.local:30443")
    assert wsurl == "wss://api-gw-service-nmn.local:30443/test"

    wsurl = pals.make_ws_url("test", "api-gw-service-nmn.local:30443")
    assert wsurl == "wss://api-gw-service-nmn.local:30443/test"


def test_get_rpc():
    """ Test JSON-RPC request creation """
    rpc = json.loads(pals.get_rpc("test"))
    expected = {"jsonrpc": "2.0", "method": "test"}
    compare_dicts(expected, rpc)
    rpc = json.loads(pals.get_rpc("test", foo="bar"))
    expected = {"jsonrpc": "2.0", "method": "test", "params": {"foo": "bar"}}
    compare_dicts(expected, rpc)
    rpc = json.loads(pals.get_rpc("test", "1234"))
    expected = {"jsonrpc": "2.0", "method": "test", "id": "1234"}
    compare_dicts(expected, rpc)


class MockSocket(object):
    """ Mock socket class that receives canned content """

    def __init__(self, recv_queue=None):
        self.recv_queue = recv_queue
        self.send_queue = []

    def recv(self):
        """ Receive a message from the socket """
        if self.recv_queue:
            return self.recv_queue.pop(0)
        return b""

    def send(self, msg):
        """ Send a message to the socket """
        self.send_queue.append(msg)


def test_send_rpc():
    """ Test RPC sending """
    sock = MockSocket()

    pals.send_rpc(sock, "start")
    pals.send_rpc(sock, "stream", "myrpc", foo="bar")

    start = {"jsonrpc": "2.0", "method": "start"}
    stream = {
        "jsonrpc": "2.0",
        "method": "stream",
        "params": {"foo": "bar"},
        "id": "myrpc",
    }
    compare_dicts(start, json.loads(sock.send_queue[0]))
    compare_dicts(stream, json.loads(sock.send_queue[1]))


def test_get_exit_code():
    """ Test exit status to exit code translation """
    # Test out extremes for exit status
    assert pals.get_exit_code(0x0000) == 0
    assert pals.get_exit_code(0xFF00) == 255

    # Test out extremes for termination signals
    assert pals.get_exit_code(0x0001) == 129
    assert pals.get_exit_code(0x007F) == 255

    # Core dump shouldn't affect exit code
    assert pals.get_exit_code(0x0081) == 129
    assert pals.get_exit_code(0x00FF) == 255


def test_log_rank_exit():
    """ Test logging rank exits (mainly for coverage) """
    # Log shepherd exits
    pals.log_rank_exit(-1, "nid000001", 0x0000)
    pals.log_rank_exit(-1, "nid000001", 0xFF00)
    pals.log_rank_exit(-1, "nid000001", 0x0001)
    pals.log_rank_exit(-1, "nid000001", 0x007F)
    pals.log_rank_exit(-1, "nid000001", 0x0081)
    pals.log_rank_exit(-1, "nid000001", 0x00FF)

    # Log rank exits
    pals.log_rank_exit(0, "nid000001", 0x0000)
    pals.log_rank_exit(0, "nid000001", 0xFF00)
    pals.log_rank_exit(0, "nid000001", 0x0001)
    pals.log_rank_exit(0, "nid000001", 0x007F)
    pals.log_rank_exit(0, "nid000001", 0x0081)
    pals.log_rank_exit(0, "nid000001", 0x00FF)


def test_handle_rpc():  # pylint: disable=too-many-locals
    """ Test handling PALS RPCs """
    sock = MockSocket()
    app = pals.PALSApp()

    stream_response = {"jsonrpc": "2.0", "result": None, "id": app.stream_rpcid}
    start_rpc = {"jsonrpc": "2.0", "method": "start", "id": app.start_rpcid}
    app.handle_rpc(sock, stream_response)
    compare_dicts(start_rpc, json.loads(sock.send_queue[0]))

    # Make temporary file for procinfo
    tmpfd, tmpfname = tempfile.mkstemp()
    os.close(tmpfd)

    start_response = {"jsonrpc": "2.0", "result": None, "id": app.start_rpcid}
    procinfo_rpc = {"jsonrpc": "2.0", "method": "procinfo", "id": app.procinfo_rpcid}
    app.handle_rpc(sock, start_response, procinfo_file=tmpfname)
    compare_dicts(json.loads(sock.send_queue[1]), procinfo_rpc)

    procinfo = {
        "apid": "5a2ecfa0-c99b-47f4-ae07-636da6dcc07e",
        "pids": [123, 234, 345, 456],
        "placement": [0, 0, 1, 2],
        "cmdidxs": [0, 0, 0, 1],
        "nodes": ["nid000001", "nid000002", "nid000003"],
        "executables": ["/home/users/seymour/a.out", "/home/users/seymour/b.out"],
    }
    procinfo_response = {"jsonrpc": "2.0", "result": procinfo, "id": app.procinfo_rpcid}
    app.handle_rpc(sock, procinfo_response, procinfo_file=tmpfname)

    with open(tmpfname, encoding='utf-8') as tmpfp:
        result = json.load(tmpfp)
    os.unlink(tmpfname)

    compare_dicts(procinfo, result)

    stdout_rpc = {
        "jsonrpc": "2.0",
        "method": "stdout",
        "params": {"content": "test", "encoding": "UTF-8"},
    }
    app.handle_rpc(sock, stdout_rpc)

    stderr_rpc = {
        "jsonrpc": "2.0",
        "method": "stderr",
        "params": {"content": "test", "encoding": "UTF-8"},
    }
    app.handle_rpc(sock, stderr_rpc)

    exit_rpc = {
        "jsonrpc": "2.0",
        "method": "exit",
        "params": {"rankid": 0, "host": "nid000001", "status": 1},
    }
    app.handle_rpc(sock, exit_rpc)

    complete_rpc = {"jsonrpc": "2.0", "method": "complete"}
    app.handle_rpc(sock, complete_rpc)
    assert app.complete

    error_rpc = {
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "RPC method foo not found"},
    }
    with pytest.raises(click.ClickException):
        app.handle_rpc(sock, error_rpc)


def test_forward_stdin():
    """ Test forwarding stdin to application """
    sock = MockSocket()

    # Send some UTF-8 content
    tmpfd, tmpfname = tempfile.mkstemp()
    os.write(tmpfd, b"test")
    os.lseek(tmpfd, 0, os.SEEK_SET)
    with os.fdopen(tmpfd) as tmpf:
        pals.forward_stdin(sock, tmpf)
    os.unlink(tmpfname)

    expected = {
        "jsonrpc": "2.0",
        "method": "stdin",
        "params": {"content": "test", "encoding": "UTF-8"},
    }
    compare_dicts(expected, json.loads(sock.send_queue[0]))

    expected = {"jsonrpc": "2.0", "method": "stdin", "params": {"eof": True}}
    compare_dicts(expected, json.loads(sock.send_queue[1]))

    # Send some non-UTF-8 content
    sock.send_queue = []
    tmpfd, tmpfname = tempfile.mkstemp()
    os.write(tmpfd, b"\xc0")
    os.lseek(tmpfd, 0, os.SEEK_SET)
    with os.fdopen(tmpfd) as tmpf:
        pals.forward_stdin(sock, tmpf)
    os.unlink(tmpfname)

    expected = {
        "jsonrpc": "2.0",
        "method": "stdin",
        "params": {"content": "wA==", "encoding": "base64"},
    }
    compare_dicts(expected, json.loads(sock.send_queue[0]))

    expected = {"jsonrpc": "2.0", "method": "stdin", "params": {"eof": True}}
    compare_dicts(expected, json.loads(sock.send_queue[1]))


def test_find_executable():
    """ Test searching for executable files """
    oldpath = os.environ.get("PATH")

    # If path contains a slash it's returned verbatim
    assert pals.find_executable("foo/bar") == "foo/bar"

    # If no PATH is set it's returned verbatim
    if "PATH" in os.environ:
        del os.environ["PATH"]
    assert pals.find_executable("foobar") == "foobar"

    # Test with something we should find
    if os.path.exists("/usr/bin/true") and os.access("/usr/bin/true", os.X_OK):
        os.environ["PATH"] = "/foobar:/usr/bin:/bin"
        assert pals.find_executable("true") == "/usr/bin/true"

    # Test with something we shouldn't find
    os.environ["PATH"] = "."
    assert pals.find_executable("foobar") is None

    # Reset PATH
    os.environ["PATH"] = oldpath


def test_get_executables():
    """ Test getting the set of binaries to transfer """
    req = {
        "cmds": [
            {"argv": ["/bin/pwd"]},
            {"argv": ["/bin/pwd"]},
            {"argv": ["/bin/echo", "foo"]},
        ]
    }

    # transfer=false doesn't modify argv
    assert pals.get_executables(req, False) == set(["/bin/pwd", "/bin/echo"])
    assert req["cmds"][0]["argv"] == ["/bin/pwd"]
    assert req["cmds"][1]["argv"] == ["/bin/pwd"]
    assert req["cmds"][2]["argv"] == ["/bin/echo", "foo"]

    # transfer=true modifies argv
    assert pals.get_executables(req, True) == set(["/bin/pwd", "/bin/echo"])
    assert req["cmds"][0]["argv"] == ["pwd"]
    assert req["cmds"][1]["argv"] == ["pwd"]
    assert req["cmds"][2]["argv"] == ["echo", "foo"]


def test_split_mpmd_args():
    """ Test splitting MPMD arguments """
    assert pals.split_mpmd_args(["hostname"]) == [["hostname"]]
    assert pals.split_mpmd_args(["hostname", ":", "echo"]) == [["hostname"], ["echo"]]
    assert pals.split_mpmd_args(["hostname", "-v", ":", "-n4", "echo", "foo"]) == [
        ["hostname", "-v"],
        ["-n4", "echo", "foo"],
    ]


def test_get_resource_limits():
    """ Test fetching resource limits """
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert pals.get_resource_limits([]) == {}
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert pals.get_resource_limits(["foo"]) == {}

    soft, hard = resource.getrlimit(
        resource.RLIMIT_CORE
    )  # pylint: disable=c-extension-no-member
    assert pals.get_resource_limits(["CORE"]) == {"CORE": "%d %d" % (soft, hard)}


def test_parse_hostfile():
    """ Test host file parsing """
    hostfile = io.StringIO("\n# comment line\nhost1\n host2 \n")
    assert pals.parse_hostfile(hostfile) == ["host1", "host2"]
    hostfile.close()
    with pytest.raises(ValueError):
        pals.parse_hostfile(hostfile)
    hostfile = io.StringIO("\n# comment line\nhost1\n host1 \n")
    assert pals.parse_hostfile(hostfile) == ["host1", "host1"]
    hostfile.close()
