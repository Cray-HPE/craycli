"""
test_aprun.py - Functional tests for aprun module
Copyright 2020 Cray Inc. All Rights Reserved.
"""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument
import json

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock


def test_cray_aprun_help(cli_runner, rest_mock):
    """ Test `cray aprun --help` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['aprun', '--help'])

    assert result.exit_code == 0
    assert 'Usage: cli aprun [OPTIONS] EXECUTABLE [ARGS]...' in result.output
    assert 'Run an application using the Parallel Application Launch Service' in result.output


def test_cray_aprun_missing_param(cli_runner, rest_mock):
    """ Test cray aprun without an executable """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['aprun'])

    assert result.exit_code == 2
    assert 'Usage: cli aprun [OPTIONS] EXECUTABLE [ARGS]...' in result.output
    assert 'Error: Missing argument' in result.output
    assert "EXECUTABLE" in result.output
