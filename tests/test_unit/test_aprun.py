"""
test_aprun.py - Unit tests for the aprun module
Copyright 2019 Cray Inc. All Rights Reserved.
"""
# pylint: disable=import-error
import io
import os
import tempfile
import click
import pytest

import cray.modules.aprun.cli as aprun


def test_parse_hostfile():
    """ Test host file parsing """
    hostfile = io.StringIO(u"\n# comment line\nnid000001\n nid200000 \n")
    assert aprun.parse_hostfile(hostfile) == [1, 200000]
    hostfile.close()

    hostfile = io.StringIO(u"\n# comment line\nnid000001\n nid000001 \n")
    assert aprun.parse_hostfile(hostfile) == [1, 1]
    hostfile.close()


def test_parse_rangelist():
    """ Test range list parsing """
    assert aprun.parse_rangelist("1") == [1]
    assert aprun.parse_rangelist("1-3") == [1, 2, 3]
    assert aprun.parse_rangelist("1,3") == [1, 3]
    assert aprun.parse_rangelist("1-3,8-10") == [1, 2, 3, 8, 9, 10]
    assert aprun.parse_rangelist("4-1,9") == [4, 3, 2, 1, 9]

    with pytest.raises(click.ClickException):
        aprun.parse_rangelist("$")
    with pytest.raises(click.ClickException):
        aprun.parse_rangelist(",")
    with pytest.raises(click.ClickException):
        aprun.parse_rangelist("1,")
    with pytest.raises(click.ClickException):
        aprun.parse_rangelist("-")
    with pytest.raises(click.ClickException):
        aprun.parse_rangelist("1-")
    with pytest.raises(click.ClickException):
        aprun.parse_rangelist("-2")


def test_get_hostlist():
    """ Test parsing a host list from file, argument, or environment """
    # Need some nodes
    with pytest.raises(click.ClickException):
        aprun.get_hostlist(None, None, None, None)
    with pytest.raises(click.ClickException):
        aprun.get_hostlist("1-3", None, "3,2,1", None)

    assert aprun.get_hostlist("1", None, None, None) == ["nid000001"]
    assert aprun.get_hostlist("1-3", None, "2", None) == ["nid000001", "nid000003"]
    assert aprun.get_hostlist("1,2,2,2", None, "2", None) == ["nid000001"]
    assert aprun.get_hostlist("1,2,2", None, "1", None) == ["nid000002", "nid000002"]

    # Test getting lists from files
    nidfile = io.StringIO(u"1\n2-3,4\n\n5")
    exclfile = io.StringIO(u"2-4\n4\n")
    assert aprun.get_hostlist(None, nidfile, None, exclfile) == [
        "nid000001",
        "nid000005",
    ]
    nidfile.close()
    exclfile.close()

    # Test getting list from PBS_NODEFILE
    tmpfd, tmpfname = tempfile.mkstemp()
    os.write(tmpfd, b"nid000001.local\nnid000001.local\nnid000002.local\n")
    os.environ["PBS_NODEFILE"] = tmpfname
    assert aprun.get_hostlist(None, None, None, None) == [
        "nid000001",
        "nid000001",
        "nid000002",
    ]
    os.unlink(tmpfname)
    del os.environ["PBS_NODEFILE"]


def test_get_launch_env():
    """ Test launch environment """
    environ = {"foo": "bar", "baz": "bat"}

    # Test no overrides
    assert aprun.get_launch_env(None, environ) == ["foo=bar", "baz=bat"]

    # Test with invalid overrides
    with pytest.raises(click.ClickException):
        aprun.get_launch_env(["ASDF"], environ)
    with pytest.raises(click.ClickException):
        aprun.get_launch_env(["ASDF=", "QWER"], environ)

    # Test with some overrides
    assert aprun.get_launch_env(["foo=boo"], environ) == ["foo=boo", "baz=bat"]
    assert aprun.get_launch_env(["baz=boo"], environ) == ["foo=bar", "baz=boo"]
    assert aprun.get_launch_env(["too=two"], environ) == [
        "foo=bar",
        "baz=bat",
        "too=two",
    ]


def test_get_umask():
    """ Test getting the current umask """
    # Set a test umask
    umask = os.umask(0o246)

    # Test that we got the right umask
    assert aprun.get_umask() == 0o246

    # Reset the umask and check that calling get_umask() didn't change it
    assert os.umask(umask) == 0o246


def test_get_wdir():
    """ Test getting the working directory """
    wdir = os.getcwd()

    assert aprun.get_wdir(None) == wdir
    assert aprun.get_wdir("/tmp") == "/tmp"

    # Set up a situation where we're in a nonexistent directory
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    os.rmdir(tmpdir)
    with pytest.raises(click.ClickException):
        aprun.get_wdir(None)

    # Go back to where we started
    os.chdir(wdir)


def test_get_cpubind():
    """ Test CPU binding translation """
    assert aprun.get_cpubind(None) == "thread"
    assert aprun.get_cpubind("cpu") == "thread"
    assert aprun.get_cpubind("depth") == "depth"
    assert aprun.get_cpubind("numa_node") == "numa"
    assert aprun.get_cpubind("none") == "none"
    assert aprun.get_cpubind("core") == "core"
    assert aprun.get_cpubind("0-3:4-7") == "list:0-3:4-7"


def test_get_membind():
    """ Test memory binding translation """
    assert aprun.get_membind(False) == "none"
    assert aprun.get_membind(True) == "local"


def test_get_exclusive():
    """ Test -F exclusive/share option translation """
    # Only first character of option is checked (e=exclusive, s=non-exclusive)
    assert aprun.get_exclusive(None) is None
    assert aprun.get_exclusive("exclusive")
    assert aprun.get_exclusive("EXCLUSIVE")
    assert aprun.get_exclusive("EXTRA!")
    assert not aprun.get_exclusive("share")
    assert not aprun.get_exclusive("SHARE")
    assert not aprun.get_exclusive("sHare")
    with pytest.raises(click.ClickException):
        aprun.get_exclusive("crud")


def test_get_argv():
    """ Test building argv for the application """
    assert aprun.get_argv("/bin/hostname", [], True) == ["/bin/hostname"]
    assert aprun.get_argv("/bin/hostname", [], False) == ["hostname"]
    assert aprun.get_argv("/bin/hostname", ["-n", "-s"], True) == [
        "/bin/hostname",
        "-n",
        "-s",
    ]
    assert aprun.get_argv("/bin/hostname", ["-n", "-s"], False) == [
        "hostname",
        "-n",
        "-s",
    ]
