""" Test fixtures that make testing easier."""
# pylint: disable=missing-docstring, redefined-outer-name, import-error
import os
try:
    from importlib import reload  # pylint: disable=redefined-builtin
except ImportError:
    pass

from click.testing import CliRunner
import pytest

from cray.constants import CONFIG_DIR_ENVVAR, CONFIG_ENVVAR
from cray import cli
from cray.config import initialize_dirs

from .utils import new_username, new_configname, new_hostname, \
    create_config_file


@pytest.fixture()
def cli_runner(request):
    """
    Create cli runner within isolated filesystem.
    """
    # pylint: disable=broad-except
    # Reload the cli module so we are truely starting over each for each test.
    reload(cli)

    params = getattr(request, 'param', {})
    is_init = params.get('is_init')
    default = {
        'configname': 'default',
        'username': new_username(),
        'hostname': new_hostname()
    }
    config = {
        'configname': new_configname(),
        'username': new_username(),
        'hostname': new_hostname()
    }
    opts = {
        'default': default,
        'config': config
    }
    cli_runner = CliRunner()
    old_env = {}
    old_env[CONFIG_DIR_ENVVAR] = os.environ.get(CONFIG_DIR_ENVVAR)
    old_env[CONFIG_ENVVAR] = os.environ.get(CONFIG_ENVVAR)
    with cli_runner.isolated_filesystem():
        os.environ[CONFIG_DIR_ENVVAR] = os.getcwd()
        os.environ['CRAY_FORMAT'] = 'json'
        try:
            del os.environ[CONFIG_ENVVAR]
        except Exception:
            pass
        if not is_init:
            initialize_dirs(os.path.join(os.getcwd(), '.config/cray/'))
            create_config_file(default['configname'], default['hostname'],
                               default['username'])
            create_config_file(config['configname'], config['hostname'],
                               config['username'])

        yield cli_runner, cli.cli, opts
        # Cleanup
        for key, value in old_env.items():
            if value is None:
                try:
                    del os.environ[key]
                except Exception:
                    pass
            else:
                os.environ[key] = value
