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
""" ims """

# pylint: disable=invalid-name
import click

from cray.generator import generate

CURRENT_VERSION = 'v3'
SWAGGER_OPTS = {
    'vocabulary': {
        'deleteall': 'deleteall'
    }
}

cli = generate(__file__, condense=False, swagger_opts=SWAGGER_OPTS)
version = cli.commands["version"]
cli.commands = cli.commands[CURRENT_VERSION].commands
cli.commands["version"] = version


def _file_cb(cb):

    def _cb(ctx, param, value):
        data = value.read()
        if cb:
            return cb(ctx, param, data)
        return data

    return _cb


for p in cli.commands['public-keys'].commands['create'].params:
    if p.payload_name == 'public_key':
        p.type = click.File(mode='r')
        p.callback = _file_cb(p.callback)
        break
