"""
test_aprun.py - Functional tests for aprun module
Copyright 2020 Cray Inc. All Rights Reserved.
"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments, unused-argument
from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import


# pylint: disable=redefined-outer-name
def test_cray_aprun_help(cli_runner, rest_mock):
    """ Test `cray aprun --help` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['aprun', '--help'])

    assert result.exit_code == 0
    assert 'Usage: cli aprun [OPTIONS] EXECUTABLE [ARGS]...' in result.output
    assert 'Run an application using the Parallel Application Launch Service' in result.output


# pylint: disable=redefined-outer-name
def test_cray_aprun_missing_param(cli_runner, rest_mock):
    """ Test cray aprun without an executable """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['aprun'])

    assert result.exit_code == 2
    assert 'Usage: cli aprun [OPTIONS] EXECUTABLE [ARGS]...' in result.output
    assert 'Error: Missing argument' in result.output
    assert "EXECUTABLE" in result.output
