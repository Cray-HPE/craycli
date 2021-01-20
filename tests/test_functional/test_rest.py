""" Test the main CLI command (`cray`) and options.

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
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument, import-error
import pytest
from ..utils.runner import cli_runner


def test_cray_connection_error(cli_runner):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    host = 'https://localhost'
    runner.invoke(cli, ['config', 'set', 'core', 'hostname={}'.format(host)])
    # running uas list just to force the connection failure
    result = runner.invoke(cli, ['uas', 'list'])
    print(result.output)
    assert result.exit_code == 2

    outputs = [
        "Error: Unable to connect to cray. Please verify your cray hostname:",
        "cray config get core.hostname",
        "cray config set core hostname=cray_hostname"
        ]
    for out in outputs:
        assert out in result.output


def test_cray_http_error(cli_runner):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    host = 'http://localhost'
    runner.invoke(cli, ['config', 'set', 'core', 'hostname={}'.format(host)])

    # running uas list just to force the connection failure
    result = runner.invoke(cli, ['uas', 'list', '-vvvvvvv'])
    print(result.output)
    assert result.exit_code == 2

    outputs = [
        "You've configured your cray hostname with http. Please " +
        "reconfigure for https."
        ]
    for out in outputs:
        assert out in result.output
