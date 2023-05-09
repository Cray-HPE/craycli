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
""" Cray CLI. """
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import os
import re
import click

from cray.auth import AuthUsername
from cray.config import _CONFIG_DIR_NAME
from cray.config import Config
from cray.config import initialize_dirs
from cray.constants import DEFAULT_CONFIG
from cray.constants import NAME
from cray.core import GeneratedCommands
from cray.core import group
from cray.core import option
from cray.echo import echo
from cray.echo import LOG_FORCE
from cray.formatting import format_result
from cray.utils import get_hostname

CONTEXT_SETTING = {
    'obj': {
        'config_dir': '',
        'globals': {},
        'config': Config('', '', raise_err=False),
        'token': None,
        'auth': None
    },
    'auto_envvar_prefix': NAME.upper(),
    'help_option_names': ['-h', '--help'],
}

CONTEXT_SETTINGS = {}

def rsa_required(config):
    """Get the value for 'auth.login.rsa_required' from the CLI
    configuration presented.  Process it as either a string or a
    boolean depending on which one is found.  If it is something else
    or not there, default to False.

    """
    rsa_req = config.get('auth.login.rsa_required', False)
    if not isinstance(rsa_req, (str, bool)):
        # Can't be sure what the user is going for by setting up a
        # non-string non-bool value here, so just go for false and be
        # done with it.
        click.echo(
            "WARNING 'auth.login.rsa_required' is present and "
            "neither a string nor a bool in the configuration, "
            "assuming false."
        )
        rsa_req = False
    if isinstance(rsa_req, str):
        rsa_req = rsa_req.lower() == "true"
    return rsa_req


@group(
    cls=GeneratedCommands,
    base_path=os.path.dirname(__file__),
    context_settings=CONTEXT_SETTING
)  # pragma: NO COVER
@click.pass_context
@click.version_option()
def cli(ctx, *args, **kwargs):
    """ Cray management and workflow tool"""
    pass


@cli.command()
@click.pass_context
@option(
    "--hostname", default=None, no_global=True,
    help='Hostname of cray system.'
)
@option(
    "--tenant", default=None, no_global=True,
    help='Tenant name to scope requests for.'
)
@option(
    "--no-auth", is_flag=True,
    help='Do not attempt to authenticate.'
)
@option(
    "--overwrite", is_flag=True,
    help="Overwrite existing configuration if it exists"
)
def init(ctx, hostname, no_auth, overwrite, tenant, **kwargs):
    """ Initialize/reinitialize the Cray CLI """
    # pylint: disable=line-too-long
    config_dir = ctx.obj.get('config_dir')
    configuration = ctx.obj['globals'].get('configuration', DEFAULT_CONFIG)
    config_file_path = os.path.join(
        config_dir,
        _CONFIG_DIR_NAME,
        configuration
    )
    if os.path.isfile(config_file_path) and not overwrite:
        if not click.confirm(
                f"Overwrite configuration file at: {config_file_path} ?"
        ):
            raise click.UsageError(
                "Not overwriting an existing configuration. \nAlternative configurations can be specified with --configuration",
                ctx=ctx
            )

    if hostname is None:
        hostname = ctx.obj.get(
            'config',
            {}
        ).get(
            'core.hostname',
            click.prompt('Cray Hostname')
        )
    # Convert http to https
    if hostname.startswith('http:'):
        hostname = hostname.replace('http:', 'https:')
    # Add https if doesn't exist at all
    if not re.match("^http(s)?://", hostname):
        hostname = f'https://{hostname}'

    if tenant is None:
        tenant = ctx.obj.get(
            'config',
            {}
        ).get(
            'core.tenant',
            click.prompt('Tenant Name (leave blank for global scope):',
                         default="",
                         type=str)
        )

    initialize_dirs(config_dir)  # No error if directories already exist
    config = Config(config_dir, configuration, raise_err=False)
    config.set_deep('core.hostname', hostname)
    config.set_deep('core.tenant', tenant)
    config.save()
    config.set_active()
    ctx.obj['config'] = config
    # Call login
    if not no_auth:
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)
        rsa_token = None
        if rsa_required(ctx.obj['config']):
            rsa_token = click.prompt('RSA Token', hide_input=True)
        echo(
            ctx.forward(
                login, hostname=hostname, username=username,
                password=password, rsa_token=rsa_token,
                tenant=tenant, **kwargs
            ), level=LOG_FORCE, ctx=ctx
        )
    return "Initialization complete."


@cli.group()
@click.pass_context
def auth(ctx):
    """ Manage OAuth2 credentials for the Cray CLI """
    pass


def _set_rsa_required(ctx, param, value):
    # pylint: disable=unused-argument
    if not rsa_required(ctx.obj['config']) and ctx.command.name == 'login':
        for p in ctx.command.params:
            if p.name == 'rsa_token':
                p.prompt = None
    return value


@auth.command()
@click.pass_context
@click.option('--username', prompt=True, callback=_set_rsa_required)
@click.option('--password', prompt=True, hide_input=True)
@click.option('--rsa_token', prompt='RSA Token', hide_input=True, default=None)
def login(ctx, username, password, rsa_token, *args, **kwargs):
    """ Authorize access the Cray System with user credentials """
    ctx.obj['config'].set_deep('auth.login.username', username)
    ctx.obj['config'].save()
    token = AuthUsername(username, get_hostname(ctx), ctx)
    echo(token.login(password, rsa_token=rsa_token), level=LOG_FORCE, ctx=ctx)


@cli.resultcallback()
@click.pass_context
def cli_cb(ctx, result, **kwargs):
    """ Global callback function. Will properly format the results """
    # Use click echo instead of our logging because we always want to echo
    # our results
    click.echo(format_result(result, ctx.obj['globals'].get('format')))
