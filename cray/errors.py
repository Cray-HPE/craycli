""" Error classes """
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
