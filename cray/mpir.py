"""
mpir.py - MPIR attach implementation

MIT License

(C) Copyright [2020] Hewlett Packard Enterprise Development LP

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

import os
import ctypes

from cray.echo import echo, LOG_INFO, LOG_WARN, LOG_DEBUG, LOG_RAW

def get_libmpirattach_path():
    """ If set, read the palsd install location from the environment """
    palsd_install_dir = os.getenv("PALSD_INSTALL_DIR")
    if palsd_install_dir is None:
        palsd_install_dir = "/usr/lib64"

    return palsd_install_dir + "/libmpirattach.so.0"

# pylint: disable=invalid-name
libMpirAttach = None

def init_libMpirAttach_functions():
    """ Try to load the MPIR attach functions from the dynamic library """
    global libMpirAttach # pylint: disable=global-statement

    # pylint: disable=bare-except
    try:
        libMpirAttach_path = get_libmpirattach_path()
        echo("Loading libMpirAttach from %s" % libMpirAttach_path, level=LOG_INFO)
        libMpirAttach = ctypes.CDLL(libMpirAttach_path)

        libMpirAttach.MPIR_Breakpoint.restype = None
        libMpirAttach.MPIR_Breakpoint.argtypes = []

        libMpirAttach.get_MPIR_being_debugged.restype = ctypes.c_int
        libMpirAttach.get_MPIR_being_debugged.argtypes = []

        libMpirAttach.free_MPIR_proctable.restype = ctypes.c_int
        libMpirAttach.free_MPIR_proctable.argtypes = []

        libMpirAttach.allocate_MPIR_proctable.restype = ctypes.c_int
        libMpirAttach.allocate_MPIR_proctable.argtypes = [
            ctypes.c_int, # proctable_size
            ctypes.POINTER(ctypes.c_char_p), # hostname list
            ctypes.c_int, # hostname list size
            ctypes.POINTER(ctypes.c_char_p), # executable list
            ctypes.c_int # executable list size
        ]

        libMpirAttach.finalize_MPIR_proctable.restype = ctypes.c_int
        libMpirAttach.finalize_MPIR_proctable.argtypes = [
            ctypes.c_int # proctable_size
        ]

        libMpirAttach.set_MPIR_debug_state.restype = ctypes.c_int
        libMpirAttach.set_MPIR_debug_state.argtypes = [
            ctypes.c_int # debug_state
        ]

        libMpirAttach.set_MPIR_proctable_elem.restype = ctypes.c_int
        libMpirAttach.set_MPIR_proctable_elem.argtypes = [
            ctypes.c_int, # idx
            ctypes.c_int, # host_name idx
            ctypes.c_int, # executable_name idx
            ctypes.c_ulong, # pid
        ]

        libMpirAttach.set_current_apid.restype = ctypes.c_int
        libMpirAttach.set_current_apid.argtypes = [
            ctypes.c_char_p, # current_apid
        ]

    except:
        echo("Failed to load library from %s. \
            Try setting PALSD_INSTALL_DIR to the directory where libMpirAttach.so is located."
            % libMpirAttach_path, level=LOG_WARN)
        libMpirAttach = None


def get_MPIR_being_debugged():
    """ Get C variable MPIR_being_debugged """

    # Load MPIR initialization functions from shared library
    if libMpirAttach is None:
        init_libMpirAttach_functions()
        if libMpirAttach is None:
            return False

    return bool(libMpirAttach.get_MPIR_being_debugged())


def MPIR_proctable_filled():
    """ Determine if proctable is already filled in """

    # Load MPIR initialization functions from shared library
    if libMpirAttach is None:
        init_libMpirAttach_functions()
        if libMpirAttach is None:
            return True

    return bool(libMpirAttach.get_MPIR_proctable_size() > 0)


def fill_MPIR_proctable(proctable_elems):
    """ Use proctable element array to fill C MPIR_proctable """
    # pylint: disable=too-many-locals,too-many-branches

    # Load MPIR initialization functions from shared library
    if libMpirAttach is None:
        init_libMpirAttach_functions()
        if libMpirAttach is None:
            return

    if not proctable_elems:
        raise Exception("proctable is empty")

    hostnames = []
    hostname_indices = {}

    executables = []
    executable_indices = {}

    for (hostname, executable, pid) in proctable_elems:
        if hostname not in hostnames:
            hostname_indices[hostname] = len(hostnames)
            hostnames.append(hostname)
        if executable not in executables:
            executable_indices[executable] = len(executables)
            executables.append(executable)

    hostname_cstr_arr = (ctypes.c_char_p * (len(hostnames) + 1))()
    hostname_cstr_storage = [
        ctypes.create_string_buffer(host.encode('utf-8')) for host in hostnames
    ]
    for (i, host_cstr) in enumerate(hostname_cstr_storage):
        hostname_cstr_arr[i] = ctypes.cast(host_cstr, ctypes.c_char_p)
    hostname_cstr_arr[len(hostname_cstr_storage)] = None

    executable_cstr_arr = (ctypes.c_char_p * (len(executables) + 1))()
    executable_cstr_storage = [
        ctypes.create_string_buffer(exe.encode('utf-8')) for exe in executables
    ]
    for (i, exe_cstr) in enumerate(executable_cstr_storage):
        executable_cstr_arr[i] = ctypes.cast(exe_cstr, ctypes.c_char_p)
    executable_cstr_arr[len(executable_cstr_storage)] = None

    if libMpirAttach.allocate_MPIR_proctable(len(proctable_elems),
                                             hostname_cstr_arr, len(hostnames),
                                             executable_cstr_arr, len(executables)):
        raise Exception("failed: allocate_MPIR_proctable")

    for (idx, (hostname, executable, pid)) in enumerate(proctable_elems):
        if libMpirAttach.set_MPIR_proctable_elem(
                idx,
                hostname_indices[hostname],
                executable_indices[executable],
                pid
        ):
            raise Exception("failed: set_MPIR_proctable_elem")

    if libMpirAttach.finalize_MPIR_proctable(len(proctable_elems)):
        raise Exception("failed: finalize_MPIR_proctable")

    # Set debug state to spawned / proctable filled
    if libMpirAttach.set_MPIR_debug_state(1):
        raise Exception("failed: set_MPIR_debug_state")


def set_current_apid(apid):
    """ Make currently-running apid available to debugger client """

    # Load MPIR initialization functions from shared library
    if libMpirAttach is None:
        init_libMpirAttach_functions()
        if libMpirAttach is None:
            return

    apid_cstr = ctypes.create_string_buffer(apid.encode('utf-8'))
    if libMpirAttach.set_current_apid(apid_cstr):
        raise Exception("failed: set_current_apid")


def call_MPIR_Breakpoint():
    """ Notify MPIR client that proctable is completed """

    # Load MPIR initialization functions from shared library
    if libMpirAttach is None:
        init_libMpirAttach_functions()
        if libMpirAttach is None:
            return

    libMpirAttach.MPIR_Breakpoint()


def free_MPIR_proctable():
    """ Free the C data structures allocated by the MPIR library """

    # Load MPIR initialization functions from shared library
    if libMpirAttach is None:
        init_libMpirAttach_functions()
        if libMpirAttach is None:
            return

    if libMpirAttach.free_MPIR_proctable():
        raise Exception("failed: free_MPIR_proctable")
