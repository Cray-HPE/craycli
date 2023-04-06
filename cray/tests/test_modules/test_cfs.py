#
#  MIT License
#
#  (C) Copyright 2020-2023 Hewlett Packard Enterprise Development LP
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.
#
""" Tests for Configuration Framework Service (CFS) CLI subcommand (`cray cfs`)
and options. """
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json


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
    assert data['url'] == f'{config["default"]["hostname"]}/apis/cfs/v2/sessions/foo'


def test_cray_cfs_session_list(cli_runner, rest_mock):
    """ Test cray cfs list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['cfs', 'sessions', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/cfs/v2/sessions'


def test_cray_cfs_session_describe(cli_runner, rest_mock):
    """ Test cray cfs describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['cfs', 'sessions', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/cfs/v2/sessions/foo'


def test_cray_cfs_session_create(cli_runner, rest_mock):
    """ Test cray cfs create ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['cfs', 'sessions', 'create', '--name', 'foo',
              '--configuration-name', 'bar']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/cfs/v2/sessions'
    assert data['body'] == {
        'name': 'foo',
        'configurationName': 'bar',
        'target': {'definition': 'dynamic', 'groups': [], 'image_map': []},
    }


def test_cray_cfs_session_create_full(cli_runner, rest_mock):
    """ Test cray cfs create ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['cfs', 'sessions', 'create', '--name', 'foo',
              '--configuration-name', 'bar',
              '--configuration-limit', 'baz',
              '--ansible-limit', 'Compute',
              '--ansible-config', 'default-config',
              '--ansible-verbosity', '1',
              '--target-definition', 'spec',
              '--target-group', 'foo', 'a, b, c',
              '--target-group', 'bar', 'x,y,z',
              '--target-image-map', 'foo', 'new']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/cfs/v2/sessions'
    assert data['body'] == {
        'name': 'foo',
        'configurationName': 'bar',
        'configurationLimit': 'baz',
        'ansibleLimit': 'Compute',
        'ansibleConfig': 'default-config',
        'ansibleVerbosity': 1,
        'target': {
            'definition': 'spec',
            'groups': [
                {'name': 'foo', 'members': ['a', 'b', 'c']},
                {'name': 'bar', 'members': ['x', 'y', 'z']}
            ],
            'image_map': [{'source_id': 'foo', 'result_name': 'new'}]
        },
    }


def test_cray_cfs_session_create_missing_required(cli_runner, rest_mock):
    """ Test cray cfs create ... when a required parameter is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(
        cli,
        ['cfs', 'sessions', 'create', '--configuration-name', 'foo']
    )
    assert result.exit_code == 2
    assert '--name' in result.output
