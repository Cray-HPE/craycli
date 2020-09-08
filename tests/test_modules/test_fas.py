""" Test the fas module."""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument
import json
import os

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock

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
        "images"
        ]
    for out in outputs:
        assert out in result.output

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


