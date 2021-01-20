""" Error classes

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
from click import UsageError


_UNAUTHORIZED = """Your session has expired, please run:
\t`cray auth login`
or pass --token with your authorization token"""


class UnauthorizedError(UsageError):
    """ Error authenticating """

    def __init__(self, ctx=None):
        message = _UNAUTHORIZED
        cmd = '.'
        if ctx:  # pragma: NO COVER
            cmd = ":\n\t`{} --token ./my_token`".format(ctx.command_path)
        message = "{}{}".format(_UNAUTHORIZED, cmd)
        UsageError.__init__(self, message, ctx=ctx)


class InsecureError(UsageError):
    """ Error authenticating """

    def __init__(self, ctx=None):
        message = "You've configured your cray hostname with http. " + \
            "Please reconfigure for https."
        UsageError.__init__(self, message, ctx=ctx)


class BadResponseError(UsageError):
    """ HTTP Response Error """

    _DEFAULT = "Error received from server: {} {}"

    def __init__(self, response, ctx=None):
        message = self._DEFAULT.format(response.status_code, response.reason)
        try:
            data = response.json()
            # RFC 7807 style error message
            # https://tools.ietf.org/html/rfc7807
            if 'title' in data and 'detail' in data:
                message = '{}: {}'.format(data['title'], data['detail'])
            # CAPMC style error message
            if 'e' in data and 'err_msg' in data:
                message = '{}: {}'.format(message, data['err_msg'])
        except:  # pylint: disable=bare-except
            pass
        UsageError.__init__(self, message, ctx=ctx)
