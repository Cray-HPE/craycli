""" Constants

MIT License

(C) Copyright 2020-2023 Hewlett Packard Enterprise Development LP

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


def _make_envvar(var):
    return '{}_{}'.format(NAME, var).upper()


# Main name of CLI
NAME = 'cray'
# Various global env vars that can be used.
CONFIG_ENVVAR = _make_envvar('CONFIG')
TOKEN_ENVVAR = _make_envvar('CREDENTIALS')
QUIET_ENVVAR = _make_envvar('QUIET')
FORMAT_ENVVAR = _make_envvar('FORMAT')
CONFIG_DIR_ENVVAR = _make_envvar('CONFIG_DIR')

# Generator constants
TAG_SPLIT = "$"
IGNORE_TAG = "cli_ignore"
HIDDEN_TAG = "cli_hidden"
DANGER_TAG = "cli_danger"
FROM_FILE_TAG = "cli_from_file"
CONVERSION_FLAG = "cray_converted"


# Config constants
DEFAULT_CONFIG = 'default'
ACTIVE_CONFIG = 'active_config'
EMPTY_CONFIG = ''
CONFIG_DIR_NAME = 'configurations'
LOG_DIR_NAME = 'logs'
AUTH_DIR_NAME = 'tokens'
