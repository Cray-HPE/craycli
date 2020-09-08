"""
cli.py - mpiexec PALS CLI
Copyright 2019-2020 Cray Inc. All Rights Reserved.
"""
# pylint: disable=bad-continuation
import argparse
import os
import socket
import sys

import click

from cray import core
from cray.pals import PALSApp, split_mpmd_args

SIGNAL_RECEIVED = 0  # Last signal number received
PING_INTERVAL = 20  # WebSocket ping interval


def validate_soft(ctx, param, value):
    # pylint: disable=unused-argument
    """ Convert a soft option into a set of acceptable ranks """
    if value is None:
        return None

    try:
        vals = set()
        for triplet in value.split(","):
            fields = triplet.split(":")
            if len(fields) == 1:
                # Single value
                vals.add(int(fields[0]))
            elif len(fields) == 2:
                # Inclusive range
                vals.update(range(int(fields[0]), int(fields[1]) + 1))
            elif len(fields) == 3:
                # Range with step
                start = int(fields[0])
                end = int(fields[1])
                step = int(fields[2])

                # Adjust the end value to make an inclusive range
                if step > 0:
                    end += 1
                elif step < 0:
                    end -= 1
                vals.update(range(start, end, step))

        return vals
    except ValueError:
        raise click.BadParameter("%s is not a valid soft value" % value)


def soft_nprocs(soft, nprocs):
    """ Reduce the number of ranks to the largest acceptable soft value """
    # If no soft specification given, use -n value
    if not soft:
        return nprocs

    # Filter to values between 1 and nprocs
    try:
        return max([x for x in soft if 0 < x <= nprocs])
    except ValueError:
        raise click.UsageError("No soft values found between 1 and %d" % nprocs)


def validate_umask(ctx, param, value):
    # pylint: disable=unused-argument
    """ Validate a umask setting """
    try:
        umaskint = int(value, base=8)
        if umaskint < 0:
            raise click.BadParameter(
                "%s is smaller than the minimum valid value 0" % value
            )
        if umaskint > 0o777:
            raise click.BadParameter(
                "%s is larger than the maximum valid value 0777" % value
            )

        return umaskint
    except ValueError:
        raise click.BadParameter("%s is not a valid octal value" % value)


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


def get_hostlist(hosts, hostfile):
    """ Given command-line arguments, produce a host list """
    hostlist = []
    if hostfile:
        hostlist = parse_hostfile(hostfile)
    elif hosts:
        hostlist = hosts.split(",")
    else:
        hostlist = [socket.gethostname()]

    if not hostlist:
        raise click.UsageError("No host list provided")
    if "" in hostlist:
        raise click.UsageError("Host list contains invalid entry")

    return hostlist


def get_launch_env(envlist, envall, env, path):
    """ Given command line arguments, build up the environment array """

    # First handle the arguments that export existing environment
    if envlist:
        # Copy the listed keys for -envlist
        environ = {
            key: os.environ[key] for key in envlist.split(",") if key in os.environ
        }
    elif envall:
        # Copy the whole environment for -envall
        environ = os.environ.copy()
    else:
        # Otherwise start from scratch
        environ = {}

    # Next add environment variables explicitly called out
    # Overrides anything already set
    if env:
        for key, val in env:
            environ[key] = val

    # Add path argument if given
    if path:
        environ["PATH"] = path

    # Format into array in the expected format
    return ["%s=%s" % (key, val) for key, val in environ.items()]


def get_umask():
    """ Return the current umask value """
    umask = os.umask(0)
    os.umask(umask)
    return umask


def get_wdir():
    """ Get the current working directory, if it exists """
    try:
        return os.getcwd()
    except OSError:
        return None


def octal(val):
    """ Parse a string into an octal value """
    return int(val, 8)


def posint(val):
    """ Parse a string into a positive integer """
    ival = int(val)
    if ival <= 0:
        raise argparse.ArgumentTypeError("%s must be positive" % val)
    return ival


def get_cmd(executable, args, nranks, soft, wdir, umask):
    """ Format a command dictionary """
    cmd = {"argv": [executable] + list(args), "nranks": soft_nprocs(soft, nranks)}
    if wdir:
        cmd["wdir"] = wdir
    if umask:
        cmd["umask"] = umask
    return cmd


def parse_mpmd_args(argv, soft):
    """ Parse MPMD command arguments into a command dictionary """
    parser = argparse.ArgumentParser(prog="", description="MPMD Command Definition")
    parser.add_argument(
        "-n", "-np", "--np", default=1, type=posint, help="number of processes to start"
    )
    parser.add_argument(
        "-wdir", "--wdir", default=get_wdir(), help="command working directory"
    )
    parser.add_argument(
        "-umask", "--umask", default=get_umask(), type=octal, help="file creation mask"
    )
    parser.add_argument("executable", help="executable to launch")
    parser.add_argument(
        "args", nargs=argparse.REMAINDER, help="arguments to executable"
    )

    # Parse arguments
    args = parser.parse_args(argv)

    # Format into a command dictionary
    return get_cmd(args.executable, args.args, args.np, soft, args.wdir, args.umask)


