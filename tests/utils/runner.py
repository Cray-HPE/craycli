""" Test fixtures that make testing easier.

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
