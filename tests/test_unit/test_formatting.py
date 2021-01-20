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
