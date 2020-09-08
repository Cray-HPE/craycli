"""
Tests for artifacts CLI subcommand (`cray artifacts/buckets`) and options.
"""
import json

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock


def test_cray_buckets_help_output(cli_runner):
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


def test_cray_artifacts_help_output(cli_runner):
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


def test_cray_artifacts_list(cli_runner):
    """ Test cray artifacts list ... """
    runner, cli, config = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'list'])
    assert result.exit_code == 2


def test_cray_artifacts_create(cli_runner):
    """ Test cray artifacts create  ... """
    runner, cli, config = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'create', ])
    assert result.exit_code == 2


def test_cray_artifacts_describe(cli_runner):
    """ Test cray artifacts describe  ... """
    runner, cli, config = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'describe', ])
    assert result.exit_code == 2


def test_cray_artifacts_get(cli_runner):
    """ Test cray artifacts get  ... """
    runner, cli, config = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'get', ])
    assert result.exit_code == 2
