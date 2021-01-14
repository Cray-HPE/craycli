""" Test the fas module."""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments, unused-argument
from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name
def test_cray_fas_base(cli_runner, rest_mock):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas'])
    assert result.exit_code == 0

    outputs = [
        # "cray fas [OPTIONS] COMMAND [ARGS]...",
        "fas",
        "actions",
        "snapshots",
        "operations",
        "service",
        "images"
        ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_cray_fas_describe_actions_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'actions', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "ACTIONID"
        ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_cray_fas_describe_images_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'images', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "IMAGEID"
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_fas_describe_snapshots_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'snapshots', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "NAME"
        ]
    for out in outputs:
        assert out in result.output


def test_cray_fas_describe_operations_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'operations', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "OPERATIONID"
        ]
    for out in outputs:
        assert out in result.output


def test_cray_fas_describe_actions_groups_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'actions'])
    assert result.exit_code == 0
    outputs = [
        'Groups:',
        "operations",
        "status",
        "instance"
        ]
    for out in outputs:
        assert out in result.output


def test_cray_fas_describe_actions_status_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'actions', 'status', 'list'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "ACTIONID"
        ]
    for out in outputs:
        assert out in result.output
