"""
atp.py - ATP launch functions used in PALSApp launch implementation
Copyright 2020 Cray Inc. All Rights Reserved.
"""

import os
import ctypes

def get_libatppalslaunch_path():
    """ If enabled, read the ATP install location from the environment (set by ATP module) """
    if os.getenv("ATP_ENABLED") == "0":
        return None

    atp_install_dir = os.getenv("ATP_INSTALL_DIR")
    if atp_install_dir is None:
        return None

    return atp_install_dir + "/pals/libAtpPalsLaunch.so"

# pylint: disable=invalid-name
libAtpPalsLaunch = None

def init_libatppalslaunch_functions():
    """ Try to load the ATP launcher functions from the dynamic library """
    global libAtpPalsLaunch # pylint: disable=global-statement

    # Try to open the dynamic PALS ATP launcher library from the currently-enabled ATP
    libAtpPalsLaunch_path = get_libatppalslaunch_path()
    if libAtpPalsLaunch_path:
        # pylint: disable=bare-except
        try:
            libAtpPalsLaunch = ctypes.CDLL(libAtpPalsLaunch_path)
        except:
            pass
    else:
        return

    # pylint: disable=bare-except
    try:
        # Determines if the ATP signal handler library needs to be preloaded
        # for the current user binary
        libAtpPalsLaunch.should_preload_atp.restype = ctypes.c_int
        libAtpPalsLaunch.should_preload_atp.argtypes = [
            ctypes.c_char_p, ctypes.c_size_t, # LD_PRELOAD
            ctypes.c_char_p # binary path
        ]

        # Performs the setup and execution of the ATP frontend binary.
        # Listener socket information will be sent back and set in the job environment
        libAtpPalsLaunch.launch_atp_frontend.restype = ctypes.c_void_p
        libAtpPalsLaunch.launch_atp_frontend.argtypes = [
            ctypes.c_char_p, ctypes.c_size_t, # ATP_SOCKET_ADDRESS
            ctypes.c_char_p, ctypes.c_size_t, # ATP_SOCKET_PORT
            ctypes.c_char_p, ctypes.c_size_t, # ATP_SHM_KEY
            ctypes.POINTER(ctypes.c_char_p) # null-terminated binary path list
        ]

        # After the job launch has started, and an application ID is assigned,
        # communicate the apid to the ATP frontend
        libAtpPalsLaunch.send_attach_data.restype = ctypes.c_int
        libAtpPalsLaunch.send_attach_data.argtypes = [
            ctypes.c_void_p, # frontend handle
            ctypes.c_char_p, # application ID
            ctypes.c_size_t # length of application ID including null pointer
        ]

        # If an error is encountered during launch, this function can be used to
        # terminate the running ATP frontend
        libAtpPalsLaunch.terminate_frontend.restype = ctypes.c_int
        libAtpPalsLaunch.terminate_frontend.argtypes = [
            ctypes.c_void_p # frontend handle
        ]
    except:
        libAtpPalsLaunch = None


def launch_atp_frontend(executables):
    """ Fork / exec ATP frontend, return handle to send launched apid later and environment list """
    global libAtpPalsLaunch # pylint: disable=global-statement

    # Load ATP initialization functions from shared library
    init_libatppalslaunch_functions()

    if libAtpPalsLaunch is None:
        return (None, [])

    result = []

    # Determine if the user binary should have the ATP signal handler library preloaded
    ld_preload = ctypes.create_string_buffer(128)
    for executable in executables:
        should_preload_atp_rc = libAtpPalsLaunch.should_preload_atp(
            ld_preload, ctypes.sizeof(ld_preload),
            ctypes.create_string_buffer(executable.encode('utf-8'))
        )
        # Check error code
        if should_preload_atp_rc < 0:
            print("should_preload_atp failed")
            return (None, [])
        if should_preload_atp_rc:
            # Add LD_PRELOAD value to the job's environment
            result.append("LD_PRELOAD=%s" % ld_preload.value.decode('utf-8'))
            break

    # Create ATP socket connection info buffers
    atp_socket_address = ctypes.create_string_buffer(128)
    atp_socket_port = ctypes.create_string_buffer(16)
    atp_shm_key = ctypes.create_string_buffer(128)

    # Create executable list
    executable_cstr_arr = (ctypes.c_char_p * (len(executables) + 1))()
    executable_cstr_storage = [
        ctypes.create_string_buffer(exe.encode('utf-8')) for exe in executables
    ]
    for (i, exe_cstr) in enumerate(executable_cstr_storage):
        executable_cstr_arr[i] = ctypes.cast(exe_cstr, ctypes.c_char_p)
    executable_cstr_arr[len(executable_cstr_storage)] = None

    # Launch ATP frontend and fill in connection info buffers
    frontend_handle = libAtpPalsLaunch.launch_atp_frontend(
        atp_socket_address, ctypes.sizeof(atp_socket_address),
        atp_socket_port, ctypes.sizeof(atp_socket_port),
        atp_shm_key, ctypes.sizeof(atp_shm_key),
        executable_cstr_arr
    )

    # Check error condition
    if not frontend_handle:
        print("launch_atp_frontend failed")
        return (None, [])

    # Add frontend connection information to the job's environment
    result.append("ATP_SOCKET_ADDRESS=%s" % atp_socket_address.value.decode('utf-8'))
    result.append("ATP_SOCKET_PORT=%s" % atp_socket_port.value.decode('utf-8'))
    result.append("ATP_SHM_KEY=%s" % atp_shm_key.value.decode('utf-8'))

    # Copy any signal handler-specific environment variables into the job environment
    atp_ignore_sigterm = os.getenv("ATP_IGNORE_SIGTERM")
    if atp_ignore_sigterm:
        result.append("ATP_IGNORE_SIGTERM=%s" % atp_ignore_sigterm)

    return (frontend_handle, result)


def terminate_frontend(frontend_handle):
    """ Terminate the ATP frontend using the handle. Used for error cases """
    global libAtpPalsLaunch # pylint: disable=global-statement

    if libAtpPalsLaunch is None:
        return

    libAtpPalsLaunch.terminate_frontend(frontend_handle)


def send_launched_apid(frontend_handle, apid):
    """ Send the launched apid to the frontend using the handle. This cleans up the handle """
    global libAtpPalsLaunch # pylint: disable=global-statement

    if libAtpPalsLaunch is None:
        return

    # Create the application ID buffer
    attach_data = ctypes.create_string_buffer(apid.encode('utf-8'))

    # Send launched application ID to the running frontend
    send_application_id_rc = libAtpPalsLaunch.send_attach_data(
        frontend_handle,
        attach_data, ctypes.sizeof(attach_data))

    if send_application_id_rc < 0:
        print("send_application_id failed")
        libAtpPalsLaunch.terminate_frontend(frontend_handle)
        return
