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

from cray import utils


def test_utils_merge_dict():
    """ Test `cray init` for creating the default configuration """
    d1 = {'foo': {'bar': 'zzz'}}
    d2 = {'foo': {'bar': 'yyy'}}
    new_dict = utils.merge_dict(d1, d2)
    assert new_dict['foo']['bar'] == 'yyy'


def test_utils_merge_dict_nested_dict():
    """ Test `cray init` for creating the default configuration """
    d1 = {'foo': {'bar': 'zzz'}}
    d2 = {'foo': {'bar': {'oh': 'no'}}}
    new_dict = utils.merge_dict(d1, d2)
    assert new_dict['foo']['bar'] == {'oh': 'no'}


def test_utils_merge_dict_nested_dict_to_str():
    """ Test `cray init` for creating the default configuration """
    d1 = {'foo': {'bar': {'oh': 'no'}}}
    d2 = {'foo': {'bar': 'ohno'}}
    with pytest.raises(ValueError):
        utils.merge_dict(d1, d2)


def test_utils_merge_dict_new_dict():
    """ Test `cray init` for creating the default configuration """
    d1 = {'foo': {'bar': {'oh': 'no'}}}
    d2 = {'foo': {'new': 'bar'}}
    new_dict = utils.merge_dict(d1, d2)
    assert new_dict['foo'] == {'bar': {'oh': 'no'}, 'new': 'bar'}


def test_utils_delete_keys_from_dict():
    """ Test `cray init` for creating the default configuration """
    d1 = {'foo': {'bar': {'oh': 'no'}}}
    utils.delete_keys_from_dict(d1, ['foo', 'bar', 'oh'])
    assert d1['foo']['bar'].get('oh') is None
