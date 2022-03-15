""" Test the main CLI command (`cray`) and options.

MIT License

(C) Copyright [2020-2022] Hewlett Packard Enterprise Development LP

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

capmc_url_base = '/capmc/v1'


nids = 1138


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
        "control",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

spc_nids = '1,3,5,7'
spc_node_val = 400
spc_accel_val = 200
# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_create(cli_runner, rest_mock):
    """ Test `cray capmc set_power_cap create --nids <nid list> --control <string> <int>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/set_power_cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create',
                                 '--nids', spc_nids,
                                 '--control', "node 0", spc_node_val,
                                 '--control', "accel 0", spc_accel_val])
    print(result)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    nids = data['body']['nids']
    for i, e in enumerate(nids):
        assert e['nid'] == i * 2 + 1
        c = e['controls']
        assert c[0]['name'] == 'node 0'
        assert c[0]['val'] == spc_node_val
        assert c[1]['name'] == 'accel 0'
        assert c[1]['val'] == spc_accel_val

# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_create_only_node(cli_runner, rest_mock):
    """ Test `cray capmc set_power_cap create --nids <nid list> --control <string> <int>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/set_power_cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create',
                                 '--nids', spc_nids,
                                 '--control', "node 0", spc_node_val])
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
        assert c[0]['name'] == 'node 0'
        assert c[0]['val'] == spc_node_val

# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_create_only_accel(cli_runner, rest_mock):
    """ Test `cray capmc set_power_cap create --nids <nid list> --control <string> <int>` """
    runner, cli, opts = cli_runner
    url_template = capmc_url_base + '/set_power_cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create',
                                 '--nids', spc_nids,
                                 '--control', "accel 0", spc_accel_val])
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
        assert c[0]['name'] == 'accel 0'
        assert c[0]['val'] == spc_accel_val

# pylint: disable=redefined-outer-name
def test_cray_capmc_set_power_cap_create_no_nids(cli_runner, rest_mock):
    """ Test `cray capmc set_power_cap create --control <string> <int> --control <string> <int>` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['capmc', 'set_power_cap', 'create',
                                 '--control', "node 0", spc_node_val,
                                 '--control', "accel 0", spc_accel_val])
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
        "Invalid value: --control must be supplied.",
        ]

    for out in outputs:
        assert out in result.output



gne_nids = '1,3,5,7'
gne_apid = '831ab138'
gne_job_id = '831138.sdb'
gne_start_time = '2019-07-10 12:55:06'
gne_end_time = '2019-07-10 14:00:00'
