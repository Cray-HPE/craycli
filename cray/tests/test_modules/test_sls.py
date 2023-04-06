#
#  MIT License
#
#  (C) Copyright 2020-2023 Hewlett Packard Enterprise Development LP
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.
#
""" Test the sls module. """
# pylint: disable=unused-argument
# pylint: disable=invalid-name
# pylint: disable=too-many-locals

import json
import os
import tempfile


def test_sls_help_info(cli_runner, rest_mock):
    """ Test `cray sls` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['sls'])
    assert result.exit_code == 0

    outputs = [
        "cli sls [OPTIONS] COMMAND [ARGS]...",
        "dumpstate",
        "hardware",
        "health",
        "loadstate",
        "networks",
        "search",
        "version",
    ]
    for out in outputs:
        assert out in result.output


def test_sls_dumpstate(cli_runner, rest_mock):
    """ Test `cray sls dumpstate` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['sls', 'dumpstate'])

    outputs = [
        "cli sls dumpstate [OPTIONS] COMMAND [ARGS]...",
        "list",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


def test_sls_hardware(cli_runner, rest_mock):
    """ Test `cray sls hardware` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['sls', 'hardware'])

    outputs = [
        "cli sls hardware [OPTIONS] COMMAND [ARGS]...",
        "create",
        "delete",
        "describe",
        "update",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


def test_sls_loadstate(cli_runner, rest_mock):
    """ Test `cray sls loadstate` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['sls', 'loadstate'])

    outputs = [
        "cli sls loadstate [OPTIONS] COMMAND [ARGS]...",
        "create",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


def test_sls_networks(cli_runner, rest_mock):
    """ Test `cray sls networks` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['sls', 'networks'])

    print(result.output)
    outputs = [
        "cli sls networks [OPTIONS] COMMAND [ARGS]...",
        "create",
        "delete",
        "describe",
        "list",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


def test_sls_health(cli_runner, rest_mock):
    """ Test `cray sls health` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['sls', 'health'])

    outputs = [
        "cli sls health [OPTIONS] COMMAND [ARGS]...",
        "list",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


def test_sls_search(cli_runner, rest_mock):
    """ Test `cray sls search` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['sls', 'search'])

    outputs = [
        "cli sls search [OPTIONS] COMMAND [ARGS]...",
        "hardware",
        "networks",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


def test_sls_version(cli_runner, rest_mock):
    """ Test `cray sls version` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['sls', 'version'])

    outputs = [
        "cli sls version [OPTIONS] COMMAND [ARGS]...",
        "list",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


def test_sls_dumpstate_list(cli_runner, rest_mock):
    """ Test `cray sls dumpstate` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/dumpstate'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['sls', 'dumpstate', 'list'])

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template


def test_sls_health_list(cli_runner, rest_mock):
    """ Test `cray sls health` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/health'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['sls', 'health', 'list'])

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template


def test_sls_version_list(cli_runner, rest_mock):
    """ Test `cray sls version` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/version'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['sls', 'version', 'list'])

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template


Type = 'ComputeModule'
Xname = 'x0c0s0'
Parent = 'x0c0'
Class = 'Mountain'
Children = ['x0c0s0b0n0', 'x0c0s0b0n1', 'x0c0s0b1n0', 'x0c0s0b1n1']


def test_sls_hardware_create(cli_runner, rest_mock):
    """ Test `cray sls hardware create` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/hardware'
    config = opts['default']
    hostname = config['hostname']
    powered_by = 'x3001'
    result = runner.invoke(
        cli, ['sls', 'hardware', 'create',
              '--xname', Xname,
              '--class', Class,
              '--extra-properties', f'{{ "PoweredBy":"{powered_by}" }}']
    )

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    assert data.get('body')
    body = data.get('body')
    assert body['Xname'] == Xname
    assert body['Class'] == Class
    assert body.get('ExtraProperties', {}).get('PoweredBy') == powered_by
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template


def test_sls_hardware_create_payload(cli_runner, rest_mock):
    """ Test `cray sls hardware create` using a payload file """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/hardware'
    config = opts['default']
    hostname = config['hostname']
    powered_by = 'x3002'
    payload = f"""{{
        "Xname": "{Xname}",
        "Class": "{Class}",
        "ExtraProperties": {{
            "PoweredBy": "{powered_by}"
        }}
    }}"""

    fd, path = tempfile.mkstemp(
        prefix='test_sls_hardware_create',
        suffix='.json'
    )
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(payload)

        result = runner.invoke(
            cli,
            ['sls', 'hardware', 'create', '--payload-file', path]
        )

        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        body = data.get('body')
        assert body
        assert body['Xname'] == Xname
        assert body['Class'] == Class
        assert body.get('ExtraProperties', {}).get('PoweredBy') == powered_by
        uri = data['url'].split(hostname)[-1]
        assert uri == url_template
    finally:
        os.remove(path)


def test_sls_hardware_create_incompatible_parameters(cli_runner, rest_mock):
    """ Test `cray sls hardware create` with incompatible parameters """
    runner, cli, _ = cli_runner
    powered_by = 'x3003'
    payload = f"""{{
        "Xname": "{Xname}",
        "Class": "{Class}",
        "ExtraProperties": {{
            "PoweredBy": "{powered_by}"
        }}
    }}"""

    fd, path = tempfile.mkstemp(
        prefix='test_sls_hardware_create',
        suffix='.json'
    )
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(payload)

        result = runner.invoke(
            cli, ['sls', 'hardware', 'create',
                  '--xname', Xname,
                  '--class', Class,
                  '--extra-properties', f'{{ "PoweredBy":"{powered_by}" }}',
                  '--payload-file', path]
        )

        print(result.output)
        assert result.exit_code != 0
    finally:
        os.remove(path)


def test_sls_hardware_update(cli_runner, rest_mock):
    """ Test `cray sls hardware update` with various params """
    runner, cli, opts = cli_runner
    url_template = f'/apis/sls/v1/hardware/{Xname}'
    config = opts['default']
    hostname = config['hostname']
    powered_by = 'x3004'
    result = runner.invoke(
        cli, ['sls', 'hardware', 'update', Xname,
              '--class', Class,
              '--extra-properties', f'{{ "PoweredBy":"{powered_by}" }}']
    )

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'put'
    assert data.get('body')
    body = data.get('body')
    assert body['xname'] == Xname
    assert body['Class'] == Class
    assert body.get('ExtraProperties', {}).get('PoweredBy') == powered_by
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template


def test_sls_hardware_update_payload(cli_runner, rest_mock):
    """ Test `cray sls hardware create` using a payload file """
    runner, cli, opts = cli_runner
    url_template = f'/apis/sls/v1/hardware/{Xname}'
    config = opts['default']
    hostname = config['hostname']
    powered_by = 'x3005'
    payload = f"""{{
        "Class": "{Class}",
        "ExtraProperties": {{
            "PoweredBy": "{powered_by}"
        }}
    }}"""

    fd, path = tempfile.mkstemp(
        prefix='test_sls_hardware_create',
        suffix='.json'
    )
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(payload)

        result = runner.invoke(
            cli,
            ['sls', 'hardware', 'update', Xname, '--payload-file', path]
        )

        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'put'
        body = data.get('body')
        assert body
        assert body['Class'] == Class
        assert body.get('ExtraProperties', {}).get('PoweredBy') == powered_by
        uri = data['url'].split(hostname)[-1]
        assert uri == url_template
    finally:
        os.remove(path)


def test_sls_hardware_update_incompatible_parameters(cli_runner, rest_mock):
    """ Test `cray sls hardware update` incorrect parameters """
    runner, cli, _ = cli_runner
    powered_by = 'x3006'
    payload = f"""{{
        "Class": "{Class}",
        "ExtraProperties": {{
            "PoweredBy": "{powered_by}"
        }}
    }}"""

    fd, path = tempfile.mkstemp(
        prefix='test_sls_hardware_create',
        suffix='.json'
    )
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(payload)

        result = runner.invoke(
            cli, ['sls', 'hardware', 'update', Xname,
                  '--class', Class,
                  '--extra-properties', f'{{ "PoweredBy":"{powered_by}" }}',
                  '--payload-file', path]
        )

        print(result.output)
        assert result.exit_code != 0
    finally:
        os.remove(path)


def test_sls_hardware_delete(cli_runner, rest_mock):
    """ Test `cray sls hardware delete` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/hardware'
    del_xname = 'x0c0s0'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['sls', 'hardware', 'delete', 'x0c0s0'])

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template + '/' + del_xname


def test_sls_hardware_describe(cli_runner, rest_mock):
    """ Test `cray sls hardware describe` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/hardware'
    des_xname = 'x0c0s0'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['sls', 'hardware', 'describe', 'x0c0s0'])

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template + '/' + des_xname


