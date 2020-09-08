""" Test the main CLI command (`cray`) and options."""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument
import json
import os
import re

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock

basePath = 'apis/network/v1'

def test_cray_nms_network_base(cli_runner, rest_mock):
    """ Test `cray network` to make sure the expected commands are available """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network'])
    assert result.exit_code == 0

    outputs = [
        "Network Manager REST API",
        "networks",
        "nics",
        "list",
        "network [OPTIONS] COMMAND [ARGS]..."
    ]
    for out in outputs:
        assert out in result.output

    # GET /lswitches
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, 'lswitches'])+"$", data['url']) != None
    assert data['method'] == 'GET'
    assert not 'body' in data

def test_cray_nms_nics(cli_runner, rest_mock):
    """ Test `cray network nics` to make sure the expected commands are available
        This command is currently a stub, and not implemented.
        So there is no "function" to test beyond existance at the moment.
    """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'nics'])
    assert result.exit_code == 0

    outputs = [
        "Usage: cli network nics [OPTIONS] COMMAND [ARGS]...",
        "list"
    ]
    for out in outputs:
        assert out in result.output

    #
    # Check the request URL and Body
    #

    # GET /lswitches/singleFabric/nics
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'nics', 'list', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, 'lswitches/singleFabric/nics'])+"$",
                    data['url']) != None
    assert data['method'] == 'GET'
    assert not 'body' in data


def test_cray_nms_networks(cli_runner, rest_mock):
    """ Test `cray network networks` to make sure the expected commands are available
        This command is currently a stub, and not implemented.
        So there is no "function" to test beyond existence at the moment.
    """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks'])
    assert result.exit_code == 0

    outputs = [
        "Usage: cli network networks [OPTIONS] COMMAND [ARGS]...",
        "dnsservices",
        "nics",
        "create",
        "delete",
        "describe",
        "list"
    ]
    for out in outputs:
        assert out in result.output

    #
    # Check the request URL and Body
    #

    # POST /lswitches/singleFabric/networks only required
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'create', "--vlan-id", "100",
                                 "--net-cidr", "10.0.1.0/24", "--name", "net1",
                                 "singleFabric"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, 'lswitches/singleFabric/networks'])+"$",
                    data['url']) != None
    assert data['method'] == 'POST'
    assert data['body'] == {'vlanID':100, 'netCIDR': '10.0.1.0/24', 'name': 'net1'}
    # Check the response from server ... no mock available

    # POST /lswitches/singleFabric/networks with optionals
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'create', "--vlan-id", "100",
                                 "--net-cidr", "10.0.1.0/24", "--name", "net1",
                                 "--nic-xnames", 'nic1, nic2', "--ipv6-prefix",
                                 "ipPrefix", "singleFabric"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, 'lswitches/singleFabric/networks'])+"$",
                    data['url']) != None
    assert data['method'] == 'POST'
    assert data['body'] == {'vlanID':100, 'netCIDR': '10.0.1.0/24', 'name': 'net1',
                            'nicXnames': ["nic1", "nic2"], 'ipv6Prefix': 'ipPrefix'}
    # Check the response from server ... no mock available

    # GET /lswitches/singleFabric/networks
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'list', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, 'lswitches/singleFabric/networks'])+"$",
                    data['url']) != None
    assert data['method'] == 'GET'
    assert not 'body' in data

    # GET /lswitches/singleFabric/networks/{netName}
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'describe', 'net1',
                                 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, 'lswitches/singleFabric/networks/net1'])+"$",
                    data['url']) != None
    assert data['method'] == 'GET'
    assert not 'body' in data
    # Check the response from server ... no mock available

    # DELETE /lswitches/singleFabric/networks/{netName}
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'delete', 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, 'lswitches/singleFabric/networks/net1'])+"$",
                    data['url']) != None
    assert data['method'] == 'DELETE'
    assert not 'body' in data


def test_cray_nms_networks_nics(cli_runner, rest_mock):
    """ Test `cray network networks nics` to make sure the expected commands are available
        This command is currently a stub, and not implemented.
        So there is no "function" to test beyond existence at the moment.
    """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'nics'])
    assert result.exit_code == 0

    outputs = [
        "Usage: cli network networks nics [OPTIONS] COMMAND [ARGS]...",
        "create",
        "delete",
        "describe",
        "list"
    ]
    for out in outputs:
        assert out in result.output

    #
    # Check the request URL and Body
    #

    nicsPath = 'lswitches/singleFabric/networks/net1/nics'

    # POST /lswitches/singleFabric/networks/{netName}/nics
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'nics', 'create',
                                 '--nic-xnames', 'nic1, nic2', 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, nicsPath])+"$", data['url']) != None
    assert data['method'] == 'POST'
    assert data['body'] == {'nicXnames': ["nic1", "nic2"]}
    # Check the response from server ... no mock available

    # GET /lswitches/singleFabric/networks/{netName}/nics
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'nics', 'list',
                                 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, nicsPath])+"$", data['url']) != None
    assert data['method'] == 'GET'
    assert not 'body' in data
    # Check the response from server ... no mock available

    # DELETE /lswitches/singleFabric/networks/{netName}/nics
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'nics', 'delete',
                                 '--nic-xnames', 'nic1, nic2', 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, nicsPath])+"$", data['url']) != None
    assert data['method'] == 'DELETE'
    assert data['body'] == {'nicXnames': ["nic1", "nic2"]}
    # Check the response from server ... no mock available

    # GET /lswitches/singleFabric/networks/{netName}/nics/{nicXname}
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'nics', 'describe', 'nic1',
                                 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, nicsPath + '/nic1'])+"$", data['url']) != None
    assert data['method'] == 'GET'
    assert not 'body' in data
    # Check the response from server ... no mock available

    # DELETE /lswitches/singleFabric/networks/{netName}/nics/{nicXname}
    #runner, cli, _ = cli_runner
    #result = runner.invoke(cli, ['network', 'networks', 'nics', 'delete', 'nic1',
    #                             'net1', 'singleFabric'])
    #assert result.exit_code == 0
    #data = json.loads(result.output)
    #assert re.match('/'.join(['(.*)', basePath, nicsPath + '/nic1'])+"$", data['url']) != None
    #assert data['method'] == 'DELETE'

    # Check the response from server ... no mock available


