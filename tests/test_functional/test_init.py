""" Test the main CLI command (`cray`) and options.

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
# pylint: disable=redefined-outer-name, unused-import, invalid-name
# pylint: disable=too-many-arguments, import-error, duplicate-code
# pylint: disable=unused-argument
import os
import json
import toml

import pytest

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock
from ..utils.utils import new_configname


@pytest.mark.parametrize('cli_runner', [{'is_init': True}],
                         indirect=['cli_runner'])
def test_cray_init_no_hostname(cli_runner):
    """ Test `cray init --configuration {config}`
     for validating a new configuration is created. """
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    configname = config['configname']
    result = runner.invoke(cli, ['init', '--no-auth'],
                           input='{}\n'.format(hostname))
    assert result.exit_code == 0
    assert "Initialization complete." in result.output
    filep = '.config/cray/configurations/{}'.format(configname)
    assert os.path.isfile(filep)
    with open(filep) as f:
        data = toml.load(f)
    assert data['core']['hostname'] == hostname


@pytest.mark.parametrize('cli_runner', [{'is_init': True}],
                         indirect=['cli_runner'])
def test_cray_init(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    configname = config['configname']
    result = runner.invoke(cli, ['init', '--hostname', hostname, '--no-auth'])

    assert result.exit_code == 0
    assert "Initialization complete." in result.output
    filep = '.config/cray/configurations/{}'.format(configname)
    assert os.path.isfile(filep)
    with open(filep) as f:
        data = toml.load(f)
    assert data['core']['hostname'] == hostname


@pytest.mark.parametrize('cli_runner', [{'is_init': True}],
                         indirect=['cli_runner'])
def test_cray_init_verify_no_auth(cli_runner, rest_mock):
    """ Test `cray init` with no auth and confirm it doesn't error """
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['init', '--hostname', hostname, '--no-auth'])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['uas', 'list'])
    print(result.output)
    assert result.exit_code == 0



@pytest.mark.parametrize('cli_runner', [{'is_init': True}],
                         indirect=['cli_runner'])
def test_cray_init_w_config(cli_runner):
    """ Test `cray init --configuration {config}`
     for validating a new configuration is created. """
    runner, cli, opts = cli_runner
    config = opts['config']
    hostname = config['hostname']
    configname = config['configname']
    result = runner.invoke(cli, ['init', '--hostname', hostname, '--no-auth',
                                 '--configuration', configname])

    assert result.exit_code == 0
    assert "Initialization complete." in result.output
    filep = '.config/cray/configurations/{}'.format(configname)
    assert os.path.isfile(filep)
    with open(filep) as f:
        data = toml.load(f)
    assert data['core']['hostname'] == '{}'.format(hostname)


@pytest.mark.parametrize('cli_runner', [{'is_init': True}],
                         indirect=['cli_runner'])
def test_cray_config_no_init(cli_runner):
    """ Test `cray init --configuration {config}`
     for validating a new configuration is created. """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['config', 'list'])

    assert result.exit_code == 2
    assert 'Error: No configuration exists. Run `cray init`' in result.output


@pytest.mark.parametrize('cli_runner', [{'is_init': True}],
                         indirect=['cli_runner'])
def test_cray_config_no_init_w_config(cli_runner):
    """ Test `cray init --configuration {config}`
     for validating a new configuration is created. """
    runner, cli, _ = cli_runner
    configname = new_configname()
    result = runner.invoke(cli, ['config', 'list', '--configuration',
                                 configname])

    assert result.exit_code == 2
    err = 'Error: No configuration exists. Run `cray init --configuration {}`'
    assert err.format(configname) in result.output