def parse_mpmd_file(configfile, soft=None):
    """ Read an MPMD config file and return a list of commands """
    try:
        cmds = []
        with open(configfile) as config:
            content = config.read().replace("\\\n", "")
            for line in content.splitlines():
                line = line.strip()

                # Ignore empty lines and comment lines
                if not line or line[0] == "#":
                    continue

                cmds.append(parse_mpmd_args(line.split(), soft))

        # Make sure we got at least one command
        if not cmds:
            raise click.ClickException("No commands found in %s" % configfile)

        return cmds
    except (IOError, OSError) as err:
        raise click.ClickException(
            "Couldn't read config file %s: %s" % (configfile, str(err))
        )


def parse_mpmd(executable, args, nranks, soft, wdir, umask):
    """ Parse MPMD commands from the given arguments """

    # Split into separate commands
    cmdargvs = split_mpmd_args(list(args))

    # Create first command
    cmds = [get_cmd(executable, cmdargvs[0], nranks, soft, wdir, umask)]

    # Add other commands
    for cmdargv in cmdargvs[1:]:
        cmds.append(parse_mpmd_args(cmdargv, soft))

    return cmds


@core.command(
    name="mpiexec",
    context_settings={"ignore_unknown_options": True, "allow_interspersed_args": False},
    needs_globals=True,
)
@core.option(
    "-n",
    "-np",
    "--np",
    "nranks",
    default=1,
    envvar="PALS_NRANKS",
    type=click.IntRange(1),
    help="number of processes to start",
)
@core.option(
    "-ppn",
    "--ppn",
    default=0,
    envvar="PALS_PPN",
    type=click.IntRange(0),
    help="processes per node",
)
@core.option(
    "-soft",
    "--soft",
    callback=validate_soft,
    envvar="PALS_SOFT",
    help="specify acceptable values for number of processes",
)
@core.option(
    "-host",
    "--host",
    "-hosts",
    "--hosts",
    "-hostlist",
    "--hostlist",
    "hostlist",
    envvar="PALS_HOSTLIST",
    help="comma-separated list of hostnames to run processes on",
)
@core.option(
    "-f",
    "-hostfile",
    "--hostfile",
    "hostfile",
    envvar=["PALS_HOSTFILE", "PBS_NODEFILE"],
    type=click.File(),
    help="file containing hostnames to run processes on",
)
@core.option("-arch", "--arch", help="compute node architecture to run on (ignored)")
@core.option(
    "-wdir",
    "--wdir",
    default=get_wdir(),
    envvar="PALS_WDIR",
    help="application working directory",
)
@core.option(
    "-path", "--path", envvar="PALS_PATH", help="list of paths to search for executable"
)
@core.option("-file", "--file", help="file with additional information (ignored)")
@core.option(
    "-configfile",
    "--configfile",
    is_flag=True,
    help="file with MPMD specifications, one per line",
)
@core.option(
    "-umask",
    "--umask",
    callback=validate_umask,
    envvar="PALS_UMASK",
    default="0%o" % get_umask(),
    help="file creation mask",
)
@core.option(
    "-env", "--env", nargs=2, multiple=True, help="set an environment variable"
)
@core.option(
    "-envlist",
    "--envlist",
    envvar="PALS_ENVLIST",
    help="comma-separated list of environment variables to export",
)
@core.option(
    "-envall/-envnone",
    "--envall/--envnone",
    default=True,
    envvar="PALS_ENVALL",
    help="export environment variables to application",
)
@core.option(
    "--transfer/--no-transfer",
    default=True,
    envvar="PALS_TRANSFER",
    help="transfer application binaries to compute nodes",
)
@core.option("--cpu-bind", envvar="PALS_CPU_BIND", help="CPU binding for application")
@core.option(
    "--mem-bind", envvar="PALS_MEM_BIND", help="memory binding for application"
)
@core.option("-d", "--depth", default=1, envvar="PALS_DEPTH", help="CPUs per process")
@core.option(
    "-l",
    "--label/--no-label",
    default=False,
    envvar="PALS_LABEL",
    help="label output with process host and rank",
)
@core.option(
    "--include-tasks",
    envvar="PALS_INCLUDE_TASKS",
    help="comma-separated list of ATOM tasks to execute",
)
@core.option(
    "--exclude-tasks",
    envvar="PALS_EXCLUDE_TASKS",
    help="comma-separated list of ATOM tasks to not execute",
)
@core.option(
    "--exclusive/--shared",
    envvar="PALS_EXCLUSIVE",
    help="require exclusive access to all nodes in application",
)
@core.option(
    "--line-buffer/--no-line-buffer",
    default=False,
    envvar="PALS_LINE_BUFFER",
    help="enable/disable line buffered mode for stdio",
)
@core.option(
    "--procinfo-file",
    envvar="PALS_PROCINFO_FILE",
    help="write application process information to the given file",
)
@core.option(
    "--abort-on-failure/--no-abort-on-failure",
    envvar="PALS_ABORT_ON_FAILURE",
    is_flag=True,
    default=True,
    help="abort/don't abort entire application if a rank exits with non-zero status",
)
@core.argument("executable")
@core.argument("args", nargs=-1)
def cli(
    nranks,
    ppn,
    soft,
    hostlist,
    hostfile,
    arch,
    wdir,
    path,
    file,
    configfile,
    umask,
    env,
    envlist,
    envall,
    transfer,
    cpu_bind,
    mem_bind,
    depth,
    label,
    include_tasks,
    exclude_tasks,
    exclusive,
    line_buffer,
    procinfo_file,
    abort_on_failure,
    executable,
    args,
):
    # pylint: disable=unused-argument, too-many-arguments, too-many-locals, redefined-builtin
    """
    Run an application using the Parallel Application Launch Service

    CPU BINDING

    The --cpu-bind option is formatted as [verbose,]<keyword>[:arguments]

    \b
    Keywords:
    * none - No CPU binding.
    * numa, socket, core, thread - Bind ranks to the specified hardware.
    * depth - Bind ranks to number of threads in 'depth' argument.
    * list - Bind ranks to colon-separated rangelists of CPUs.
    * mask - Bind ranks to comma-separated bitmasks of CPUs.

    MEMORY (NUMA NODE) BINDING

    The --mem-bind option is formatted as [verbose,]<keyword>[:arguments]

    \b
    Keywords:
    * none - No memory binding.
    * local - Restrict each rank to use only its own NUMA node memory.
    * list - Bind ranks to colon-separated rangelists of NUMA nodes.
    * mask - Bind ranks to comma-separated bitmasks of NUMA nodes.

    ENVIRONMENT VARIABLES

    \b
    Input Environment Variables:
    * PALS_NRANKS - default number of ranks
    * PALS_PPN - default ranks per node
    * PALS_SOFT - default soft number of ranks
    * PALS_HOSTLIST - default host list
    * PALS_HOSTFILE - default host file
    * PALS_WDIR - default working directory
    * PALS_PATH - default executable search path
    * PALS_UMASK - default file creation mask
    * PALS_ENVLIST - default list of exported environment variables
    * PALS_ENVALL - default export of all environment variables
    * PALS_TRANSFER - default executable transfer
    * PALS_CPU_BIND - default CPU binding
    * PALS_MEM_BIND - default memory binding
    * PALS_DEPTH - default CPUs per rank
    * PALS_LABEL - default output labeling
    * PALS_INCLUDE_TASKS - comma-separated list of ATOM tasks to execute
    * PALS_EXCLUDE_TASKS - comma-separated list of ATOM tasks to not execute
    * PALS_EXCLUSIVE - if set, request exclusive access to all app nodes
    * PALS_LINE_BUFFER - Whether to enable line buffered mode
    * PALS_PROCINFO_FILE - Write application process information to the given file
    * PALS_ABORT_ON_FAILURE - Whether to abort application on non-zero rank exit
    """

    # Create a launch request from arguments
    launchreq = {
        "hosts": get_hostlist(hostlist, hostfile),
        "ppn": ppn,
        "environment": get_launch_env(envlist, envall, env, path),
        "depth": depth,
        "abort_on_failure": abort_on_failure,
    }

    # Parse commands
    if configfile:
        launchreq["cmds"] = parse_mpmd_file(executable, soft)
    else:
        launchreq["cmds"] = parse_mpmd(executable, args, nranks, soft, wdir, umask)

    # Add optional settings
    if "PBS_JOBID" in os.environ:
        launchreq["jobid"] = os.environ["PBS_JOBID"]
    if cpu_bind:
        launchreq["cpubind"] = cpu_bind
    if mem_bind:
        launchreq["membind"] = mem_bind
    if include_tasks:
        launchreq["include_tasks"] = include_tasks.split(",")
    if exclude_tasks:
        launchreq["exclude_tasks"] = exclude_tasks.split(",")
    if exclusive:
        launchreq["exclusive"] = exclusive
    if line_buffer:
        launchreq["line_buffered"] = True

    # Make the launch request
    app = PALSApp()
    exit_codes = app.launch(launchreq, transfer, False, procinfo_file)

    # Calculate exit code
    exit_code = max(exit_codes) if exit_codes else 0
    sys.exit(exit_code)
