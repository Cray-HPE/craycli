""" Test the main CLI command (`cray`) and options."""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-variable
import json
import os

from ..utils.runner import cli_runner
from ..utils.pets import pets
from ..utils.rest import rest_mock


def test_cray_help(cli_runner):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    outputs = [
        "Options:", "Groups:", "Commands:", "init", "auth", "config"
        ]
    for txt in outputs:
        assert txt in result.output


#pylint: disable=unused-argument
def test_cray_upper_hidden(cli_runner, pets):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pets', '--help'])
    print(result.output)
    assert result.exit_code == 0
    outputs = [
        "upperCase"
        ]
    for txt in outputs:
        assert txt in result.output
    not_outputs = [
        "UpperCase"
        ]
    for txt in not_outputs:
        assert txt not in result.output


#pylint: disable=unused-argument
def test_cray_nested_upper_hidden(cli_runner, pets):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pets', 'upperCase', '--help'])
    print(result.output)
    assert result.exit_code == 0
    outputs = [
        "test"
        ]
    for txt in outputs:
        assert txt in result.output
    not_outputs = [
        "Test",
        "(DEPRECATED)"
        ]
    for txt in not_outputs:
        assert txt not in result.output


#pylint: disable=unused-argument
def test_cray_deprecated_upper(cli_runner, pets):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pets', 'UpperCase', '--help'])
    print(result.output)
    assert result.exit_code == 0
    outputs = [
        "(DEPRECATED)"
        ]
    for txt in outputs:
        assert txt in result.output
