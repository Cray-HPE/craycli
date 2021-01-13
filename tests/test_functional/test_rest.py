""" Test the main CLI command (`cray`) and options."""
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
