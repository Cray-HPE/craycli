#
#  MIT License
#
#  (C) Copyright 2020-2024 Hewlett Packard Enterprise Development LP
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
from cray.generator import generate
import click 

# def print_response(resp):
#     # Intercept the response by printing it.
#     print(resp)
#     print("I am printing")
#     click.echo(resp)
#     click.echo("I am using click to echo")
#     # Return the response unchanged (or modify if needed).
#     return resp

def _rrs_format_response(cb):

    def _cb(ctx, param, value):
        data = value.read()
        print(data)
        print("I am printing")
        click.echo(data)
        click.echo("I am using click to echo")
        if cb:
            return cb(ctx, param, data)
        return data

    return _cb


# Pass the callback to generate
cli = generate(__file__, callback=_rrs_format_response)
