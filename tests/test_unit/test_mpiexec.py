"""
test_mpiexec.py - Unit tests for the mpiexec module
Copyright 2019-2020 Cray Inc. All Rights Reserved.
"""
# pylint: disable=import-error
import io
import os
import socket
import tempfile
import click
import pytest

import cray.modules.mpiexec.cli as mpiexec


def test_validate_soft():
    """ Test validation of the -soft argument """
    # Must be all numbers
    with pytest.raises(click.BadParameter):
        mpiexec.validate_soft(None, None, "~")
    with pytest.raises(click.BadParameter):
        mpiexec.validate_soft(None, None, "1:~")
    with pytest.raises(click.BadParameter):
        mpiexec.validate_soft(None, None, "1:2:~")

    # If not given, default to None
    assert mpiexec.validate_soft(None, None, None) is None

    # Test some valid sets
    assert mpiexec.validate_soft(None, None, "1") == set([1])
    assert mpiexec.validate_soft(None, None, "1:3") == set([1, 2, 3])
    assert mpiexec.validate_soft(None, None, "1:3:2") == set([1, 3])
    assert mpiexec.validate_soft(None, None, "3:1:-2") == set([1, 3])
    assert mpiexec.validate_soft(None, None, "1,5,9:8:-1") == set([1, 5, 8, 9])


def test_soft_nprocs():
    """ Test setting nprocs based on soft values """
    with pytest.raises(click.UsageError):
        mpiexec.soft_nprocs(set([-1]), 1)
    with pytest.raises(click.UsageError):
        mpiexec.soft_nprocs(set([2]), 1)

    assert mpiexec.soft_nprocs(set(), 4) == 4
    assert mpiexec.soft_nprocs(set([-1, 1, 2, 3, 5]), 4) == 3


def test_validate_umask():
    """ Test validation of umask arguments """
    with pytest.raises(click.BadParameter):
        mpiexec.validate_umask(None, None, "-1")
    with pytest.raises(click.BadParameter):
        mpiexec.validate_umask(None, None, "07777")
    with pytest.raises(click.BadParameter):
        mpiexec.validate_umask(None, None, "asdf")

    assert mpiexec.validate_umask(None, None, "0123") == 0o123


def test_parse_hostfile():
    """ Test host file parsing """
    hostfile = io.StringIO(u"\n# comment line\nhost1\n host2 \n")
    assert mpiexec.parse_hostfile(hostfile) == ["host1", "host2"]
    hostfile.close()
    with pytest.raises(ValueError):
        mpiexec.parse_hostfile(hostfile)
    hostfile = io.StringIO(u"\n# comment line\nhost1\n host1 \n")
    assert mpiexec.parse_hostfile(hostfile) == ["host1", "host1"]
    hostfile.close()


def test_get_hostlist():
    """ Test parsing a host list from file, argument, or environment """
    # Test some bad host lists
    with pytest.raises(click.UsageError):
        mpiexec.get_hostlist("a,,b", None)
    hostfile = io.StringIO(u"\n# comment line\n\n")
    with pytest.raises(click.UsageError):
        mpiexec.get_hostlist(None, hostfile)
    hostfile.close()

    # Test default
    assert mpiexec.get_hostlist(None, None) == [socket.gethostname()]

    # Use the command line argument if present
    assert mpiexec.get_hostlist("a,b", None) == ["a", "b"]

    # Read a host file
    hostfile = io.StringIO(u"\n# comment line\na\nb\n")
    assert mpiexec.get_hostlist(None, hostfile) == ["a", "b"]
    hostfile.close()


