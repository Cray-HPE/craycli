""" Test the main CLI command (`cray`) and options."""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument
from ..utils.runner import cli_runner
from ..utils.rest import rest_mock


def test_cray_auth(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    username = 'foo'
    password = 'bar'
    result = runner.invoke(cli, ['auth', 'login', '--username', username,
                                 '--password', password])
    print(result.output)
    assert result.exit_code == 2


def test_cray_auth_success(cli_runner, rest_mock):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner
    username = 'foo'
    password = 'bar'
    result = runner.invoke(cli, ['auth', 'login', '--username', username,
                                 '--password', password])
    print(result.output)
    assert result.exit_code == 2
    assert 'Invalid Credentials' in result.output