def test_cray_nms_networks_dnsservices(cli_runner, rest_mock):
    """ Test `cray network networks dnsservices` to make sure the expected commands are available
        This command is currently a stub, and not implemented.
        So there is no "function" to test beyond existence at the moment.
    """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'dnsservices'])
    assert result.exit_code == 0

    outputs = [
        "Usage: cli network networks dnsservices [OPTIONS] COMMAND [ARGS]...",
        "hosts",
        "list"
    ]
    for out in outputs:
        assert out in result.output

    dnsPath = 'lswitches/singleFabric/networks/net1/dnsservices'

    #
    # Check the request URL and Body
    #

    # GET /lswitches/singleFabric/networks/{netName}/dnsservices
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'dnsservices', 'list',
                                 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, dnsPath])+"$", data['url']) != None
    assert data['method'] == 'GET'
    assert not 'body' in data
    # Check the response from server ... no mock available


def test_cray_nms_networks_dnsservices_hosts(cli_runner, rest_mock):
    """ Test `cray network networks dnsservices hosts` to make sure the expected
        commands are available.
        This command is currently a stub, and not implemented.
        So there is no "function" to test beyond existence at the moment.
    """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'dnsservices', 'hosts'])
    assert result.exit_code == 0

    outputs = [
        "Usage: cli network networks dnsservices hosts [OPTIONS] COMMAND [ARGS]...",
        "create",
        "delete",
        "describe",
        "list",
        "replace",
        "update"
    ]
    for out in outputs:
        assert out in result.output

    dnsHostPath = 'lswitches/singleFabric/networks/net1/dnsservices/dns1/hosts'

    # GET /lswitches/singleFabric/networks/{netName}/dnsservices/{instanceId}/hosts
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'dnsservices', 'hosts',
                                 'list', 'dns1', 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, dnsHostPath])+"$", data['url']) != None
    assert data['method'] == 'GET'
    assert not 'body' in data
    # Check the response from server ... no mock available

    # POST /lswitches/singleFabric/networks/{netName}/dnsservices/{instanceId}/hosts
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'dnsservices', 'hosts',
                                 'create', '--host-ip', 'ip1', '--host-name',
                                 'host1', 'dns1', 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, dnsHostPath])+"$", data['url']) != None
    assert data['method'] == 'POST'
    assert data['body'] == {'hostIP': 'ip1', 'hostName': 'host1'}
    # Check the response from server ... no mock available

    # GET /lswitches/singleFabric/networks/{netName}/dnsservices/{instanceId}/hosts/{hostEntryId}
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'dnsservices', 'hosts',
                                 'describe', 'ip1', 'dns1', 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, dnsHostPath + '/ip1'])+"$", data['url']) != None
    assert data['method'] == 'GET'
    assert not 'body' in data
    # Check the response from server ... no mock available

    # DELETE /lswitches/singleFabric/networks/{netName}/dnsservices/{instanceId}/hosts/{hostEntryId}
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'dnsservices', 'hosts',
                                 'delete', 'ip1', 'dns1', 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, dnsHostPath + '/ip1'])+"$", data['url']) != None
    assert data['method'] == 'DELETE'
    assert not 'body' in data
    # Check the response from server ... no mock available

    # PUT /lswitches/singleFabric/networks/{netName}/dnsservices/{instanceId}/hosts/{hostEntryId}
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'dnsservices', 'hosts',
                                 'replace', '--host-ip', 'ip1', '--host-name', 'host1',
                                 '--host-aliases', 'alias1, alias2', 'ip1', 'dns1',
                                 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, dnsHostPath + '/ip1'])+"$", data['url']) != None
    assert data['method'] == 'PUT'
    assert data['body'] == {'hostIP': 'ip1', 'hostName': 'host1',
                            'hostAliases':["alias1", "alias2"]}
    # Check the response from server ... no mock available

    # PATCH /lswitches/singleFabric/networks/{netName}/dnsservices/{instanceId}/hosts/{hostEntryId}
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['network', 'networks', 'dnsservices', 'hosts',
                                 'update', '--host-ip', 'ip1', '--host-aliases',
                                 'alias1, alias2', 'ip1', 'dns1', 'net1', 'singleFabric'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert re.match('/'.join(['(.*)', basePath, dnsHostPath + '/ip1'])+"$", data['url']) != None
    assert data['method'] == 'PATCH'
    assert data['body'] == {'hostIP': 'ip1', 'hostAliases':["alias1", "alias2"]}
    # Check the response from server ... no mock available
