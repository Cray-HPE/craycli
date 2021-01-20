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
# pylint: disable=too-many-arguments, unused-argument
# pylint: disable=too-many-lines
import json

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name
def test_cray_capmc(cli_runner):
    """ Test `cray capmc` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc'])

    outputs = [
        "cli capmc [OPTIONS] COMMAND [ARGS]...",
        "Cray Advanced Platform Monitoring and Control (CAPMC) API",
        "emergency_power_off",
        "get_nid_map",
        "get_node_energy",
        "get_node_energy_stats",
        "get_node_energy_counter",
        "get_node_rules",
        "get_node_status",
        "get_power_cap",
        "get_power_cap_capabilities",
        "get_xname_status",
        "get_group_status",
        "node_off",
        "node_on",
        "node_reinit",
        "xname_off",
        "xname_on",
        "xname_reinit",
        "group_off",
        "group_on",
        "group_reinit"
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_nid_map(cli_runner):
    """ Test `cray capmc get_nid_map` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_nid_map'])

    outputs = [
        "cli capmc get_nid_map [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_rules(cli_runner):
    """ Test `cray capmc get_node_rules` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_node_rules'])

    outputs = [
        "cli capmc get_node_rules [OPTIONS] COMMAND [ARGS]...",
        "create",
        "list"
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_status(cli_runner):
    """ Test `cray capmc get_node_status` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_node_status'])

    outputs = [
        "cli capmc get_node_status [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_xname_status(cli_runner):
    """ Test `cray capmc get_xname_status` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_xname_status'])

    outputs = [
        "cli capmc get_xname_status [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_group_status(cli_runner):
    """ Test `cray capmc get_group_status` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_group_status'])

    outputs = [
        "cli capmc get_group_status [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_node_off(cli_runner):
    """ Test `cray capmc node_off` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'node_off'])

    outputs = [
        "cli capmc node_off [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_node_on(cli_runner):
    """ Test `cray capmc node_on` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'node_on'])

    outputs = [
        "cli capmc node_on [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_node_reinit(cli_runner):
    """ Test `cray capmc node_reinit` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'node_reinit'])

    outputs = [
        "cli capmc node_reinit [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_off(cli_runner):
    """ Test `cray capmc xname_off` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'xname_off'])

    outputs = [
        "cli capmc xname_off [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_off_help(cli_runner):
    """ Test `cray capmc xname_off create --help` to make sure expected options are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'xname_off', 'create', '--help'])

    outputs = [
        "cli capmc xname_off create [OPTIONS]",
        "prereq",
        "recursive",
        "force",
        "xnames",
        "reason",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_on(cli_runner):
    """ Test `cray capmc xname_on` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'xname_on'])

    outputs = [
        "cli capmc xname_on [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_on_help(cli_runner):
    """ Test `cray capmc xname_on create --help` to make sure the expected options are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'xname_on', 'create', '--help'])

    outputs = [
        "cli capmc xname_on create [OPTIONS]",
        "prereq",
        "recursive",
        "force",
        "xnames",
        "reason",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_reinit(cli_runner):
    """ Test `cray capmc xname_reinit` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'xname_reinit'])

    outputs = [
        "cli capmc xname_reinit [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_reinit_help(cli_runner):
    """ Test `cray capmc xname_reinit create --help` to be sure expected options are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'xname_reinit', 'create', '--help'])

    outputs = [
        "cli capmc xname_reinit create [OPTIONS]",
        "force",
        "xnames",
        "reason",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_off(cli_runner):
    """ Test `cray capmc group_off` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'group_off'])

    outputs = [
        "cli capmc group_off [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_off_help(cli_runner):
    """ Test `cray capmc group_off create --help` to make sure expected options are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'group_off', 'create', '--help'])

    outputs = [
        "cli capmc group_off create [OPTIONS]",
        "force",
        "groups",
        "reason",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_on(cli_runner):
    """ Test `cray capmc group_on` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'group_on'])

    outputs = [
        "cli capmc group_on [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_on_help(cli_runner):
    """ Test `cray capmc group_on create --help` to make sure the expected options are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'group_on', 'create', '--help'])

    outputs = [
        "cli capmc group_on create [OPTIONS]",
        "force",
        "groups",
        "reason",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_reinit(cli_runner):
    """ Test `cray capmc group_reinit` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'group_reinit'])

    outputs = [
        "cli capmc group_reinit [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_reinit_help(cli_runner):
    """ Test `cray capmc group_reinit create --help` to be sure expected options are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'group_reinit', 'create', '--help'])

    outputs = [
        "cli capmc group_reinit create [OPTIONS]",
        "force",
        "groups",
        "reason",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_emergency_power_off(cli_runner):
    """ Test `cray capmc emergency_power_off` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'emergency_power_off'])

    outputs = [
        "cli capmc emergency_power_off [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_emergency_power_off_help(cli_runner):
    """ Test `cray capmc emergency_power_off create --help` for expected options """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'emergency_power_off', 'create', '--help'])

    outputs = [
        "cli capmc emergency_power_off create [OPTIONS]",
        "force",
        "xnames",
        "reason",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

capmc_url_base = '/capmc/v1'

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_rules_call(cli_runner, rest_mock):
    """ Test `cray capmc get_node_rules list` """
    #pylint: disable=protected-access
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/get_node_rules'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'get_node_rules', 'list'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    assert data.get('body') is None
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri

nids = 1138
# pylint: disable=redefined-outer-name
def test_cray_capmc_node_off_call(cli_runner, rest_mock):
    """ Test `cray capmc node_off create --nids <nid list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/node_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'node_off', 'create',
                                 '--nids', nids])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['nids'] == nids
    assert data.get('body').get('force') is None

# pylint: disable=redefined-outer-name
def test_cray_capmc_node_off_force_call(cli_runner, rest_mock):
    """ Test `cray capmc node_off create --nids <nid list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/node_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'node_off', 'create',
                                 '--nids', nids, '--force', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['nids'] == nids
    assert data['body']['force'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_node_on_call(cli_runner, rest_mock):
    """ Test `cray capmc node_on create --nids <nid list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/node_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'node_on', 'create',
                                 '--nids', nids])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['nids'] == nids
    assert data.get('body').get('force') is None

