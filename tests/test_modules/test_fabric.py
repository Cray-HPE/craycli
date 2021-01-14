""" Test the fabric-control module."""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments, unused-argument
import json

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import

basePath = 'apis/fc/v2'

# pylint: disable=redefined-outer-name
def test_fabric_help_info(cli_runner, rest_mock):
    """ Test `cray fabric` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric'])
    assert result.exit_code == 0

    outputs = [
        "cli fabric [OPTIONS] COMMAND [ARGS]...",
        "Fabric Controller API",
        "fabric-configuration",
        "port-links",
        "port-sets",
        "ports"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_priv_set_template(cli_runner, rest_mock):
    """ Test `cray fabric priv set-template` with valid params """

    runner, cli, config = cli_runner
    url = config['default']['hostname']
    json_data = '''{
        "numGroups": 0,
        "maxNumLocalSwitches": 2,
        "switches": [
            {
                "grpId": 0,
                "IP": "IP",
                "fabricPorts": [
                    {
                        "meta": {
                            "conn_port": "conn_port"
                        },
                        "id": "id"
                    },
                    {
                        "meta": {
                            "conn_port": "conn_port"
                        },
                        "id": "id"
                    }
                ],
                "edgePorts": [
                    {
                        "meta": {
                            "conn_port": "conn_port"
                        },
                        "id": "id"
                    },
                    {
                        "meta": {
                            "conn_port": "conn_port"
                        },
                        "id": "id"
                    }
                ],
                "swcNum": 6
            },
            {
                "grpId": 0,
                "IP": "IP",
                "fabricPorts": [
                    {
                        "meta": {
                            "conn_port": "conn_port"
                        },
                        "id": "id"
                    },
                    {
                        "meta": {
                            "conn_port": "conn_port"
                        },
                        "id": "id"
                    }
                ],
                "edgePorts": [
                    {
                        "meta": {
                            "conn_port": "conn_port"
                        },
                        "id": "id"
                    },
                    {
                        "meta": {
                            "conn_port": "conn_port"
                        },
                        "id": "id"
                    }
                ],
                "swcNum": 6
            }
        ],
        "links": [
            {
                "endpoint1": "x16c3r4j7p0",
                "endpoint2": "x16c3r4j7p0"
            },
            {
                "endpoint1": "x16c3r4j7p0",
                "endpoint2": "x16c3r4j7p0"
            }
        ]
    }'''
    payload = json.loads(json_data)

    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['fabric', 'priv', 'set-template',
                                 'create', 'test.json', '--quiet'])
    # print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/{}/priv/set-template'.format(url, basePath)
    assert data['body'] == payload

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration(cli_runner, rest_mock):
    """ Test `cray fabric fabric-configuration` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration'])
    assert result.exit_code == 0

    outputs = [
        "cli fabric fabric-configuration [OPTIONS] COMMAND [ARGS]...",
        "lldp",
        "sweep-rate",
        "agent-timeout",
        "telemetry",
        "list",
        "update"
    ]

    for out in outputs:
        assert out in result.output

    # test `cray fabric fabric-configuration list`
    # REST: `GET /fabric-configuration`
    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'list'])
    assert result.exit_code == 0
    print(result.output)

    # test `cray fabric fabric-configuration update`
    # REST: `PUT /fabric-configurtion`
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'update',
                                 '--mtu', '3000'])
    assert result.exit_code == 0
    # print(result.output)

    data = json.loads(result.output)
    # print(data)

    assert data['url'] == '{}/{}/fabric-configuration'.format(url, basePath)
    assert data['method'] == 'PUT'
    assert data['body'] == {'mtu':3000}

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_lldp(cli_runner, rest_mock):
    """Text `cray fabric fabric-configuration lldp` with valid params """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'lldp'])
    assert result.exit_code == 0
    outputs = [
        "cli fabric fabric-configuration lldp [OPTIONS] COMMAND [ARGS]...",
        "list",
        "update"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_lldp_list(cli_runner, rest_mock):
    """ Test `GET /fabric-configuration/lldp` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'lldp', 'list'])
    # print(result.output)
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'GET'
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_lldp_update(cli_runner, rest_mock):
    """ Test `PUT /fabric-configuration/lldp update --enable true` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'lldp', 'update',
                                 '--enable', True])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['body'] == {'enable': True}

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_sweep_rate(cli_runner, rest_mock):
    """ Test `cray fabric fabric-configuration sweep-rate` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'sweep-rate'])
    assert result.exit_code == 0

    outputs = [
        "cli fabric fabric-configuration sweep-rate [OPTIONS] COMMAND [ARGS]...",
        "list",
        "update"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_sweep_rate_list(cli_runner, rest_mock):
    """ Test `GET /fabric-configuration/sweep-rate` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'sweep-rate', 'list'])
    # print(result.output)
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'GET'
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_sweep_rate_update(cli_runner, rest_mock):
    """ Test `PUT /fabric-configuration/sweep-rate update --value 30` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'sweep-rate', 'update',
                                 '--value', '30'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['body'] == {'value':30}

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_agent_timeout(cli_runner, rest_mock):
    """ Test `cray fabric fabric-configuration agent-timeout` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'agent-timeout'])
    assert result.exit_code == 0

    outputs = [
        "cli fabric fabric-configuration agent-timeout [OPTIONS] COMMAND [ARGS]...",
        "list",
        "update"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_agent_timeout_list(cli_runner, rest_mock):
    """ Test `GET /fabric-configuration/agent-timeout` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'agent-timeout', 'list'])
    # print(result.output)
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'GET'
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_agent_timeout_update(cli_runner, rest_mock):
    """ Test `PUT /fabric-configuration/agent-timeout update --value 30` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'agent-timeout', 'update',
                                 '--value', '30'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['body'] == {'value':30}

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_telemetry(cli_runner, rest_mock):
    """ Test `cray fabric fabric-configuration telemetry` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'telemetry'])
    assert result.exit_code == 0

    outputs = [
        "cli fabric fabric-configuration telemetry [OPTIONS] COMMAND [ARGS]...",
        "list",
        "update"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_telemetry_list(cli_runner, rest_mock):
    """ Test `GET /fabric-configuration/telemetry` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'telemetry', 'list'])
    # print(result.output)
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'GET'
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_fabric_configuration_telemetry_update(cli_runner, rest_mock):
    """ Test `PUT /fabric-configuration/telemetry` with valid params """

    json_data = '''{
        "counters": {
            "values": [
                "abcd",
                "efgh"
            ]
        },
        "periodicity": {
            "value": 24
        },
        "locality": {
            "enable": true
        },
        "collector": {
            "value": "value"
        },
        "statistics": {
            "values": [
                "abcd",
                "efgh"
                ]
            }
        }'''
    payload = json.loads(json_data)

    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'fabric-configuration', 'telemetry', 'update',
                                 'test.json', '--quiet'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == '{}/{}/fabric-configuration/telemetry'.format(url, basePath)
    assert data['body'] == payload

