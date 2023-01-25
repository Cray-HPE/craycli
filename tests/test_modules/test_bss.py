""" Test the bss module.

MIT License

(C) Copyright [2020,2023] Hewlett Packard Enterprise Development LP

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
import json

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import


# pylint: disable=redefined-outer-name
def test_cray_bss_help_info(cli_runner, rest_mock):
    """ Test `cray bss` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bss'])

    outputs = [
        "cli bss [OPTIONS] COMMAND [ARGS]...",
        "Boot Script Service",
        "bootparameters",
        "bootscript",
        "dumpstate",
        "hosts",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_bss_bootparameters(cli_runner, rest_mock):
    """ Test `cray bss bootparameters` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bss', 'bootparameters'])

    outputs = [
        "cli bss bootparameters [OPTIONS] COMMAND [ARGS]...",
        "create",
        "delete",
        "list",
        "replace",
        "update",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_bss_bootscript(cli_runner, rest_mock):
    """ Test `cray bss bootscript` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bss', 'bootscript'])

    outputs = [
        "cli bss bootscript [OPTIONS] COMMAND [ARGS]...",
        "list"
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_bss_dumpstate(cli_runner, rest_mock):
    """ Test `cray bss dumpstate` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bss', 'dumpstate'])

    outputs = [
        "cli bss dumpstate [OPTIONS] COMMAND [ARGS]...",
        "list",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_cray_bss_hosts(cli_runner, rest_mock):
    """ Test `cray capmc get_xname_status` to make sure the expected commands are available """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bss', 'hosts'])

    outputs = [
        "cli bss hosts [OPTIONS] COMMAND [ARGS]...",
        "create",
        "list",
        ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

kernel = '/test/kernel'
initrd = '/test/initrd'
params = 'foo bar params'
host = 'foo'
nid = 42
mac = "11_22_33_44_55_66"
ts = '12345678'
arch = 'x86_64'
retry = '1'

# pylint: disable=redefined-outer-name
def test_cray_bss_rest_call_create(cli_runner, rest_mock):
    """ Test `cray bss create` with various params """
    # pylint: disable=protected-access
    runner, cli, opts = cli_runner
    url_template = '/apis/bss/boot/v1/bootparameters'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['bss', 'bootparameters', 'create',
                                 '--hosts', host,
                                 '--kernel', kernel,
                                 '--initrd', initrd,
                                 '--nids', str(nid),
                                 '--macs', mac,
                                 '--params', params])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    assert data.get('body')
    body = data.get('body')
    assert body['kernel'] == kernel
    assert body['initrd'] == initrd
    assert body['params'] == params
    assert host in body['hosts']
    assert nid in body['nids']
    assert mac in body['macs']
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template

# pylint: disable=redefined-outer-name
def test_cray_bss_rest_call_replace(cli_runner, rest_mock):
    """ Test `cray bss create` with various params """
    # pylint: disable=protected-access
    runner, cli, opts = cli_runner
    url_template = '/apis/bss/boot/v1/bootparameters'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['bss', 'bootparameters', 'replace',
                                 '--hosts', host,
                                 '--kernel', kernel,
                                 '--initrd', initrd,
                                 '--nids', str(nid),
                                 '--macs', mac,
                                 '--params', params])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'put'
    assert data.get('body')
    body = data.get('body')
    assert body['kernel'] == kernel
    assert body['initrd'] == initrd
    assert body['params'] == params
    assert host in body['hosts']
    assert nid in body['nids']
    assert mac in body['macs']
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template

# pylint: disable=redefined-outer-name
def test_cray_bss_bootscript_call(cli_runner, rest_mock):
    """ Test `cray bss create` with various params """
    # pylint: disable=protected-access
    runner, cli, opts = cli_runner
    url_template = '/apis/bss/boot/v1/bootscript'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['bss', 'bootscript', 'list',
                                 '--name', host,
                                 '--arch', arch,
                                 '--mac', mac,
                                 '--nid', str(nid),
                                 '--retry', retry,
                                 '--ts', str(ts)])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    assert data.get('body') is None
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    assert "name=" + host in uri
    assert "arch=" + arch in uri
    assert "mac=" + mac in uri
    assert "nid=" + str(nid) in uri
    assert "retry=" + retry in uri
    assert "ts=" + ts in uri
