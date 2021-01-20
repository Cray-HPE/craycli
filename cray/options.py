""" Common options available for commands

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
# pylint: disable=invalid-name
import os

import click

from cray.constants import CONFIG_ENVVAR, QUIET_ENVVAR, FORMAT_ENVVAR, \
                       TOKEN_ENVVAR, CONFIG_DIR_ENVVAR, NAME, ACTIVE_CONFIG, \
                       DEFAULT_CONFIG, EMPTY_CONFIG
from cray.config import Config
from cray.auth import AuthFile, AuthUsername
from cray.utils import get_hostname


def _has_changed(ctx, param, value):
    return param.name not in ctx.obj['globals'] or param.default != value


def _set_config(ctx, param, value):
    ignored_commands = ['init']
    command_name = ctx.command.name
    base_dir = os.environ.get(CONFIG_DIR_ENVVAR, os.path.expanduser("~"))
    config_dir = os.path.join(base_dir, '.config', NAME)

    ctx.obj['config_dir'] = config_dir
    if _has_changed(ctx, param, value) and value is not None:
        active_config_path = os.path.join(config_dir, ACTIVE_CONFIG)
        active_config = DEFAULT_CONFIG
        if os.path.isfile(active_config_path):
            with open(active_config_path) as active_config_fp:
                active_config = active_config_fp.read()
        ctx.obj['globals']['active_config'] = active_config
        # If user hasn't passed in configuration, use active
        if value == EMPTY_CONFIG:
            value = active_config
        ctx.obj['globals'][param.name] = value
        if command_name not in ignored_commands:
            ctx.obj['config'] = Config(config_dir, value)
        else:
            ctx.obj['config'] = Config(config_dir, '', False)
    if ctx.obj['config'] == {} and command_name not in ['init']:
        opt = ''
        if value != DEFAULT_CONFIG:
            opt = " --configuration {}".format(value)
        msg = "No configuration exists. Run `cray init{}`".format(opt)
        raise click.UsageError(msg)
    return ctx.obj['globals'][param.name]


def _set_global(ctx, param, value):
    if _has_changed(ctx, param, value):
        ctx.obj['globals'][param.name] = value
    return ctx.obj['globals'][param.name]


def _set_token(ctx, param, value):
    # pylint: disable=unused-argument
    token = ctx.obj['globals'].get(param.name)
    if ctx.info_name != 'init' and _has_changed(ctx, param, value):
        hostname = get_hostname(ctx)
        auth = None
        if value:
            auth = AuthFile(value, hostname, ctx=ctx)
        else:
            username = ctx.obj['config'].get('auth.login.username')
            if username:
                auth = AuthUsername(username, hostname, ctx=ctx)
        ctx.obj['auth'] = auth
        if auth:
            token = auth.load()
    ctx.obj['globals'][param.name] = token
    return token


def global_options(f):
    """ Set of global options that should be added to every command """
    # pylint: disable=cyclic-import,import-outside-toplevel
    from .core import option
    opts = {'expose_value': False}
    f = option('--configuration', show_envvar=True, envvar=CONFIG_ENVVAR,
               metavar='CONFIG', default=EMPTY_CONFIG, callback=_set_config,
               required=True, is_eager=True,
               help="name of configuration to use. Create through `cray init`", **opts)(f)
    f = option('--quiet', is_flag=True, callback=_set_global,
               envvar=QUIET_ENVVAR, **opts)(f)
    f = option('--format', default='toml', type=click.Choice(['json', 'toml', 'yaml']),
               envvar=FORMAT_ENVVAR, callback=_set_global, **opts)(f)
    f = option("--token", metavar='TOKEN_FILE_PATH', callback=_set_token,
               envvar=TOKEN_ENVVAR, show_envvar=True, **opts)(f)
    f = option('-v', '--verbose', count=True, help="Example: -vvvv",
               callback=_set_global, default=0, is_eager=True, **opts)(f)
    return f
