""" Test the main CLI command (`cray`) and options."""
# pylint: disable=redefined-outer-name, unused-import, invalid-name
# pylint: disable=too-many-arguments, unused-variable, import-error
import os
import json

import click
import toml
import requests
import pytest

from cray import formatting


def test_formatting_format_results():
    """ Test `cray init` for creating the default configuration """
    d1 = {'foo': {'bar': {'oh': 'no'}}}
    result = formatting.format_result(d1, 'json')
    assert result == json.dumps(d1, indent=2)


def test_formatting_format_results_toml():
    """ Test `cray init` for creating the default configuration """
    d1 = {'foo': {'bar': {'oh': 'no'}}}
    result = formatting.format_result(d1, 'toml')
    assert result == toml.dumps(d1)


def test_formatting_format_results_toml_list():
    """ Test `cray init` for creating the default configuration """
    d1 = [{'bar': {'oh': 'no'}}]
    result = formatting.format_result(d1, 'toml')
    assert result == toml.dumps({'results': d1})


def test_formatting_format_results_yaml():
    """ Test `cray init` for creating the default configuration """
    d1 = {'foo': {'bar': {'oh': 'no'}}}
    expect = 'foo:\n  bar:\n    oh: no\n'
    result = formatting.format_result(d1, 'yaml')
    assert result == expect


def test_formatting_format_results_raises():
    """ Test `cray init` for creating the default configuration """
    def temp():  # pylint: disable=missing-docstring
        return True
    d1 = {'foo': {'bar': {'oh': temp}}}
    with pytest.raises(click.ClickException):
        formatting.format_result(d1, 'json')
