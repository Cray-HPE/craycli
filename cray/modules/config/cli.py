""" Configuration commands """

import os

import click

from cray.core import group, argument, pass_context
from cray.config import Config
from cray.utils import delete_keys_from_dict, merge_dict
from cray.constants import DEFAULT_CONFIG
from cray.echo import echo, LOG_FORCE


def _print_active(config):
    return 'Your active configuration is: {}'.format(config)


@group()  # Name for main group is inferred from the directory name.
def cli():
    """ View and edit Cray configuration properties """
    pass


@cli.command(name='use')
@argument('config', metavar='CONFIGURATION')
@pass_context
def config_activate(ctx, config):
    """Activate a configuration. This sets the default configuration to use."""
    # Load config to make sure it exists.
    Config(ctx.obj['config_dir'], config, True)
    ctx.obj['config'].set_active(config)
    return _print_active(config)


@cli.command(name='list')
@pass_context
def config_list(ctx):
    """ List all your configurations. """
    path = ctx.obj['config'].get_configurations_dir()
    config_files = os.listdir(path)
    active_config = ctx.obj['globals'].get('active_config', DEFAULT_CONFIG)
    configs = []
    for config_file in config_files:
        configs.append({
            'name': config_file,
            'is_active': (config_file == active_config)
            })
    return {'configurations': configs}


@cli.command(name='describe')
@pass_context
def config_describe(ctx):
    """ List current configuration values. """
    configuration = ctx.obj['globals'].get('configuration')
    active_config = ctx.obj['globals']['active_config']

    echo(_print_active(active_config), level=LOG_FORCE, ctx=ctx)
    if configuration != active_config:
        echo('Describing configuration: {}'.format(configuration),
             level=LOG_FORCE, ctx=ctx)
    return Config(ctx.obj['config_dir'], configuration, True)


@cli.command(name='get')
@pass_context
@argument('prop', metavar='PROPERTY')
def config_get(ctx, prop):
    """ Get a specific property. \n
    This should be a deep reach of the section/value. For example to get
    the username value: \n
    `cray config get auth.login.username` """
    configuration = ctx.obj['globals'].get('configuration')
    config = Config(ctx.obj['config_dir'], configuration, True)
    try:
        keys = prop.split('.')
        data = config[keys.pop(0)]
        while keys:
            data = data[keys.pop(0)]
    except Exception:
        raise click.UsageError("Unable to find property.")
    return data


@cli.command(name='set')
@pass_context
@argument('section', required=True)
@argument('values', nargs=-1, required=True)
def config_set(ctx, section, values):
    """ Set configuration parameters.\n
    Example: `cray config set cmd.subcmd foo=bar bars=foos` \n
    To update login user:
     `cray config set auth.login username=janedoe`"""
    configuration = ctx.obj['globals'].get('configuration')
    config = Config(ctx.obj['config_dir'], configuration, True)
    try:
        data = {v[0]: v[1] for v in [value.split('=') for value in values]}
        keys = section.split('.')[::-1]
        while keys:
            data = {keys.pop(0): data}

        merge_dict(config, data).save()
    except Exception:
        raise click.UsageError("Unable to set property.")


@cli.command(name='unset')
@pass_context
@argument('props', metavar='PROPERTIES', nargs=-1, required=True)
def config_unset(ctx, props):
    """ Unset configuration parameters. \n
    Example: `cray config unset cmd.subcmd.foo`
    """
    configuration = ctx.obj['globals'].get('configuration')
    config = Config(ctx.obj['config_dir'], configuration, True)
    for prop in props:
        try:
            keys = prop.split('.')
            delete_keys_from_dict(config, keys)
            config.save()
        except Exception:
            raise click.UsageError("Unable to unset property.")
