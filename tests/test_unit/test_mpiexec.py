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
test_mpiexec.py - Unit tests for the mpiexec module
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


def test_get_hostlist():
    """ Test parsing a host list from file, argument, or environment """
    # Test some bad host lists
    with pytest.raises(click.UsageError):
        mpiexec.get_hostlist("a,,b", None)
    hostfile = io.StringIO("\n# comment line\n\n")
    with pytest.raises(click.UsageError):
        mpiexec.get_hostlist(None, hostfile)
    hostfile.close()

    # Test default
    assert mpiexec.get_hostlist(None, None) == [socket.gethostname()]  # pylint: disable=no-member

    # Use the command line argument if present
    assert mpiexec.get_hostlist("a,b", None) == ["a", "b"]

    # Read a host file
    hostfile = io.StringIO("\n# comment line\na\nb\n")
    assert mpiexec.get_hostlist(None, hostfile) == ["a", "b"]
    hostfile.close()

    # Hosts should override hostfile
    hostfile = io.StringIO("\n# comment line\na\nb\n")
    assert mpiexec.get_hostlist("c,d", hostfile) == ["c", "d"]
    hostfile.close()


def test_get_launch_env():
    """ Test launch environment """
    savedenv = os.environ
    os.environ = {"foo": "bar", "baz": "bat"}

    # Test -envall/-envnone
    assert mpiexec.get_launch_env(None, False, [], None) == []
    assert sorted(mpiexec.get_launch_env(None, True, [], None)) == sorted(
        ["foo=bar", "baz=bat"]
    )

    # Test -envlist
    assert mpiexec.get_launch_env("foo", False, [], None) == ["foo=bar"]
    assert sorted(mpiexec.get_launch_env(
        "foo,baz",
        False,
        [],
        None
    )) == sorted(["foo=bar", "baz=bat"])
    assert sorted(mpiexec.get_launch_env(
        "foo,baz,bap",
        False,
        [],
        None
    )) == sorted(["foo=bar", "baz=bat"])

    # Test -env
    assert mpiexec.get_launch_env(None, False, [("foo", "cat")], None) == ["foo=cat"]
    assert sorted(mpiexec.get_launch_env(None, True, [("foo", "cat")], None)) == sorted(
        [
            "foo=cat",
            "baz=bat",
        ]
    )
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
        mpiexec.parse_mpmd_file(tmpfname, None, 1, 0)

    # File with only spaces and comments isn't good either
    os.write(tmpfd, b"# comment\n\t\n \n\\\n")
    with pytest.raises(click.ClickException):
        mpiexec.parse_mpmd_file(tmpfname, None, 1, 0)

    # Negative -n value not allowed
    os.lseek(tmpfd, 0, os.SEEK_SET)
    os.write(tmpfd, b"-n -1 hostname\n")
    with pytest.raises(SystemExit):
        mpiexec.parse_mpmd_file(tmpfname, None, 1, 0)

    # Must have executable
    os.lseek(tmpfd, 0, os.SEEK_SET)
    os.write(tmpfd, b"-n 1\n")
    with pytest.raises(SystemExit):
        mpiexec.parse_mpmd_file(tmpfname, None, 1, 0)

    # umask must be octal
    os.lseek(tmpfd, 0, os.SEEK_SET)
    os.write(tmpfd, b"--umask 99 hostname\n")
    with pytest.raises(SystemExit):
        mpiexec.parse_mpmd_file(tmpfname, None, 1, 0)

    # Good file with a bunch of different options
    os.lseek(tmpfd, 0, os.SEEK_SET)
    os.write(tmpfd, b"# comment\n\nhostname\nhostname -a\n-n 2 hostname -b\n")
    os.write(tmpfd, b"-n 3 --wdir /tmp -umask 0222 -d 2 -ppn 3 hostname -c\n")
    os.write(tmpfd, b"-n4 --wdir=/home --umask=0333 --depth=3 --ppn=4 hostname -d\n")
    cmds = [
        dict(argv=["hostname"], nranks=1, wdir=wdir, umask=umask, depth=7, ppn=1),
        dict(argv=["hostname", "-a"], nranks=1, wdir=wdir, umask=umask, depth=7, ppn=1),
        dict(argv=["hostname", "-b"], nranks=2, wdir=wdir, umask=umask, depth=7, ppn=1),
        dict(argv=["hostname", "-c"], nranks=3, wdir="/tmp", umask=0o222, depth=2, ppn=3),
        dict(argv=["hostname", "-d"], nranks=4, wdir="/home", umask=0o333, depth=3, ppn=4),
    ]
    assert mpiexec.parse_mpmd_file(tmpfname, None, 7, 1) == cmds

    os.close(tmpfd)
    os.unlink(tmpfname)

    # Nonexistent file should produce a Click exception
    with pytest.raises(click.ClickException):
        mpiexec.parse_mpmd_file(tmpfname, None, 1, 0)
