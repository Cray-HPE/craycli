""" Test the cps module."""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments, unused-argument
import json

from urllib.parse import urlencode as get_urlencode_str

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import
from ..utils.utils import compare_urls


# pylint: disable=redefined-outer-name
def test_example_cps_help_info(cli_runner, rest_mock):
    """ Test `cray cps` to make sure the expected commands are available """

    ############################################################################
    # This example shows how to create a test that validates the outputs of
    # --help options for your module
    ############################################################################

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['cps', 'contents', '--help'])
    assert result.exit_code == 0

    outputs = [
        "create",
        "delete",
        "list",
        "cli cps contents [OPTIONS] COMMAND [ARGS].."
    ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_cps_create_s3(cli_runner, rest_mock):
    """ Test more `cray cps ` create """
    runner, cli, config = cli_runner
    opt1 = 's3://boot-images/c3b72f49-33b0-4617-b456-70c9bc8e3edb/rootfs'
    opt2 = 'dvs'
    result = runner.invoke(cli, ['cps', 'contents', 'create', '--s3path', opt1,
                                 '--transport', opt2])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    compare_urls(
        '{}/apis/v2/cps/contents'.format(config['default']['hostname']),
        data['url']
    )
    assert data['body'] == {
        "s3path":"s3://boot-images/c3b72f49-33b0-4617-b456-70c9bc8e3edb/rootfs",
        "transport":["dvs"]
    }


# pylint: disable=redefined-outer-name
def test_cray_cps_delete_s3(cli_runner, rest_mock):
    """ Test more `cray cps contents` delete artifact """
    runner, cli, config = cli_runner
    opt1 = 's3://boot-images/c3b72f49-33b0-4617-b456-70c9bc8e3edb/rootfs'
    result = runner.invoke(cli, ['cps', 'contents', 'delete', '--s3path', opt1])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    q = {'s3path':opt1}
    query = get_urlencode_str(q)
    hostname = config['default']['hostname']
    expected_url = "{0}/apis/v2/cps/contents?{1}".format(
        hostname,
        query
    )
    compare_urls(expected_url, data['url'])


# pylint: disable=redefined-outer-name
def test_cray_cps_list(cli_runner, rest_mock):
    """ Test more `cray cps ` list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['cps', 'contents', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    expected_url = '{0}/apis/v2/cps/contents'.format(config['default']['hostname'])
    compare_urls(expected_url, data['url'])


# pylint: disable=redefined-outer-name
def test_cray_cps_transports_create(cli_runner, rest_mock):
    """ Test more `cray cps transports` create """
    runner, cli, config = cli_runner
    opt1 = 'dvs'
    opt2 = 's3://boot-images/c3b72f49-33b0-4617-b456-70c9bc8e3edb/rootfs'
    result = runner.invoke(cli, ['cps', 'transports', 'create',
                                 '--transport', opt1, '--s3path', opt2])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['body']['s3path'] == opt2
    expected_url = '{}/apis/v2/cps/transports'.format(config['default']['hostname'])
    compare_urls(expected_url, data['url'])
    assert 'dvs' in data['body']['transport']


# pylint: disable=redefined-outer-name
def test_cray_cps_transports_describe(cli_runner, rest_mock):
    """ Test more `cray cps transports` describe """
    runner, cli, config = cli_runner
    opt1 = 'dvs'
    opt2 = 's3://boot-images/c3b72f49-33b0-4617-b456-70c9bc8e3edb/rootfs'
    result = runner.invoke(cli, ['cps', 'transports', 'list',
                                 '--transport', opt1, '--s3path', opt2])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    hostname = config['default']['hostname']
    q = {'s3path':opt2, 'transport':opt1}
    query = get_urlencode_str(q)
    expected_url = '{0}/apis/v2/cps/transports?{1}'.format(hostname, query)
    compare_urls(expected_url, data['url'])


# pylint: disable=redefined-outer-name
def test_cray_cps_transports_delete_transport(cli_runner, rest_mock):
    """ Test more `cray cps transports` delete transport """
    runner, cli, config = cli_runner
    opt1 = 'dvs'
    opt2 = 'c3b72f49-33b0-4617-b456-70c9bc8e3edb'
    result = runner.invoke(cli, ['cps', 'transports', 'delete',
                                 '--transport', opt1, '--s3path', opt2])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    hostname = config['default']['hostname']
    q = {'s3path':opt2, 'transport':opt1}
    query = get_urlencode_str(q)
    expected_url = '{0}/apis/v2/cps/transports?{1}'.format(hostname, query)
    compare_urls(expected_url, data['url'])


# pylint: disable=redefined-outer-name
def test_cray_cps_deployment_list(cli_runner, rest_mock):
    """ Test more `cray cps deployment` list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['cps', 'deployment', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    expected_url = '{0}/apis/v2/cps/deployment'.format(config['default']['hostname'])
    compare_urls(expected_url, data['url'])


# pylint: disable=redefined-outer-name
def test_cray_cps_deployment_list_nodes(cli_runner, rest_mock):
    """ Test more `cray cps deployment` list """
    runner, cli, config = cli_runner
    nodes = 'ncn-w001,ncn-w002'
    result = runner.invoke(cli, ['cps', 'deployment', 'list', '--nodes', nodes])
    assert result.exit_code == 0
    data = json.loads(result.output)
    q = {'nodes': nodes}
    query = get_urlencode_str(q)
    url = '{0}/apis/v2/cps/deployment?{1}'.format(config['default']['hostname'], query)
    assert data['method'] == 'GET'
    compare_urls(url, data['url'])


# pylint: disable=redefined-outer-name
def test_cray_cps_deployment_put_nodes(cli_runner, rest_mock):
    """ Test more `cray cps deployment` put nodes """
    runner, cli, config = cli_runner
    nodes = 'ncn-w001,ncn-w002'
    result = runner.invoke(cli, ['cps', 'deployment', 'update',
                                 '--nodes', nodes])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['body']['nodes'] == nodes.split(',')
    expected_url = '{}/apis/v2/cps/deployment'.format(config['default']['hostname'])
    compare_urls(expected_url, data['url'])


# pylint: disable=redefined-outer-name
def test_cray_cps_deployment_put_numpods(cli_runner, rest_mock):
    """ Test more `cray cps deployment` put numpods"""
    runner, cli, config = cli_runner
    numpods = 3
    result = runner.invoke(cli, ['cps', 'deployment', 'update',
                                 '--numpods', numpods])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['body']['numpods'] == numpods
    expected_url = '{}/apis/v2/cps/deployment'.format(config['default']['hostname'])
    compare_urls(expected_url, data['url'])


# pylint: disable=redefined-outer-name
def test_cray_cps_deployment_delete_nodes(cli_runner, rest_mock):
    """ Test more `cray cps deployment` delete nodes """
    runner, cli, config = cli_runner
    nodes = 'ncn-w001,ncn-w002'
    result = runner.invoke(cli, ['cps', 'deployment', 'delete',
                                 '--nodes', nodes])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    hostname = config['default']['hostname']
    q = {'nodes': nodes}
    query = get_urlencode_str(q)
    url = '{0}/apis/v2/cps/deployment?{1}'.format(hostname, query)
    compare_urls(url, data['url'])
