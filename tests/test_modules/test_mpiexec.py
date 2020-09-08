"""
test_mpiexec.py - Functional tests for mpiexec module
Copyright 2019 Cray Inc. All Rights Reserved.
"""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument
import json

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock


def test_cray_mpiexec_help(cli_runner, rest_mock):
    """ Test `cray mpiexec --help` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['mpiexec', '--help'])

    assert result.exit_code == 0
    assert 'Usage: cli mpiexec [OPTIONS] EXECUTABLE [ARGS]...' in result.output
    assert 'Run an application using the Parallel Application Launch Service' in result.output


def test_cray_mpiexec_missing_param(cli_runner, rest_mock):
    """ Test cray mpiexec without an executable """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['mpiexec'])

    assert result.exit_code == 2
    outputs = [
        "Usage: cli mpiexec [OPTIONS] EXECUTABLE [ARGS]...",
        "Error: Missing argument",
        "EXECUTABLE"
    ]
    for out in outputs:
        assert out in result.output
