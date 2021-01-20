"""
test_mpiexec.py - Functional tests for mpiexec module

MIT License

(C) Copyright [2020] Hewlett Packard Enterprise Development LP

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
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
