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
""" Auth related methods. """
import json
import os
import warnings
import click
# pylint: disable=fixme
########################################
# NOTE: This is still very much beta
# TODO: Better handle/solidify token uri
# TODO: Don't assume client_id
# TODO: Get valid SSL Certs
# TODO: Switch to browser auth code flow
########################################
from oauthlib.oauth2 import InvalidGrantError
from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2 import MissingTokenError
from oauthlib.oauth2 import UnauthorizedClientError
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
from requests_oauthlib import OAuth2Session
from urllib3.exceptions import InsecureRequestWarning

from cray.constants import AUTH_DIR_NAME
from cray.echo import echo
from cray.echo import LOG_RAW
from cray.rest import make_url
from cray.utils import hostname_to_name
from cray.utils import open_atomic


class Auth(object):  # pylint: disable=too-many-instance-attributes
    """ Auth Class used for generating, refreshing, and saving OAuth Tokens """

    TOKEN_URI = '/keycloak/realms/{}/protocol/openid-connect/token'

    def __init__(self, hostname, path, username=None, name=None, **kwargs):
        ctx = kwargs.get('ctx', click.get_current_context())
        if name is None and username is None:
            raise click.UsageError("Username or Token File required.")

        self.domain = hostname_to_name(hostname=hostname, ctx=ctx)
        if name is None:
            self.set_name(username)
        else:
            self.name = name

        self.tenant = kwargs.get('tenant', 'shasta')
        self.username = username
        self.ctx = ctx
        self.url = make_url(self.TOKEN_URI.format(self.tenant), hostname)
        self.path = path
        self.client_id = kwargs.get('client_id', 'cray')
        self._token_path = os.path.join(self.path, self.name)
        self.session = None

    def get_session_opts(self):
        """ Set the session options to pass when getting tokens """
        return {
            'token_updater': self.save,
            'auto_refresh_url': self.url,
            'auto_refresh_kwargs': {
                'client_id': self.client_id
            }
        }

    def set_name(self, name):
        """ Convert name parameter to format ready for saving """
        self.name = f'{self.domain}.{name.replace(".", "_")}'
        return self.name

    def get_session(self, token=None):
        """ Set the OAuth Session """
        opts = self.get_session_opts()
        client = LegacyApplicationClient(
            client_id=self.client_id,
            token=token
        )
        if token:
            client.parse_request_body_response(json.dumps(token))

        return OAuth2Session(client=client, token=token, **opts)

    def save(self, token):
        """ Save token to file """
        if 'client_id' not in token:
            token['client_id'] = self.client_id
        with open_atomic(self._token_path) as token_file:
            json.dump(token, token_file)
        echo(
            f'Saved token: {self._token_path}',
            ctx=self.ctx,
            level=LOG_RAW
        )

    def load(self, name=None):
        """ Load token file """
        if name:
            self.set_name(name)
        token = {}
        if os.path.isfile(self._token_path):
            with open(self._token_path, encoding='utf-8') as token_file:
                token = json.load(token_file)
            echo(
                f'Loaded token: {self._token_path}',
                ctx=self.ctx,
                level=LOG_RAW
            )
        if 'client_id' in token:
            self.client_id = token['client_id']
        self.session = self.get_session(token=token)
        return token

    def get_token(self, **kwargs):
        """ Fetch a new token """
        token = kwargs.get('token')
        if 'token' not in kwargs and 'client_id' not in kwargs:
            kwargs['client_id'] = self.client_id
        self.session = self.get_session(token=token)
        try:
            # TODO Remove when have valid certs
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    category=InsecureRequestWarning
                )
                opts = {
                    'verify': False  # TODO: Enable
                }
                opts.update(self.get_session_opts())
                opts.update(kwargs)
                token = self.session.fetch_token(token_url=self.url, **opts)
        except (
                MissingTokenError, UnauthorizedClientError,
                InvalidGrantError) as e:
            echo(f'AUTH ERROR: {e}', ctx=self.ctx, level=LOG_RAW)
            raise click.UsageError('Invalid Credentials', ctx=self.ctx)
        except CustomOAuth2Error as e:
            echo(f'AUTH ERROR: {e}', ctx=self.ctx, level=LOG_RAW)
            raise click.UsageError(e.description, ctx=self.ctx)
        except Exception as e:
            echo(f'AUTH ERROR: {e}', ctx=self.ctx, level=LOG_RAW)
            raise click.UsageError('Unable to login!')
        return token

    def login(self, password, username=None, rsa_token=None, **kwargs):
        """ Login to generate a new token """
        if username:  # pragma: NO COVER
            self.username = username
            self.set_name(username)
        if rsa_token:
            kwargs['rsa_username'] = self.username
            kwargs['rsa_otp'] = rsa_token
        token = self.get_token(
            username=self.username,
            password=password,
            **kwargs
        )
        if token:
            self.save(token)
        if self.session.authorized:
            return 'Success!'
        return 'Credentials failed!'


class AuthFile(Auth):
    """ Auth Class for existing token files """

    def __init__(self, token_path, hostname, **kwargs):
        path = os.path.dirname(token_path)
        name = os.path.basename(token_path)
        try:
            with open(token_path, encoding='utf-8') as token_file:
                token = json.load(token_file)
        except Exception as e:
            echo(
                f'AUTH ERROR: {e}',
                ctx=kwargs.get('ctx'),
                level=LOG_RAW
            )
            raise click.UsageError(
                'Unable to open token file, is it valid JSON?'
            )
        Auth.__init__(
            self, hostname, path, name=name,
            client_id=token.get('client_id'), **kwargs
        )


class AuthUsername(Auth):
    """ Auth Class when username/password provided """

    def __init__(self, username, hostname, ctx, **kwargs):
        path = os.path.join(ctx.obj['config_dir'], AUTH_DIR_NAME)
        Auth.__init__(self, hostname, path, username=username, ctx=ctx)
