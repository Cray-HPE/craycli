""" Test the main CLI command (`cray`) and options."""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments, unused-argument
import json

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import


# pylint: disable=redefined-outer-name
def test_cray_badger_base(cli_runner, rest_mock):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['badger'])
    assert result.exit_code == 0

    outputs = [
        # "cray badger [OPTIONS] COMMAND [ARGS]...",
        "Badger",
        "applications",
        "sessions",
        "suites"
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_badger_create_suite(cli_runner, rest_mock):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=too-many-locals
    runner, cli, opts = cli_runner
    name = 'someName'
    description = 'someDescription'
    config = opts['default']
    hostname = config['hostname']
    app_id_0 = "c3370eca-e3af-4c6f-80ae-09bc93d5707b"
    app_id_1 = "f3a3d357-65c9-49f7-ae8d-ab98b265d1bc"
    applicationOrder = [
        {"applicationID": app_id_0},
        {"applicationID": app_id_1}]
    result = runner.invoke(cli, ['badger', 'suites', 'create', '--name', name,
                                 '--description', description,
                                 '--application-order-application-id',
                                 ",".join([app_id_0, app_id_1])])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    assert data.get('body')
    body = data.get('body')
    assert body.get('description') == description
    applicationOrderFromBody = body.get('applicationOrder')

    print(applicationOrder)
    print(applicationOrderFromBody)

    assert applicationOrder == applicationOrderFromBody


    uri = data['url'].split(hostname)[-1]
    assert uri == '/apis/badger-api/v1/suites'


# pylint: disable=redefined-outer-name
def test_cray_badger_create_application(cli_runner, rest_mock):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, opts = cli_runner
    name = 'someName'
    link = 'someURL'
    config = opts['default']

    hostname = config['hostname']
    result = runner.invoke(cli, ['badger', 'applications', 'create',
                                 '--link-to-exe', link, '--name', name])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    assert data.get('body')
    body = data.get('body')
    assert body.get('linkToExe') == link
    assert body.get('name') == name
    uri = data['url'].split(hostname)[-1]
    assert uri == '/apis/badger-api/v1/applications'


# pylint: disable=redefined-outer-name
def test_cray_badger_describe_applications_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['badger', 'applications', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "APPLICATIONID"
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_badger_describe_suites_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an suite """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['badger', 'suites', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "SUITEID"
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_badger_describe_sessions_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an sessions """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['badger', 'sessions', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "SESSIONID"
        ]
    for out in outputs:
        assert out in result.output