def test_get_launch_env():
    """ Test launch environment """
    savedenv = os.environ
    os.environ = {"foo": "bar", "baz": "bat"}

    # Test -envall/-envnone
    assert mpiexec.get_launch_env(None, False, [], None) == []
    assert mpiexec.get_launch_env(None, True, [], None) == ["foo=bar", "baz=bat"]

    # Test -envlist
    assert mpiexec.get_launch_env("foo", False, [], None) == ["foo=bar"]
    assert mpiexec.get_launch_env("foo,baz", False, [], None) == ["foo=bar", "baz=bat"]
    assert mpiexec.get_launch_env("foo,baz,bap", False, [], None) == [
        "foo=bar",
        "baz=bat",
    ]

    # Test -env
    assert mpiexec.get_launch_env(None, False, [("foo", "cat")], None) == ["foo=cat"]
    assert mpiexec.get_launch_env(None, True, [("foo", "cat")], None) == [
        "foo=cat",
        "baz=bat",
    ]
    assert mpiexec.get_launch_env("foo", False, [("foo", "cat")], None) == ["foo=cat"]

    # Test -path
    assert mpiexec.get_launch_env(None, False, [], "/tmp") == ["PATH=/tmp"]
    assert sorted(mpiexec.get_launch_env(None, True, [], "/tmp")) == sorted(
        ["PATH=/tmp", "foo=bar", "baz=bat"]
    )
    assert sorted(mpiexec.get_launch_env("foo", False, [], "/tmp")) == sorted(
        ["PATH=/tmp", "foo=bar"]
    )

    os.environ = savedenv


def test_get_umask():
    """ Test getting the current umask """
    # Set a test umask
    umask = os.umask(0o246)

    # Test that we got the right umask
    assert mpiexec.get_umask() == 0o246

    # Reset the umask and check that calling get_umask() didn't change it
    assert os.umask(umask) == 0o246


def test_get_wdir():
    """ Test getting the working directory """
    wdir = os.getcwd()

    assert mpiexec.get_wdir() == wdir

    # Set up a situation where we're in a nonexistent directory
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    os.rmdir(tmpdir)
    assert mpiexec.get_wdir() is None

    # Go back to where we started
    os.chdir(wdir)


def test_parse_mpmd_file():
    """ Test parsing an MPMD file """
    tmpfd, tmpfname = tempfile.mkstemp()
    wdir = os.getcwd()
    umask = os.umask(0)
    os.umask(umask)

    # Empty file should produce a Click exception
    with pytest.raises(click.ClickException):
        mpiexec.parse_mpmd_file(tmpfname)

    # File with only spaces and comments isn't good either
    os.write(tmpfd, b"# comment\n\t\n \n\\\n")
    with pytest.raises(click.ClickException):
        mpiexec.parse_mpmd_file(tmpfname)

    # Negative -n value not allowed
    os.lseek(tmpfd, 0, os.SEEK_SET)
    os.write(tmpfd, b"-n -1 hostname\n")
    with pytest.raises(SystemExit):
        mpiexec.parse_mpmd_file(tmpfname)

    # Must have executable
    os.lseek(tmpfd, 0, os.SEEK_SET)
    os.write(tmpfd, b"-n 1\n")
    with pytest.raises(SystemExit):
        mpiexec.parse_mpmd_file(tmpfname)

    # umask must be octal
    os.lseek(tmpfd, 0, os.SEEK_SET)
    os.write(tmpfd, b"--umask 99 hostname\n")
    with pytest.raises(SystemExit):
        mpiexec.parse_mpmd_file(tmpfname)

    # Good file with a bunch of different options
    os.lseek(tmpfd, 0, os.SEEK_SET)
    os.write(tmpfd, b"# comment\n\nhostname\nhostname -a\n-n 2 hostname -b\n")
    os.write(tmpfd, b"-n 3 --wdir /tmp -umask 0222 hostname -c\n")
    os.write(tmpfd, b"-n4 --wdir=/home --umask=0333 hostname -d\n")
    cmds = [
        {"argv": ["hostname"], "nranks": 1, "wdir": wdir, "umask": umask},
        {"argv": ["hostname", "-a"], "nranks": 1, "wdir": wdir, "umask": umask},
        {"argv": ["hostname", "-b"], "nranks": 2, "wdir": wdir, "umask": umask},
        {"argv": ["hostname", "-c"], "nranks": 3, "wdir": "/tmp", "umask": 0o222},
        {"argv": ["hostname", "-d"], "nranks": 4, "wdir": "/home", "umask": 0o333},
    ]
    assert mpiexec.parse_mpmd_file(tmpfname) == cmds

    os.close(tmpfd)
    os.unlink(tmpfname)

    # Nonexistent file should produce a Click exception
    with pytest.raises(click.ClickException):
        mpiexec.parse_mpmd_file(tmpfname)
