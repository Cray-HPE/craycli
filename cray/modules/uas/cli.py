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
""" Cray User Access Manager """
# pylint: disable=invalid-name
import click

from cray.generator import generate

cli = generate(__file__)


def _check_for_private_key(existing_callback):
    """Returns a function that ensures a private key will not hit the wire."""

    def _callback(ctx, param, value):
        cb_data = existing_callback(ctx, param, value)

        # NOTE: This unfortunately means the file is opened twice, once here
        #       and again in cray.generate._parse_data.
        with open(cb_data["value"], "rb") as f:
            pubkey = f.read()

        if b"PRIVATE KEY" in pubkey:
            raise click.UsageError(
                "Please specify a properly formatted public key. It "
                "appears that you are trying to use your private key."
            )

        return cb_data

    return _callback


cmd = cli.commands["create"]
for p in cmd.params:
    if p.name == "publickey":
        p.callback = _check_for_private_key(p.callback)
        break
