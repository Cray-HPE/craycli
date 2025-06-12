#
#  MIT License
#
#  (C) Copyright 2025 Hewlett Packard Enterprise Development LP
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
"""rrs"""
# pylint: disable=invalid-name
import json

from cray.constants import FROM_FILE_TAG
from cray.core import option
from cray.generator import _opt_callback
from cray.generator import generate

# Generates a Click CLI from the current file
cli = generate(__file__)


def create_templates_critical_services(func):
    """ Callback function to custom create our own payload for critical services """

    def _decorator(from_file, **kwargs):
        if not from_file.get('value'):
            return func(**kwargs)
        with open(from_file["value"], 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        payload = data
        # Hack to tell the CLI we are passing our own payload; don't generate
        kwargs[FROM_FILE_TAG] = {"value": payload, "name": FROM_FILE_TAG}
        return func(**kwargs)

    return _decorator


def setup_critical_services_from_file(command):
    """ Adds a --from-file parameter for critical services update """
    option(
        '--from-file', callback=_opt_callback, type=str, default='', metavar='TEXT',
        help="A file containing the JSON for critical services configuration"
    )(command)
    params = [command.params[-1]]
    for param in command.params[:-1]:
        if not getattr(param, 'help', None) or 'DEPRECATED' not in param.help:
            params.append(param)
    command.params = params
    command.callback = create_templates_critical_services(command.callback)


# Setup the file-based critical services update
setup_critical_services_from_file(
    cli.commands['criticalservices'].commands['update']
)