def test_sls_networks_create(cli_runner, rest_mock):
    """ Test `cray sls networks create` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/networks'
    config = opts['default']
    hostname = config['hostname']
    network_name = 'foobar'
    payload = f"""{{
        "Name": "{network_name}",
        "FullName": "barfoobar",
        "IPRanges": ["192.168.1.0/24"],
        "Type": "ethernet"
    }}"""

    fd, path = tempfile.mkstemp(
        prefix='test_sls_networks_create',
        suffix='.json'
    )
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(payload)

        result = runner.invoke(cli, ['sls', 'networks', 'create', path])

        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        body = data.get('body')
        assert body
        assert body['Name'] == network_name
        uri = data['url'].split(hostname)[-1]
        assert uri == url_template
    finally:
        os.remove(path)


def test_sls_networks_update(cli_runner, rest_mock):
    """ Test `cray sls networks update` with various params """
    runner, cli, opts = cli_runner
    network_name = 'foobar'
    url_template = f'/apis/sls/v1/networks/{network_name}'
    config = opts['default']
    hostname = config['hostname']
    payload = f"""{{
        "Name": "{network_name}",
        "FullName": "barfoobar",
        "IPRanges": ["192.168.1.0/24"],
        "Type": "ethernet"
    }}"""

    fd, path = tempfile.mkstemp(
        prefix='test_sls_networks_create',
        suffix='.json'
    )
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(payload)

        result = runner.invoke(
            cli,
            ['sls', 'networks', 'update', path, network_name]
        )

        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'put'
        body = data.get('body')
        assert body
        assert body['Name'] == network_name
        uri = data['url'].split(hostname)[-1]
        assert uri == url_template
    finally:
        os.remove(path)


def test_sls_networks_delete(cli_runner, rest_mock):
    """ Test `cray sls networks delete` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/networks'
    del_network = "foobar"
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['sls', 'networks', 'delete', del_network])

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template + '/' + del_network


