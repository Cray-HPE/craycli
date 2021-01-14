"""
test_mpiexec.py - Functional tests for mpiexec module
Copyright 2019 Cray Inc. All Rights Reserved.
"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments, unused-argument
from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import


# pylint: disable=redefined-outer-name
def test_cray_mpiexec_help(cli_runner, rest_mock):
    """ Test `cray mpiexec --help` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['mpiexec', '--help'])

    assert result.exit_code == 0
    assert 'Usage: cli mpiexec [OPTIONS] EXECUTABLE [ARGS]...' in result.output
    assert 'Run an application using the Parallel Application Launch Service' in result.output


# pylint: disable=redefined-outer-name
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
