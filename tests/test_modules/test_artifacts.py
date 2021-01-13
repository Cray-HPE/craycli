"""
Tests for artifacts CLI subcommand (`cray artifacts/buckets`) and options.
"""
from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name
def test_cray_buckets_help_output(cli_runner):
    """ Test cray buckets help output """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['artifacts'])
    assert result.exit_code == 0

    outputs = [
        "buckets",
        "list",
        "create",
        "describe",
        "get",
        "delete",
    ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_artifacts_help_output(cli_runner):
    """ Test cray artifacts help output """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['artifacts'])
    assert result.exit_code == 0

    outputs = [
        "buckets",
        "list",
        "create",
        "describe",
        "get",
        "delete",
    ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_artifacts_list(cli_runner):
    """ Test cray artifacts list ... """
    runner, cli, _ = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'list'])
    assert result.exit_code == 2


# pylint: disable=redefined-outer-name
def test_cray_artifacts_create(cli_runner):
    """ Test cray artifacts create  ... """
    runner, cli, _ = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'create', ])
    assert result.exit_code == 2


# pylint: disable=redefined-outer-name
def test_cray_artifacts_describe(cli_runner):
    """ Test cray artifacts describe  ... """
    runner, cli, _ = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'describe', ])
    assert result.exit_code == 2


# pylint: disable=redefined-outer-name
def test_cray_artifacts_get(cli_runner):
    """ Test cray artifacts get  ... """
    runner, cli, _ = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'get', ])
    assert result.exit_code == 2