# pylint: disable=redefined-outer-name
def test_fabric_port_links(cli_runner, rest_mock):
    """ Test `cray fabric port-links` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'port-links'])
    assert result.exit_code == 0
    # print(result.output)

    outputs = [
        "cli fabric port-links [OPTIONS] COMMAND [ARGS]...",
        "list",
    ]

    for out in outputs:
        assert out in result.output

    # Test `cray fabric port-links list`
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'port-links', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_port_sets(cli_runner, rest_mock):
    """ Test `cray fabric port-sets` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'port-sets'])
    assert result.exit_code == 0
    # print(result.output)

    outputs = [
        "cli fabric port-sets [OPTIONS] COMMAND [ARGS]...",
        "config",
        "loopback",
        "status",
        "create",
        "delete",
        "describe",
        "list",
        "update"
    ]

    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_list(cli_runner, rest_mock):
    """ Test `cray fabric port-sets list` with valid params
        REST: `GET /port-sets`
    """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'port-sets', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_create(cli_runner, rest_mock):
    """ Test `cray fabric port-sets create` with valid params
        REST: `POST /port-sets`
    """
    json_data = '''{
        "name": "my-port-sets",
        "ports": [
            "x16c3r4j7p0",
            "x16c3r4j7p1"
        ]
    }'''
    payload = json.loads(json_data)
    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    runner, cli, config = cli_runner
    url = config['default']['hostname']
    result = runner.invoke(cli, ['fabric', 'port-sets', 'create',
                                 'test.json', '--quiet'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/{}/port-sets'.format(url, basePath)
    assert data['body'] == payload

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_describe(cli_runner, rest_mock):
    """ Test `cray fabric port-sets describe {name}` with valid params
        REST: `GET /port-sets/{name}`
    """
    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'port-sets', 'describe', 'my-port-set'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/{}/port-sets/my-port-set'.format(url, basePath)


# pylint: disable=redefined-outer-name
def test_fabric_port_sets_update(cli_runner, rest_mock):
    """ Test `cray fabric port-sets update {name}` with valid params
        REST: `PUT /port-sets/{name}`
    """
    runner, cli, config = cli_runner
    url = config['default']['hostname']

    json_data = '''{
        "ports": [
            "x16c3r4j7p0",
            "x16c3r4j7p1"
        ]
    }'''
    payload = json.loads(json_data)
    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['fabric', 'port-sets', 'update',
                                 'test.json', 'my-port-set'])
    assert result.exit_code == 0

    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == '{}/{}/port-sets/my-port-set'.format(url, basePath)

    assert data['body'] == payload


# pylint: disable=redefined-outer-name
def test_fabric_port_sets_delete(cli_runner, rest_mock):
    """ Test `cray fabric port-sets delete {name}` with valid params
        REST: `DELETE /port-sets/{name}`
    """
    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'port-sets', 'delete', 'my-port-set'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/{}/port-sets/my-port-set'.format(url, basePath)
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_config(cli_runner, rest_mock):
    """ Test `cray fabric port-sets config` with valid params
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'port-sets', 'config'])

    outputs = [
        "cli fabric port-sets config [OPTIONS] COMMAND [ARGS]...",
        "list",
        "update"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_config_list(cli_runner, rest_mock):
    """ Test `cray fabric port-sets config list {name}` with valid params
        REST: `GET /port-sets/{name}/config`
    """
    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'port-sets', 'config',
                                 'list', 'my-port-set'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/{}/port-sets/my-port-set/config'.format(url, basePath)
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_config_update(cli_runner, rest_mock):
    """ Test `cray fabric port-sets config update {file} {name}` with valid params
        REST: `PUT /port-sets/{name}/config`
    """
    json_data = '''{
        "autoneg":true,
        "enable": true,
        "flowControl": {
            "tx": true,
            "rx": true
        },
        "speed": "100"
    }'''
    payload = json.loads(json_data)
    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'port-sets', 'config',
                                 'update', 'test.json', 'my-port-set'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == '{}/{}/port-sets/my-port-set/config'.format(url, basePath)

    assert data['body'] == payload

# pylint: disable=redefined-outer-name
def test_fabric_ports_config(cli_runner, rest_mock):
    """ Test `cray fabric ports config` with valid params
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'ports', 'config'])

    outputs = [
        "cli fabric ports config [OPTIONS] COMMAND [ARGS]...",
        "list",
        "update"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_ports_config_list(cli_runner, rest_mock):
    """ Test `cray fabric ports config list {xname}` with valid params
        REST: `GET /ports/{xname}/config`
    """
    runner, cli, config = cli_runner
    url = config['default']['hostname']
    print("$$$$$$  test_fabric_ports_config_list $$$$")
    result = runner.invoke(cli, ['fabric', 'ports', 'config',
                                 'list', 'x16c3r4j7p0'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/{}/ports/x16c3r4j7p0/config'.format(url, basePath)
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_ports_config_update(cli_runner, rest_mock):
    """ Test `cray fabric ports config update {file} {xname}` with valid params
        REST: `PUT /ports/{xname}/config`
    """
    json_data = '''{
        "autoneg":true,
        "enable": true,
        "flowControl": {
            "tx": true,
            "rx": true
        },
        "speed": "100"
    }'''

    payload = json.loads(json_data)
    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'ports', 'config',
                                 'update', 'test.json', 'x16c3r4j7p0'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == '{}/{}/ports/x16c3r4j7p0/config'.format(url, basePath)

    assert data['body'] == payload

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_loopback(cli_runner, rest_mock):
    """ Test `cray fabric port-sets loopback` with valid params
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'port-sets', 'loopback'])

    outputs = [
        "cli fabric port-sets loopback [OPTIONS] COMMAND [ARGS]...",
        "update"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_loopback_update(cli_runner, rest_mock):
    """ Test `cray fabric port-sets loopback update --loopback local {name}`
        REST: `PUT /port-sets/{name}/loopback`
    """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'port-sets', 'loopback',
                                 'update', 'my-port-set', '--loopback', 'local'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['body'] == {"loopback": "local"}

# pylint: disable=redefined-outer-name
def test_fabric_ports_loopback(cli_runner, rest_mock):
    """ Test `cray fabric ports loopback` with valid params
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'ports', 'loopback'])

    outputs = [
        "cli fabric ports loopback [OPTIONS] COMMAND [ARGS]...",
        "update"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_ports_loopback_update(cli_runner, rest_mock):
    """ Test `cray fabric ports loopback update --loopback local {name}`
        REST: `PUT /ports/{name}/loopback`
    """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'ports', 'loopback',
                                 'update', 'my-ports-set', '--loopback', 'local'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['body'] == {"loopback": "local"}

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_status(cli_runner, rest_mock):
    """ Test `cray fabric port-sets status` with valid params
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'port-sets', 'status'])

    outputs = [
        "cli fabric port-sets status [OPTIONS] COMMAND [ARGS]...",
        "list",
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_port_sets_status_list(cli_runner, rest_mock):
    """ Test `cray fabric port-sets status list` with valid params
        REST: GET /port-sets/{name}/status
    """
    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'port-sets', 'status',
                                 'list', 'my-port-set'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/{}/port-sets/my-port-set/status'.format(url, basePath)
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_ports_status(cli_runner, rest_mock):
    """ Test `cray fabric ports status` with valid params
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'ports', 'status'])

    outputs = [
        "cli fabric ports status [OPTIONS] COMMAND [ARGS]...",
        "list",
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_ports_status_list(cli_runner, rest_mock):
    """ Test `cray fabric ports status list` with valid params
        REST: GET /ports/{name}/status
    """
    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'ports', 'status',
                                 'list', 'x16c3r4j7p0'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/{}/ports/x16c3r4j7p0/status'.format(url, basePath)
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_switch_xname_lldp_feature_flag(cli_runner, rest_mock):
    """ Test `cray fabric switch lldp feature-flag` with valid params
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fabric', 'switch', 'lldp', 'feature-flag'])

    outputs = [
        "cli fabric switch lldp feature-flag [OPTIONS] COMMAND [ARGS]...",
        # cli_hidden, list and update won't show up in help
        # "list",
        # "update"
    ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_fabric_switch_xname_lldp_feature_flag_list(cli_runner, rest_mock):
    """ Test `cray fabric switch lldp feature-flag list {xname}` with valid params
        REST: GET /switch/{xname}/lldp/feature-flag
    """
    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'switch', 'lldp', 'feature-flag',
                                 'list', 'x1000c0r7b0'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/{}/switch/x1000c0r7b0/lldp/feature-flag'.format(url, basePath)
    assert 'body' not in data

# pylint: disable=redefined-outer-name
def test_fabric_switch_xname_lldp_feature_flag_update(cli_runner, rest_mock):
    """ Test `cray fabric switch lldp feature-flag update {file} {xname}` with valid params
        REST: `PUT /switch/{name}/lldp/feature-flag`
    """
    json_data = '''{
        "featureFlag": [ "defaults" ]
    }'''
    payload = json.loads(json_data)
    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    runner, cli, config = cli_runner
    url = config['default']['hostname']

    result = runner.invoke(cli, ['fabric', 'switch', 'lldp', 'feature-flag',
                                 'update', 'test.json', 'x1000c0r7b0'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == '{}/{}/switch/x1000c0r7b0/lldp/feature-flag'.format(url, basePath)

    assert data['body'] == payload
