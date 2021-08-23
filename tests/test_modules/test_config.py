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
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
import os
import json
import toml

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.utils import new_hostname, new_random_string


# pylint: disable=redefined-outer-name
def test_cray_config_describe(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['default']
    configname = config['configname']
    result = runner.invoke(cli, ['config', 'describe', '--quiet'])
    assert result.exit_code == 0
    res = json.loads(result.output)
    filep = '.config/cray/configurations/{}'.format(configname)
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data == res


# pylint: disable=redefined-outer-name
def test_cray_config_list(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['config', 'list', '--quiet'])
    assert result.exit_code == 0
    res = json.loads(result.output)
    assert res.get('configurations')
    active = [i for i in res['configurations'] if i['is_active']]
    assert len(active) == 1


# pylint: disable=redefined-outer-name
def test_cray_config_describe_format_toml(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['default']
    configname = config['configname']
    result = runner.invoke(cli, ['config', 'describe', '--format', 'toml',
                                 '--quiet'])
    assert result.exit_code == 0
    res = toml.loads(result.output)
    filep = '.config/cray/configurations/{}'.format(configname)
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data == res


# pylint: disable=redefined-outer-name
def test_cray_config_describe_w_config(cli_runner):
    """ Test `cray init` for creating the custom configuration """
    runner, cli, opts = cli_runner
    config = opts['config']
    configname = config['configname']
    result = runner.invoke(cli, ['config', 'describe', '--configuration',
                                 configname, '--quiet'])
    assert result.exit_code == 0
    res = json.loads(result.output)
    filep = '.config/cray/configurations/{}'.format(configname)
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data == res


# pylint: disable=redefined-outer-name
def test_cray_config_describe_w_bad_param(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    configname = 'somebadconfig'
    result = runner.invoke(cli, ['config', 'describe', '--configuration',
                                 configname])
    assert result.exit_code == 2
    err = 'Error: No configuration exists. Run `cray init --configuration {}`'
    assert err.format(configname) in result.output


# pylint: disable=redefined-outer-name
def test_cray_config_describe_w_missing_param(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['config', 'describe', '--configuration'])
    assert result.exit_code == 2
    assert 'Error: --configuration option requires an argument' in \
        result.output


# pylint: disable=redefined-outer-name
def test_cray_config_set_hostname(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    new_host = new_hostname()
    config = opts['default']
    configname = config['configname']
    filep = '.config/cray/configurations/{}'.format(configname)
    with open(filep, encoding='utf-8') as f:
        original_data = toml.load(f)
    result = runner.invoke(cli, ['config', 'set', 'core',
                                 'hostname={}'.format(new_host)])
    assert result.exit_code == 0
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data != original_data
    assert data['core']['hostname'] == new_host


# pylint: disable=redefined-outer-name
def test_cray_config_set_hostname_w_config(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    new_host = new_hostname()
    config = opts['config']
    configname = config['configname']
    filep = '.config/cray/configurations/{}'.format(configname)
    with open(filep, encoding='utf-8') as f:
        original_data = toml.load(f)
    result = runner.invoke(cli, ['config', 'set', 'core',
                                 'hostname={}'.format(new_host),
                                 '--configuration', configname])
    assert result.exit_code == 0
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data != original_data
    assert data['core']['hostname'] == new_host


# pylint: disable=redefined-outer-name
def test_cray_config_set_multiple(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    value1 = new_random_string()
    value2 = new_random_string()
    config = opts['default']
    configname = config['configname']
    filep = '.config/cray/configurations/{}'.format(configname)
    with open(filep, encoding='utf-8') as f:
        original_data = toml.load(f)
    result = runner.invoke(cli, ['config', 'set', 'test.deep.config',
                                 'value1={}'.format(value1),
                                 'value2={}'.format(value2)])
    assert result.exit_code == 0
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data != original_data
    assert data['test']['deep']['config'] == {'value1': value1,
                                              'value2': value2}


# pylint: disable=redefined-outer-name
def test_cray_config_set_multiple_w_config(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    value1 = new_random_string()
    value2 = new_random_string()
    config = opts['config']
    configname = config['configname']
    filep = '.config/cray/configurations/{}'.format(configname)
    with open(filep, encoding='utf-8') as f:
        original_data = toml.load(f)
    result = runner.invoke(cli, ['config', 'set', 'test.deep.config',
                                 'value1={}'.format(value1),
                                 'value2={}'.format(value2),
                                 '--configuration', configname])
    assert result.exit_code == 0
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data != original_data
    assert data['test']['deep']['config'] == {'value1': value1,
                                              'value2': value2}


# pylint: disable=redefined-outer-name
def test_cray_config_set_missing_section(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['config', 'set'])
    assert result.exit_code == 2
    assert "SECTION" in result.output
    assert 'Error: Missing argument' in result.output


# pylint: disable=redefined-outer-name
def test_cray_config_set_missing_value(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['config', 'set', 'core'])
    assert result.exit_code == 2
    assert 'Error: Missing argument' in result.output
    assert "VALUES..." in result.output


# pylint: disable=redefined-outer-name
def test_cray_config_unset(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['default']
    configname = config['configname']
    filep = '.config/cray/configurations/{}'.format(configname)
    with open(filep, encoding='utf-8') as f:
        original_data = toml.load(f)
    result = runner.invoke(cli, ['config', 'unset', 'auth.login.username'])
    assert result.exit_code == 0
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data != original_data
    assert data['auth']['login'].get('username') is None


# pylint: disable=redefined-outer-name
def test_cray_config_unset_w_config(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['config']
    configname = config['configname']
    filep = '.config/cray/configurations/{}'.format(configname)
    with open(filep, encoding='utf-8') as f:
        original_data = toml.load(f)
    result = runner.invoke(cli, ['config', 'unset', 'auth.login.username',
                                 '--configuration', configname])
    assert result.exit_code == 0
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data != original_data
    assert data['auth']['login'].get('username') is None


# pylint: disable=redefined-outer-name
def test_cray_config_unset_multiple_w_config(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['config']
    configname = config['configname']
    filep = '.config/cray/configurations/{}'.format(configname)
    with open(filep, encoding='utf-8') as f:
        original_data = toml.load(f)
    result = runner.invoke(cli, ['config', 'unset', 'auth.login.username',
                                 'core.hostname', '--configuration',
                                 configname])
    assert result.exit_code == 0
    assert os.path.isfile(filep)
    with open(filep, encoding='utf-8') as f:
        data = toml.load(f)
    assert data != original_data
    assert data['auth']['login'].get('username') is None
    assert data['core'].get('hostname') is None


# pylint: disable=redefined-outer-name
def test_cray_config_unset_missing_param(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['config', 'unset'])
    assert result.exit_code == 2
    assert 'Error: Missing argument'  in result.output
    assert "PROPERTIES" in result.output


# pylint: disable=redefined-outer-name
def test_cray_config_get_w_config(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['config']
    username = config['username']
    configname = config['configname']
    result = runner.invoke(cli, ['config', 'get', 'auth.login.username',
                                 '--configuration', configname])
    assert result.exit_code == 0
    assert username in result.output


# pylint: disable=redefined-outer-name
def test_cray_config_get(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['config', 'get', 'core.hostname'])
    assert result.exit_code == 0
    assert hostname in result.output


# pylint: disable=redefined-outer-name
def test_cray_config_get_bad(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['config', 'get', 'core.host'])
    assert result.exit_code == 2
    assert 'Error: Unable to find property.' in result.output


# pylint: disable=redefined-outer-name
def test_cray_config_get_w_config_bad(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['default']
    configname = config['configname']
    result = runner.invoke(cli, ['config', 'get', 'core.host',
                                 '--configuration', configname])
    assert result.exit_code == 2
    assert 'Error: Unable to find property.' in result.output


# pylint: disable=redefined-outer-name
def test_cray_config_get_shallow(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['config', 'get', 'core'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data == {'hostname': hostname}


# pylint: disable=redefined-outer-name
def test_cray_config_get_missing_param(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['config', 'get'])
    assert result.exit_code == 2
    assert 'Error: Missing argument' in result.output
    assert "PROPERTY" in result.output