# pylint: disable=redefined-outer-name
def test_cray_capmc_node_on_force_call(cli_runner, rest_mock):
    """ Test `cray capmc node_on create --nids <nid list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/node_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'node_on', 'create',
                                 '--nids', nids, '--force', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['nids'] == nids
    assert data['body']['force'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_node_reinit_call(cli_runner, rest_mock):
    """ Test `cray capmc node_reinit create --nids <nid list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/node_reinit'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'node_reinit', 'create',
                                 '--nids', nids])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['nids'] == nids
    assert data.get('body').get('force') is None

# pylint: disable=redefined-outer-name
def test_cray_capmc_node_reinit_force_call(cli_runner, rest_mock):
    """ Test `cray capmc node_reinit create --nids <nid list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/node_reinit'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'node_reinit', 'create',
                                 '--nids', nids, '--force', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['nids'] == nids
    assert data['body']['force'] is True

xname = 'x0c0s0b0n0'
# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_off_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_off create --xnames <xname list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_off', 'create',
                                 '--xnames', xname])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data.get('body').get('force') is None

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_off_force_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_off create --xnames <xname list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_off', 'create',
                                 '--xnames', xname, '--force', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['force'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_off_recursive_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_off create --xnames <xname list> --recursive true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_off', 'create',
                                 '--xnames', xname, '--recursive', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['recursive'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_off_force_recursive_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_off create --xnames <xname list> --force true --recursive true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_off', 'create',
                                 '--xnames', xname, '--force', 'true',
                                 '--recursive', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['force'] is True
    assert data['body']['recursive'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_off_prereq_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_off create --xnames <xname list> --prereq true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_off', 'create',
                                 '--xnames', xname, '--prereq', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['prereq'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_off_force_prereq_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_off create --xnames <xname list> --force true --prereq true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_off', 'create',
                                 '--xnames', xname, '--force', 'true',
                                 '--prereq', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['force'] is True
    assert data['body']['prereq'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_on_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_on create --xnames <xname list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_on', 'create',
                                 '--xnames', xname])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data.get('body').get('force') is None

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_on_force_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_on create --xnames <xname list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_on', 'create',
                                 '--xnames', xname, '--force', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['force'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_on_recursive_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_on create --xnames <xname list> --recursive true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_on', 'create',
                                 '--xnames', xname, '--recursive', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['recursive'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_on_force_recursive_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_on create --xnames <xname list> --force true --recursive true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_on', 'create',
                                 '--xnames', xname, '--force', 'true',
                                 '--recursive', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['force'] is True
    assert data['body']['recursive'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_on_prereq_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_on create --xnames <xname list> --prereq true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_on', 'create',
                                 '--xnames', xname, '--prereq', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['prereq'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_on_force_prereq_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_on create --xnames <xname list> --force true --prereq true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_on', 'create',
                                 '--xnames', xname, '--force', 'true',
                                 '--prereq', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['force'] is True
    assert data['body']['prereq'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_reinit_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_reinit create --xnames <xname list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_reinit'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_reinit', 'create',
                                 '--xnames', xname])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data.get('body').get('force') is None

# pylint: disable=redefined-outer-name
def test_cray_capmc_xname_reinit_force_call(cli_runner, rest_mock):
    """ Test `cray capmc xname_reinit create --xnames <xname list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/xname_reinit'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'xname_reinit', 'create',
                                 '--xnames', xname, '--force', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [xname]
    assert data['body']['force'] is True

group = 'my_group'
# pylint: disable=redefined-outer-name
def test_cray_capmc_group_off_call(cli_runner, rest_mock):
    """ Test `cray capmc group_off create --groups <group list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/group_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'group_off', 'create',
                                 '--groups', group])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['groups'] == [group]
    assert data.get('body').get('force') is None

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_off_force_call(cli_runner, rest_mock):
    """ Test `cray capmc group_off create --groups <group list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/group_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'group_off', 'create',
                                 '--groups', group, '--force', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['groups'] == [group]
    assert data['body']['force'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_on_call(cli_runner, rest_mock):
    """ Test `cray capmc group_on create --groups <group list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/group_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'group_on', 'create',
                                 '--groups', group])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['groups'] == [group]
    assert data.get('body').get('force') is None

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_on_force_call(cli_runner, rest_mock):
    """ Test `cray capmc group_on create --groups <group list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/group_on'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'group_on', 'create',
                                 '--groups', group, '--force', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['groups'] == [group]
    assert data['body']['force'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_reinit_call(cli_runner, rest_mock):
    """ Test `cray capmc group_reinit create --groups <group list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/group_reinit'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'group_reinit', 'create',
                                 '--groups', group])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['groups'] == [group]
    assert data.get('body').get('force') is None

# pylint: disable=redefined-outer-name
def test_cray_capmc_group_reinit_force_call(cli_runner, rest_mock):
    """ Test `cray capmc group_reinit create --groups <group list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/group_reinit'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'group_reinit', 'create',
                                 '--groups', group, '--force', 'true'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['groups'] == [group]
    assert data['body']['force'] is True

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_power_cap_capabilities(cli_runner):
    """ Test `cray capmc get_power_cap_capabilities` for expected commands"""
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_power_cap_capabilities'])

    outputs = [
        "cli capmc get_power_cap_capabilities [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_power_cap_capabilities_help(cli_runner):
    """ Test `cray capmc get_power_cap_capabilities --help` for expected options """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_power_cap_capabilities', 'create', '--help'])

    outputs = [
        "cli capmc get_power_cap_capabilities create [OPTIONS]",
        "nids",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_power_cap(cli_runner):
    """ Test `cray capmc get_power_cap` for expected commands"""
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_power_cap'])

    outputs = [
        "cli capmc get_power_cap [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_power_cap_help(cli_runner):
    """ Test `cray capmc get_power_cap --help` for expected options """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_power_cap', 'create', '--help'])

    outputs = [
        "cli capmc get_power_cap create [OPTIONS]",
        "nids",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_power_cap_capabilities_create(cli_runner, rest_mock):
    """ Test `cray capmc get_power_cap_capabilities create --nids <nid list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/get_power_cap_capabilities'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'get_power_cap_capabilities', 'create',
                                 '--nids', nids])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['nids'] == nids

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_power_cap_create(cli_runner, rest_mock):
    """ Test `cray capmc get_power_cap create --nids <nid list>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/get_power_cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'get_power_cap', 'create',
                                 '--nids', nids])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['nids'] == nids

# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap(cli_runner):
    """ Test `cray capmc set_power_cap` for expected commands"""
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'set_power_cap'])

    outputs = [
        "cli capmc set_power_cap [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_help(cli_runner):
    """ Test `cray capmc set_power_cap --help` for expected options """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create', '--help'])

    outputs = [
        "cli capmc set_power_cap create [OPTIONS]",
        "nids",
        "node",
        "accel",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

spc_nids = '1,3,5,7'
spc_node_val = 400
spc_accel_val = 200
# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_create(cli_runner, rest_mock):
    """ Test `cray capmc set_power_cap create --nids <nid list> --node <int> --accel <int>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/set_power_cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create',
                                 '--nids', spc_nids,
                                 '--node', spc_node_val,
                                 '--accel', spc_accel_val])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    nids = data['body']['nids']
    for i, e in enumerate(nids):
        assert e['nid'] == i * 2 + 1
        c = e['controls']
        assert c[0]['name'] == 'node'
        assert c[0]['val'] == spc_node_val
        assert c[1]['name'] == 'accel'
        assert c[1]['val'] == spc_accel_val

# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_create_only_node(cli_runner, rest_mock):
    """ Test `cray capmc set_power_cap create --nids <nid list> --node <int>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/set_power_cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create',
                                 '--nids', spc_nids,
                                 '--node', spc_node_val])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    nids = data['body']['nids']
    for i, e in enumerate(nids):
        assert e['nid'] == i * 2 + 1
        c = e['controls']
        assert c[0]['name'] == 'node'
        assert c[0]['val'] == spc_node_val

# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_create_only_accel(cli_runner, rest_mock):
    """ Test `cray capmc set_power_cap create --nids <nid list> --accel <int>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/set_power_cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create',
                                 '--nids', spc_nids,
                                 '--accel', spc_accel_val])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    nids = data['body']['nids']
    for i, e in enumerate(nids):
        assert e['nid'] == i * 2 + 1
        c = e['controls']
        assert c[0]['name'] == 'accel'
        assert c[0]['val'] == spc_accel_val

# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_create_no_nids(cli_runner, rest_mock):
    """ Test `cray capmc set_power_cap create --node <int> --accel <int>` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create',
                                 '--node', spc_node_val,
                                 '--accel', spc_accel_val])
    print(result.output)
    assert result.exit_code == 2
    outputs = [
        "Invalid value: --nids option required",
        ]

    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_create_no_node_or_accel(cli_runner, rest_mock):
    """ Test `cray capmc set_power_cap create --nids <nid list>` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create',
                                 '--nids', spc_nids])
    print(result.output)
    assert result.exit_code == 2
    outputs = [
        "Invalid value: --node and/or --accel must be supplied.",
        ]

    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_energy(cli_runner):
    """ Test `cray capmc get_node_energy` for expected commands"""
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_node_energy'])

    outputs = [
        "cli capmc get_node_energy [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_energy_help(cli_runner):
    """ Test `cray capmc get_node_energy --help` for expected options """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_node_energy', 'create', '--help'])

    outputs = [
        "cli capmc get_node_energy create [OPTIONS]",
        "job-id",
        "apid",
        "nids",
        "end-time",
        "start-time",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

gne_nids = '1,3,5,7'
gne_apid = '831ab138'
gne_job_id = '831138.sdb'
gne_start_time = '2019-07-10 12:55:06'
gne_end_time = '2019-07-10 14:00:00'
# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_energy_create(cli_runner, rest_mock):
    """
    Test `cray capmc get_node_energy create --nids <nid list> --apid <int> --job-id <str> \
            --start-time <str> --end-time <str>`
    """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/get_node_energy'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'get_node_energy', 'create',
                                 '--nids', gne_nids,
                                 '--apid', gne_apid,
                                 '--job-id', gne_job_id,
                                 '--start-time', gne_start_time,
                                 '--end-time', gne_end_time])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    data['body']['nids'] = gne_nids
    data['body']['apid'] = gne_apid
    data['body']['job_id'] = gne_job_id
    data['body']['start_time'] = gne_start_time
    data['body']['end_time'] = gne_end_time

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_energy_stats(cli_runner):
    """ Test `cray capmc get_node_energy_stats` for expected commands"""
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_node_energy_stats'])

    outputs = [
        "cli capmc get_node_energy_stats [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_energy_stats_help(cli_runner):
    """ Test `cray capmc get_node_energy_stats --help` for expected options """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_node_energy_stats', 'create', '--help'])

    outputs = [
        "cli capmc get_node_energy_stats create [OPTIONS]",
        "job-id",
        "apid",
        "nids",
        "end-time",
        "start-time",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_energy_stats_create(cli_runner, rest_mock):
    """
    Test `cray capmc get_node_energy_stats create --nids <nid list> --apid <int> --job-id <str> \
            --start-time <str> --end-time <str>`
    """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/get_node_energy_stats'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'get_node_energy_stats', 'create',
                                 '--nids', gne_nids,
                                 '--apid', gne_apid,
                                 '--job-id', gne_job_id,
                                 '--start-time', gne_start_time,
                                 '--end-time', gne_end_time])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    data['body']['nids'] = gne_nids
    data['body']['apid'] = gne_apid
    data['body']['job_id'] = gne_job_id
    data['body']['start_time'] = gne_start_time
    data['body']['end_time'] = gne_end_time

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_energy_counter(cli_runner):
    """ Test `cray capmc get_node_energy_counter` for expected commands"""
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_node_energy_counter'])

    outputs = [
        "cli capmc get_node_energy_counter [OPTIONS] COMMAND [ARGS]...",
        "create",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_energy_counter_help(cli_runner):
    """ Test `cray capmc get_node_energy_counter --help` for expected options """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'get_node_energy_counter', 'create', '--help'])

    outputs = [
        "cli capmc get_node_energy_counter create [OPTIONS]",
        "job-id",
        "apid",
        "nids",
        "time",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_capmc_get_node_energy_counter_create(cli_runner, rest_mock):
    """
    Test `cray capmc get_node_energy_counter create --nids <nid list> --apid <int> --job-id <str> \
            --time <str>`
    """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/get_node_energy_counter'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'get_node_energy_counter', 'create',
                                 '--nids', gne_nids,
                                 '--apid', gne_apid,
                                 '--job-id', gne_job_id,
                                 '--time', gne_start_time])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    data['body']['nids'] = gne_nids
    data['body']['apid'] = gne_apid
    data['body']['job_id'] = gne_job_id
    data['body']['time'] = gne_start_time

EPOxname = 's0'
# pylint: disable=redefined-outer-name
def test_cray_capmc_emergency_power_off_force_call(cli_runner, rest_mock):
    """ Test `cray capmc emergency_power_off create --xnames <xname list> --force true` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/emergency_power_off'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'emergency_power_off', 'create',
                                 '--xnames', EPOxname, '--force', 'true',
                                 '--reason', 'Test EPO'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert data['body']['xnames'] == [EPOxname]
    assert data['body']['reason'] == 'Test EPO'
