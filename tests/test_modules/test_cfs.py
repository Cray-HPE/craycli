"""
Tests for Configuration Framework Service (CFS) CLI subcommand (`cray cfs`)
and options.
"""
# pylint: disable=redefined-outer-name, unused-import, invalid-name
# pylint: disable=too-many-arguments, import-error, duplicate-code
# pylint: disable=unused-argument
import json
import os

import pytest

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock


def test_cray_cfs_base(cli_runner, rest_mock):
    """ Test cray cfs base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['cfs'])
    assert result.exit_code == 0

    outputs = [
        "Configuration Framework Service",
        "Groups:",
        "sessions",
    ]
    for txt in outputs:
        assert txt in result.output


def test_cray_cfs_sessions_base(cli_runner, rest_mock):
    """ Test cray cfs sessions base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['cfs', 'sessions'])
    assert result.exit_code == 0

    outputs = [
        "Commands:",
        "create",
        "delete",
        "describe",
        "list",
    ]
    for txt in outputs:
        assert txt in result.output


def test_cray_cfs_session_delete(cli_runner, rest_mock):
    """ Test cray cfs delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['cfs', 'sessions', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/cfs/sessions/foo'.format(config['default']['hostname'])


def test_cray_cfs_session_list(cli_runner, rest_mock):
    """ Test cray cfs list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['cfs', 'sessions', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/cfs/sessions'.format(config['default']['hostname'])


def test_cray_cfs_session_describe(cli_runner, rest_mock):
    """ Test cray cfs describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['cfs', 'sessions', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/cfs/sessions/foo'.format(config['default']['hostname'])


def test_cray_cfs_session_create(cli_runner, rest_mock):
    """ Test cray cfs create ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['cfs', 'sessions', 'create', '--name', 'foo',
                                 '--clone-url', 'bar', '--branch', 'baz'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/cfs/sessions'.format(config['default']['hostname'])
    assert data['body'] == {
        'name': 'foo',
        'cloneUrl': 'bar',
        'branch': 'baz',
        'ansiblePlaybook': 'site.yml',
        'target': {'definition': 'dynamic', 'groups': []},
    }


def test_cray_cfs_session_create_full(cli_runner, rest_mock):
    """ Test cray cfs create ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['cfs', 'sessions', 'create', '--name', 'foo',
                                 '--clone-url', 'bar', '--branch', 'baz',
                                 '--ansible-playbook', 'test.yml',
                                 '--ansible-limit', 'Compute',
                                 '--ansible-config', 'default-config',
                                 '--ansible-verbosity', '1',
                                 '--target-definition', 'spec',
                                 '--target-group', 'foo', 'a, b, c',
                                 '--target-group', 'bar', 'x,y,z'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/cfs/sessions'.format(config['default']['hostname'])
    assert data['body'] == {
        'name': 'foo',
        'cloneUrl': 'bar',
        'branch': 'baz',
        'ansiblePlaybook': 'test.yml',
        'ansibleLimit': 'Compute',
        'ansibleConfig': 'default-config',
        'ansibleVerbosity': 1,
        'target': {
            'definition': 'spec',
            'groups': [
                {'name': 'foo', 'members': ['a', 'b', 'c']},
                {'name': 'bar', 'members': ['x', 'y', 'z']}
            ]
        },
    }


def test_cray_cfs_session_create_missing_required(cli_runner, rest_mock):
    """ Test cray cfs create ... when a required parameter is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['cfs', 'sessions', 'create', '--clone-url', 'foo'])
    assert result.exit_code == 2
    assert '--name' in result.output

