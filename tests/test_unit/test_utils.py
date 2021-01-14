""" Test the main CLI command (`cray`) and options."""
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
