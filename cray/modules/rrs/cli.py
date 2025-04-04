#
#  MIT License
#
#  (C) Copyright [2025] Hewlett Packard Enterprise Development LP
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
""" rrs """
# pylint: disable=invalid-name
from typing import Callable, Optional, Any
import click
from cray.generator import generate

cli = generate(__file__)

def _file_cb(
    cb: Optional[Callable[[click.Context, click.Parameter, str], Any]]
) -> Callable[[click.Context, click.Parameter, click.File], Any]:
    def _cb(ctx: click.Context, param: click.Parameter, value: click.File) -> Any:
        data = value.read()
        if cb:
            return cb(ctx, param, data)
        return data
    return _cb

for p in cli.commands['criticalservices'].commands['update'].params:
    if getattr(p, 'payload_name', None) == 'from_file':
        p.type = click.File(mode='r')
        p.callback = _file_cb(p.callback)
        break
