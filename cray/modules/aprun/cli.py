"""
cli.py - aprun PALS CLI

MIT License

(C) Copyright [2020-2021] Hewlett Packard Enterprise Development LP

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
import argparse
import base64
import os
import sys

import click

from cray import core
from cray.pals import PALSApp, split_mpmd_args, get_resource_limits, parse_hostfile

APRUN_ENV_ALIAS = {
    "ALPS_APP_DEPTH": "PALS_DEPTH",
    "ALPS_APP_ID": "PALS_APID",
    "ALPS_APP_PE": "PALS_RANKID",
}


def parse_rangelist(rli):
    """Parse a range list into a list of integers"""
    try:
        mylist = []
        for nidrange in rli.split(","):
            startstr, sep, endstr = nidrange.partition("-")
            start = int(startstr, 0)
            if sep:
                end = int(endstr, 0)
                if end < start:
                    mylist.extend(range(start, end - 1, -1))
                else:
                    mylist.extend(range(start, end + 1))
            else:
                mylist.append(start)
    except ValueError:
        # pylint: disable=raise-missing-from
        raise click.ClickException("Invalid range list %s" % rli)

    return mylist


def parse_rangelist_file(rlif):
    """Parse a file containing rangelists into a list of integers"""
    mylist = []
    for line in rlif:
        line = line.strip()
        if line and line[0] != "#":
            mylist.extend(parse_rangelist(line))
    return mylist


def nids_to_hosts(nidlist):
    """Convert a list of integer nids to a list of hostnames"""
    return ["nid%06d" % nid for nid in nidlist]


def get_hostlist(node_list, node_list_file, exclude_node_list, exclude_node_list_file):
    """Given command-line arguments, produce a host list"""
    nodelist = []
    excllist = []

    # Build node list from command line arguments
    if node_list:
        nodelist = nids_to_hosts(parse_rangelist(node_list))
    elif node_list_file:
        nodelist = nids_to_hosts(parse_rangelist_file(node_list_file))
    elif "PBS_NODEFILE" in os.environ:
        with open(os.environ["PBS_NODEFILE"], encoding="utf-8") as nodefile:
            nodelist = parse_hostfile(nodefile)

    # Build exclude node list from command line arguments
    if exclude_node_list:
        excllist = nids_to_hosts(parse_rangelist(exclude_node_list))
    elif exclude_node_list_file:
        excllist = nids_to_hosts(parse_rangelist_file(exclude_node_list_file))

    # Remove excluded nodes from host list
    hostlist = [node for node in nodelist if node not in excllist]

    # Check list before returning
    if not hostlist:
        raise click.ClickException("No host list provided")

    return hostlist


def get_launch_env(environment_override, environ=None):
    """Given command line arguments, build up the environment array"""
    # Copy the environment to avoid modifying the original
    if environ is None:
        environ = os.environ.copy()
    else:
        environ = environ.copy()

    # Override specified environment variables
    if environment_override:
        for envvar in environment_override:
            key, sep, val = envvar.partition("=")
            if not sep:
                raise click.ClickException("Invalid environment variable %s" % envvar)
            environ[key] = val

    # Format into array in the expected format
    return ["%s=%s" % (key, val) for key, val in environ.items()]


def get_umask():
    """Return the current umask value"""
    umask = os.umask(0)
    os.umask(umask)
    return umask


def get_wdir(wdir):
    """Get the current working directory to use for the launch"""
    # If user provided a wdir through argument or env var, use that
    if wdir:
        return wdir

    # Otherwise, attempt to get our cwd
    # aprun treated this as a fatal error, so we do too
    try:
        return os.getcwd()
    except OSError as err:
        raise click.ClickException("getcwd failed: %s" % str(err))


def get_cpubind(cpu_binding):
    """Convert aprun-style CPU binding to PALS-style"""
    # First check for keywords
    if not cpu_binding or cpu_binding == "cpu":
        return "thread"
    if cpu_binding == "depth":
        return "depth"
    if cpu_binding == "numa_node":
        return "numa"
    if cpu_binding == "none":
        return "none"
    if cpu_binding == "core":
        return "core"

    # If not a keyword, it's colon-separated rangelists
    return "list:%s" % cpu_binding


def get_membind(strict_memory_containment):
    """Get memory binding to use"""
    if strict_memory_containment:
        return "local"

    return "none"


def get_exclusive(access_mode):
    """Get exclusive setting from -F [exclusive|share] option"""
    # aprun only checked for e/E (exclusive) or s/S (share)
    if not access_mode:
        return None
    if access_mode[0].lower() == "e":
        return True
    if access_mode[0].lower() == "s":
        return False

    raise click.ClickException("Invalid -F/--access-mode argument %s" % access_mode)


def print_output(params, a_file):
    """Print output from a stdout/stderr RPC to the given file"""
    content = params.get("content")
    if not content:
        return

    # If encoded in base64, decode it before printing
    encoding = params.get("encoding")
    if encoding == "base64":
        content = base64.b64decode(content)

    click.echo(content, nl=False, file=a_file)


def get_argv(executable, args, bypass_app_transfer):
    """
    Get the application argv
    """
    if bypass_app_transfer:
        argv0 = executable
    else:
        argv0 = os.path.basename(executable)

    return [argv0] + list(args)


def posint(val):
    """Parse a string into a positive integer"""
    ival = int(val)
    if ival <= 0:
        raise argparse.ArgumentTypeError("%s must be positive" % val)
    return ival


def parse_mpmd(executable, args, pes, wdir, depth, ppn):
    """Parse MPMD commands from the given arguments"""

    # Split into separate commands
    cmdargvs = split_mpmd_args(list(args))

    # Create first command
    umask = get_umask()
    argv = [executable] + cmdargvs[0]
    cmds = [dict(argv=argv, nranks=pes, umask=umask, wdir=wdir, depth=depth, ppn=ppn)]

    # Create a parser for each other MPMD command
    parser = argparse.ArgumentParser(prog="", description="MPMD Command Definition")
    parser.add_argument(
        "-n", "--pes", default=1, type=posint, help="number of processes to start"
    )
    parser.add_argument("executable", help="executable to launch")
    parser.add_argument(
        "args", nargs=argparse.REMAINDER, help="arguments to executable"
    )
    parser.add_argument(
        "-d", "--cpus-per-pe", default=depth, type=posint, help="CPUs per process"
    )
    parser.add_argument(
        "-N", "--pes-per-node", default=ppn, type=posint, help="PEs per compute node"
    )

    # Add other commands
    for cmdargv in cmdargvs[1:]:
        # Parse args for this command
        cmdargs = parser.parse_args(cmdargv)

        # Create MPMD command dict
        argv = [cmdargs.executable] + list(cmdargs.args)
        cmds.append(
            dict(
                argv=argv,
                nranks=cmdargs.pes,
                umask=umask,
                wdir=wdir,
                depth=cmdargs.cpus_per_pe,
                ppn=cmdargs.pes_per_node,
            )
        )

    return cmds


def get_rlimits(memory_per_pe):
    """Get resource limits to transfer to application"""
    # Check relevant environment variables
    send_limits = int(os.environ.get("APRUN_XFER_LIMITS", 0))
    stack_limit = int(os.environ.get("APRUN_XFER_STACK_LIMIT", 0))

    # Always send CORE, CPU limits
    limitnames = ["CORE", "CPU"]

    if send_limits:
        limitnames.extend(
            [
                "RSS",
                "STACK",
                "FSIZE",
                "DATA",
                "NPROC",
                "NOFILE",
                "MEMLOCK",
                "AS",
                "LOCKS",
                "SIGPENDING",
                "MSGQUEUE",
                "NICE",
                "RTPRIO",
            ]
        )
    else:
        if memory_per_pe:
            limitnames.append("RSS")
        if stack_limit:
            limitnames.append("STACK")

    return get_resource_limits(limitnames)


@core.command(
    name="aprun",
    context_settings={"ignore_unknown_options": True, "allow_interspersed_args": False},
    needs_globals=True,
)
@core.option("-a", "--architecture", help="compute node architecture (ignored)")
@core.option(
    "-b", "--bypass-app-transfer", is_flag=True, help="skip application binary transfer"
)
@core.option(
    "-B",
    "--batch-args",
    is_flag=True,
    help="reuse batch reservation arguments (ignored)",
)
@core.option(
    "-C", "--reconnect", is_flag=True, help="reconnect on node failure (ignored)"
)
@core.option("--cpu-binding", "--cc", help="CPU binding for application")
@core.option("--cpu-binding-file", "--cp", help="specify binding in a file (ignored)")
@core.option(
    "-d", "--cpus-per-pe", default=1, type=click.IntRange(1), help="CPUs per PE"
)
@core.option(
    "-D", "--debug", default=0, type=click.IntRange(0), help="debug level (ignored)"
)
@core.option(
    "-e",
    "--environment-override",
    multiple=True,
    help="set an application environment variable (use VARNAME=value format)",
)
@core.option("-E", "--exclude-node-list", help="exclude a list of nodes from placement")
@core.option(
    "--exclude-node-list-file",
    type=click.File(),
    help="file with list of nodes to exclude",
)
@core.option("-F", "--access-mode", help="exclusive/share access mode")
@core.option("-j", "--cpus-per-cu", help="CPUs per compute unit (ignored)")
@core.option("-L", "--node-list", help="list of nodes for placement")
@core.option(
    "-l",
    "--node-list-file",
    type=click.File(),
    help="file with list of nodes for placement",
)
@core.option(
    "-m", "--memory-per-pe", envvar="APRUN_DEFAULT_MEMORY", help="memory per PE"
)
@core.option(
    "--mpmd-env", multiple=True, help="set an MPMD environment variable (ignored)"
)
@core.option(
    "-n",
    "--pes",
    default=1,
    type=click.IntRange(1),
    help="number of processing elements (PEs)",
)
@core.option(
    "-N",
    "--pes-per-node",
    default=0,
    type=click.IntRange(0),
    help="PEs per compute node",
)
@core.option("-p", "--protection-domain", help="use protection domain (ignored)")
@core.option("--p-governor", help="compute node performance governor (ignored)")
@core.option(
    "--p-state", envvar="APRUN_PSTATE", help="compute node performance state (ignored)"
)
@core.option("-q", "--quiet", "--silent", is_flag=True, help="quiet mode")
@core.option("-r", "--specialized-cpus", help="number of system process CPUs (ignored)")
@core.option("-R", "--relaunch", help="relaunch with fewer ranks on failure (ignored)")
@core.option("-S", "--pes-per-numa-node", help="number of PEs per NUMA node (ignored)")
@core.option(
    "--strict-memory-containment",
    "--ss",
    is_flag=True,
    help="restrict memory to local NUMA node",
)
@core.option(
    "-T",
    "--sync-output",
    envvar="APRUN_SYNC_TTY",
    is_flag=True,
    default=False,
    help="synchronize output",
)
@core.option("--wdir", envvar="APRUN_WDIR", help="application working directory")
@core.option(
    "-z",
    "--zone-sort",
    envvar="APRUN_ZONE_SORT",
    is_flag=True,
    help="memory zone sort at launch (ignored)",
)
@core.option(
    "-Z",
    "--zone-sort-secs",
    envvar="APRUN_ZONE_SORT_SECS",
    help="periodic memory zone sort (ignored)",
)
@core.option(
    "--procinfo-file",
    envvar="APRUN_PROCINFO_FILE",
    help="write application process information to the given file",
)
@core.option(
    "--abort-on-failure/--no-abort-on-failure",
    envvar="APRUN_ABORT_ON_FAILURE",
    is_flag=True,
    default=True,
    help="abort/don't abort entire application if a rank exits with non-zero status",
)
@core.option(
    "--pmi",
    envvar="APRUN_PMI",
    type=click.Choice(["cray", "pmix", "none"], case_sensitive=False),
    default="cray",
    help="Application PMI wire-up method ('cray' default)",
)
@core.option(
    "--sstartup/--no-sstartup",
    default=False,
    help="enable/disable Scalable Start Up",
)
@core.argument("executable")
@core.argument("args", nargs=-1)
def cli(
    architecture,
    bypass_app_transfer,
    batch_args,
    reconnect,
    cpu_binding,
    cpu_binding_file,
    cpus_per_pe,
    debug,
    environment_override,
    exclude_node_list,
    exclude_node_list_file,
    access_mode,
    cpus_per_cu,
    node_list,
    node_list_file,
    memory_per_pe,
    mpmd_env,
    pes,
    pes_per_node,
    protection_domain,
    p_governor,
    p_state,
    quiet,
    specialized_cpus,
    relaunch,
    pes_per_numa_node,
    strict_memory_containment,
    sync_output,
    wdir,
    zone_sort,
    zone_sort_secs,
    procinfo_file,
    abort_on_failure,
    pmi,
    sstartup,
    executable,
    args,
):
    # pylint: disable=unused-argument, too-many-arguments, too-many-locals, redefined-builtin
    """
    Run an application using the Parallel Application Launch Service

    ARGUMENT PROCESSING

    Use -- to separate the executable and its arguments from aprun's arguments.

    For example, use 'cray aprun -n 4 -- a.out -n 2' to launch 4 copies of
    'a.out -n 2'.

    CPU BINDING

    The --cpu-binding option is formatted as <keyword>|<cpu list>.

    The cpu list consists of colon-separated range lists of CPU numbers.
    The first range list will be used for the first PE on each node in the
    application, second range list for the second PE, etc.

    \b
    Keywords:
    * none - No CPU binding.
    * cpu(default) - Bind ranks to a single thread.
    * depth - Bind ranks to -d/--cpus-per-pe threads.
    * numa_node - Bind ranks each thread in its assigned NUMA node.
    * core - Bind ranks to every thread on -d/--cpus-per-pe cores.

    ENVIRONMENT VARIABLES

    \b
    Input Environment Variables:
    * APRUN_WDIR - Default working directory
    * APRUN_SYNC_TTY - Synchronize output
    * APRUN_PROCINFO_FILE - Write application process information to the given file
    * APRUN_ABORT_ON_FAILURE - Whether to abort application on non-zero rank exit
    * APRUN_PMI - Application PMI wire-up setting (cray, pmix, none)
    * APRUN_XFER_LIMITS - If set to 1, transfer all resource limits
    * APRUN_XFER_STACK_LIMIT - If set to 1, transfer stack limit
    * APRUN_LABEL - If set to 1, label output with hostname and rank number

    \b
    Output Environment Variables:
    * ALPS_APP_DEPTH - CPUs per PE
    * ALPS_APP_ID - Application ID
    * ALPS_APP_PE - Rank ID
    """

    # Create a launch request from arguments
    launchreq = {
        "cmds": parse_mpmd(
            executable, args, pes, get_wdir(wdir), cpus_per_pe, pes_per_node
        ),
        "hosts": get_hostlist(
            node_list, node_list_file, exclude_node_list, exclude_node_list_file
        ),
        "ppn": pes_per_node,
        "environment": get_launch_env(environment_override),
        "cpubind": get_cpubind(cpu_binding),
        "membind": get_membind(strict_memory_containment),
        "envalias": APRUN_ENV_ALIAS,
        "abort_on_failure": abort_on_failure,
        "pmi": pmi,
        "rlimits": get_rlimits(memory_per_pe),
    }

    # Add optional settings
    if "PBS_JOBID" in os.environ:
        launchreq["jobid"] = os.environ["PBS_JOBID"]
    excl = get_exclusive(access_mode)
    if excl:
        launchreq["exclusive"] = excl
    if sync_output:
        launchreq["line_buffered"] = True
    if sstartup:
        launchreq["sstartup"] = True

    label = int(os.getenv("APRUN_LABEL", "0"))

    # Make the launch request
    app = PALSApp()
    exit_codes = app.launch(launchreq, not bypass_app_transfer, label, procinfo_file)

    # Print exit code summary (4 highest nonzero exit codes)
    exit_codes.discard(0)
    if exit_codes:
        codelist = ", ".join([str(code) for code in sorted(exit_codes)[-4:]])
        click.echo("Application %s exit codes: %s" % (app.apid, codelist))
        exit_code = max(exit_codes)
    else:
        exit_code = 0

    sys.exit(exit_code)
