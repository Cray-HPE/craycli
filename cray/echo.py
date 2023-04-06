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
""" Handles logging for the CLI. """
import click

# Logging levels
# Note, there is purposely no ERROR level, if an actual error occurs an
# exception should be raise from the exceptions library provided. If you
# do not think it merits an exception than it is not an error.
LOG_FORCE = 0  # Generally avoided, used by the config module
LOG_WARN = 0
LOG_INFO = 1
LOG_DEBUG = 2
LOG_RAW = 3  # Ultra verbose


# Custom utils
def echo(*args, **kwargs):
    """ Logging to console and files """
    default_verbose = 0
    default_is_quiet = False
    try:
        ctx = kwargs.get('ctx', click.get_current_context())
        verbosity = ctx.obj['globals'].get('verbose', default_verbose)
        is_quiet = ctx.obj['globals'].get('quiet', default_is_quiet)
    except RuntimeError:
        # This is mostly a workaround for unit tests.
        verbosity = default_verbose
        is_quiet = default_is_quiet

    if 'ctx' in kwargs:
        del kwargs['ctx']
    level = kwargs.get('level', 2)
    if 'level' in kwargs:
        del kwargs['level']
    to_log = (level <= verbosity)

    if not is_quiet and to_log:
        click.echo(*args, **kwargs)
