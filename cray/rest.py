"""Functions for making REST Calls

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
# pylint: disable=fixme
import warnings

import click
import requests
from six.moves import urllib

from cray.errors import UnauthorizedError, InsecureError, BadResponseError
from cray.exceptions import InsecureRequestWarning, InsecureTransportError, \
    InvalidGrantError
from cray.utils import get_hostname
from cray.echo import echo, LOG_DEBUG, LOG_RAW


def make_url(route, url=None, default_scheme='https', ctx=None):
    """Normalize url parts and join them with a slash."""
    if url is None:
        url = get_hostname(ctx=ctx)
    if route[0] == '/':
        route = route[1:]
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
    if not scheme or scheme == '':
        scheme = default_scheme
    if (not netloc or netloc == '') and path:
        parsed = path.split('/')
        netloc = parsed[0]
        path = '/'.join(parsed[1:])
    path = urllib.parse.urljoin(path, route)
    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))


def _default_cb(response):
    """ Default callback in case the user doesn't pass one"""
    return response


def _log_request_error(err, ctx):
    echo('ERROR: {}'.format(err), ctx=ctx, level=LOG_RAW)


def request(method, route, callback=None, **kwargs):
    """ This is our REST caller. Will call endpoint and return response """
    # pylint: disable=unused-argument
    # NOTE: This has not been tested against a Shasta API Gateway.
    if callback is None:
        callback = _default_cb
    ctx = click.get_current_context()
    requester = requests
    session = None
    auth = ctx.obj['auth']
    if auth:
        session = auth.session
        if session:
            requester = session
    # TODO Get Real Certs
    kwargs.setdefault('verify', False)

    opts = {k: v for k, v in kwargs.items() if v is not None}

    try:
        url = make_url(route)
        echo('REQUEST: {} to {}'.format(method, url), ctx=ctx, level=LOG_DEBUG)
        echo('OPTIONS: {}'.format(opts), ctx=ctx, level=LOG_RAW)
        # TODO: Find solution for this.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            response = requester.request(method, url, **opts)
            if not response.ok:
                _log_request_error(response.text, ctx)
                raise BadResponseError(response, ctx=ctx)
    except InsecureTransportError as err:  # pragma: NO COVER
        _log_request_error(err, ctx)
        # pylint: disable=raise-missing-from
        raise InsecureError(ctx=ctx)
    except InvalidGrantError as err:  # pragma: NO COVER
        _log_request_error(err, ctx)
        # pylint: disable=raise-missing-from
        raise UnauthorizedError(ctx=ctx)
    except requests.exceptions.HTTPError as err:  # pragma: NO COVER
        _log_request_error(err, ctx)
        if err.response.status_code == 401:
            # pylint: disable=raise-missing-from
            raise UnauthorizedError(ctx=ctx)
        raise click.UsageError(str(err))
    except requests.exceptions.Timeout as err:  # pragma: NO COVER
        _log_request_error(err, ctx)
        raise click.UsageError('Timed out trying to connect to cray', ctx=ctx)
    except click.ClickException:
        # Don't log click specific exceptions
        raise
    except Exception as err:
        _log_request_error(err, ctx)
        raise click.UsageError('Unable to connect to cray. Please verify' +
                               ' your cray hostname:\n\n\t' +
                               'cray config get core.hostname\n\t' +
                               'cray config set core hostname=cray_hostname')

    return callback(response)
