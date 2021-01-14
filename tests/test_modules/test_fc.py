""" Test the fc module."""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments, unused-argument
import json

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import


# pylint: disable=redefined-outer-name
def test_fc_not_in_main_help(cli_runner, rest_mock):
    """ Test `cray --help` to make sure the fc group is hidden """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'fc' not in result.output


# pylint: disable=redefined-outer-name
def test_fc_help_info(cli_runner, rest_mock):
    """ Test `cray fc` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fc'])
    assert result.exit_code == 0

    outputs = [
        "commit",
        "config",
        "links",
        "list",
        "mtu",
        "port",
        "routing",
        "Fabric Controller Rest API",
        "cli fc [OPTIONS] COMMAND [ARGS].."
    ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_fc_routing_create_required_param(cli_runner, rest_mock):
    """ Test `cray fc` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fc', 'routing', 'init', 'create'])
    print(result.output)
    assert result.exit_code == 2

    outputs = [
        'Error: Missing argument',
        "PAYLOAD_FILE",
        'cli fc routing init create --help'
    ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_fc_routing_init_create(cli_runner, rest_mock):
    """ Test `cray fc routing init create` with valid params """

    runner, cli, config = cli_runner
    url = config['default']['hostname']
    json_data = """{
    "switches" : [
    { "grpId" : 0,
      "swcNum" : 0,
      "edgePorts" : [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
          10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
          20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
          30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
          40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
          50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
          60, 61, 62, 63 ],
      "fabricPorts" : [],
      "IP" : "x1000c0r38b0:8080" }
    ],    "links" : [
    ],    "numGroups" : 1,
    "maxNumLocalSwitches" : 1
    }"""
    payload = json.loads(json_data)

    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['fc', 'routing', 'init', 'create',
                                 'test.json', '--quiet'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/fabric/v1/switch/routing/init'.format(url)
    assert data['body'] == payload


# pylint: disable=redefined-outer-name
def test_fc_port_enable_update(cli_runner, rest_mock):
    """ Test `cray fc routing init create` with valid params """

    runner, cli, config = cli_runner
    switches = '2'
    ports = '1'
    opt3 = True
    url = config['default']['hostname']
    result = runner.invoke(cli, ['fc', 'port', 'enable', 'update',
                                 ports, switches, '--enable', opt3])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == '{}/apis/fabric/v1/switch/{}/port/{}/enable'.format(url, switches, ports)
    assert data['body'] == {
        'enable': opt3
    }
