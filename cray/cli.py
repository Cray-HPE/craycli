""" Cray CLI """
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import os
import sys
import re

import click

from cray.core import GeneratedCommands, option, group
from cray.config import Config, initialize_dirs, _CONFIG_DIR_NAME
from cray.utils import get_hostname
from cray.formatting import format_result
from cray.constants import NAME, DEFAULT_CONFIG
from cray.auth import AuthUsername
from cray.echo import echo, LOG_FORCE


CONTEXT_SETTING = dict(
    obj={
        'config_dir': '',
        'globals': {},
        'config': Config('', '', raise_err=False),
        'token': None,
        'auth': None
    },
    auto_envvar_prefix=NAME.upper()
)


@group(cls=GeneratedCommands,
       base_path=os.path.dirname(__file__),
       context_settings=CONTEXT_SETTING)  # pragma: NO COVER
@click.pass_context
def cli(ctx, *args, **kwargs):
    """ Cray management and workflow tool"""
    pass


@cli.command()
@click.pass_context
@option("--hostname", default=None, no_global=True,
        help='Hostname of cray system.')
@option("--no-auth", is_flag=True,
        help='Do not attempt to authenticate.')
@option("--overwrite", is_flag=True,
        help="Overwrite existing configuration if it exists")
def init(ctx, hostname, no_auth, overwrite, **kwargs):
    """ Initialize/reinitialize the Cray CLI """
    # pylint: disable=line-too-long
    config_dir = ctx.obj.get('config_dir')
    configuration = ctx.obj['globals'].get('configuration', DEFAULT_CONFIG)
    config_file_path = os.path.join(config_dir, _CONFIG_DIR_NAME, configuration)
    if os.path.isfile(config_file_path) and not overwrite:
        if not click.confirm("Overwrite configuration file at: %s ?" % config_file_path):
            raise click.UsageError(
                "Not overwriting an existing configuration. \nAlternative configurations can be specified with --configuration",
                ctx=ctx
            )

    if hostname is None:
        hostname = ctx.obj.get('config',
                               {}).get('core.hostname',
                                       click.prompt('Cray Hostname'))
    # Convert http to https
    if hostname.startswith('http:'):
        hostname = hostname.replace('http:', 'https:')
    # Add https if doesn't exist at all
    if not re.match("^http(s)?://", hostname):
        hostname = 'https://{}'.format(hostname)

    initialize_dirs(config_dir) # No error if directories already exist
    config = Config(config_dir, configuration, raise_err=False)
    config.set_deep('core.hostname', hostname)
    config.save()
    config.set_active()
    ctx.obj['config'] = config
    # Call login
    if not no_auth:
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)
        rsa_token = None
        if ctx.obj['config'].get('auth.login.rsa_required'):
            rsa_token = click.prompt('RSA Token', hide_input=True)
        echo(ctx.forward(login, hostname=hostname, username=username,
                         password=password, rsa_token=rsa_token, **kwargs), level=LOG_FORCE, ctx=ctx)
    return "Initialization complete."


@cli.group()
@click.pass_context
def auth(ctx):
    """ Manage OAuth2 credentials for the Cray CLI """
    pass

def _set_rsa_required(ctx, param, value):
    # pylint: disable=unused-argument
    rsa_required = ctx.obj['config'].get('auth.login.rsa_required')
    if not rsa_required and ctx.command.name == 'login':
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


if getattr(sys, 'frozen', False):
    version = None
    if '--version' in sys.argv:
        # Only bother opening the file if actually asking for version
        path = os.path.join(os.path.dirname(__file__), 'build_version')
        if os.path.isfile(path):
            with open(path) as v:
                version = v.read()
    click.version_option(version)(cli)
    cli(sys.argv[1:])
else:
    click.version_option()(cli)