def test_sls_networks_describe(cli_runner, rest_mock):
    """ Test `cray sls networks describe` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/networks'
    des_network = "foobar"
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['sls', 'networks', 'describe', des_network])

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    uri = data['url'].split(hostname)[-1]
    assert uri == url_template + '/' + des_network


sxname = 'x0c0s0'
sparent = 'x0c0'
sclass = 'Mountain'
stype = 'ComputeModule'
spower = 'x0c0s0j0'
sobject = 'x0'
snics = 'x0c0s0b0n0i0'
snetwork = 'foobar'
speers = 'x0c0'


def test_sls_search_hardware_list(cli_runner, rest_mock):
    """ Test `cray sls search hardware list` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/search/hardware'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(
        cli, ['sls', 'search', 'hardware', 'list',
              '--xname', sxname,
              '--parent', sparent,
              '--class', sclass,
              '--type', stype,
              '--power-connector', spower,
              '--object', sobject,
              '--node-nics', snics,
              '--networks', snetwork,
              '--peers', speers]
    )

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    outputs = [
        url_template,
        "xname=" + sxname,
        "parent=" + sparent,
        "class=" + sclass,
        "type=" + stype,
        "power_connector=" + spower,
        "object=" + sobject,
        "node_nics=" + snics,
        "networks=" + snetwork,
        "peers=" + speers,
    ]
    for out in outputs:
        assert out in uri


sname = 'foobar'
sfullname = 'barfoobar'
stype = 'ComputeModule'
sipaddr = '192.168.1.1'


def test_sls_search_networks_list(cli_runner, rest_mock):
    """ Test `cray sls search networks list` with various params """
    runner, cli, opts = cli_runner
    url_template = '/apis/sls/v1/search/networks'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(
        cli, ['sls', 'search', 'networks', 'list',
              '--name', sname,
              '--full-name', sfullname,
              '--type', stype,
              '--ip-address', sipaddr]
    )

    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    outputs = [
        url_template,
        "name=" + sname,
        "full_name=" + sfullname,
        "type=" + stype,
        "ip_address=" + sipaddr,
    ]

    for out in outputs:
        assert out in uri
