#
# MIT License
#
# (C) Copyright 2020-2024 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
""" Test the bos module - sessions actions."""
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json

from cray.tests.utils import compare_dicts
from cray.tests.test_modules.test_bos import bos_url


def test_cray_bos_sessions_base(cli_runner, rest_mock):
    """ Test cray bos session base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions'])
    assert result.exit_code == 0

    outputs = ['Groups:', 'status', 'Commands:', 'create', 'delete',
               'describe', 'list']
    for txt in outputs:
        assert txt in result.output
    assert 'update' not in result.output


def test_cray_bos_v2_sessions_base(cli_runner, rest_mock):
    """ Test cray bos v2 session base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions'])
    assert result.exit_code == 0

    outputs = ['Groups:', 'status', 'Commands:', 'create', 'delete',
               'describe', 'list']
    for txt in outputs:
        assert txt in result.output
    assert 'update' not in result.output


def test_cray_bos_sessions_delete(cli_runner, rest_mock):
    """ Test cray bos delete session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == bos_url(config, uri='/sessions/foo')


def test_cray_bos_v2_sessions_delete(cli_runner, rest_mock):
    """ Test cray bos v2 delete session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessions/foo')


def test_cray_bos_sessions_list(cli_runner, rest_mock):
    """ Test cray bos list session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, uri='/sessions')


def test_cray_bos_v2_sessions_list(cli_runner, rest_mock):
    """ Test cray bos v2 list session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessions')


def test_cray_bos_sessions_list_filtered(cli_runner, rest_mock):
    """ Test cray bos list session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli,
                           ['bos', 'sessions', 'list',
                            '--status', 'complete',
                            '--max-age', '1d',
                            '--min-age', '1h'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    expected_url_without_params = bos_url(config, uri='/sessions')
    assert data['url'][:len(expected_url_without_params)+1] == f"{expected_url_without_params}?"
    actual_url_param_string = data['url'].split('?')[-1]
    actual_params = {}
    for kvstring in actual_url_param_string.split('&'):
        k, v = kvstring.split('=')
        actual_params[k] = v

    expected_params = {'min_age': '1h',
                       'max_age': '1d',
                       'status': 'complete'}
    compare_dicts(expected_params, actual_params)


def test_cray_bos_v2_sessions_list_filtered(cli_runner, rest_mock):
    """ Test cray bos v2 list session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli,
                           ['bos', 'v2', 'sessions', 'list',
                            '--status', 'complete',
                            '--max-age', '1d',
                            '--min-age', '1h'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    expected_url_without_params = bos_url(config, ver="v2", uri='/sessions')
    assert data['url'][:len(expected_url_without_params)+1] == f"{expected_url_without_params}?"
    actual_url_param_string = data['url'].split('?')[-1]
    actual_params = {}
    for kvstring in actual_url_param_string.split('&'):
        k, v = kvstring.split('=')
        actual_params[k] = v

    expected_params = {'min_age': '1h',
                       'max_age': '1d',
                       'status': 'complete'}
    compare_dicts(expected_params, actual_params)


def test_bad_path_cray_bos_sessions_list_filtered_invalid(cli_runner, rest_mock):
    """ Test cray bos list session with invalid status filter """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli,
                           ['bos', 'sessions', 'list',
                            '--status', 'foo',
                            '--max-age', '1d',
                            '--min-age', '1h'])
    assert result.exit_code != 0
    assert '--status' in result.output


def test_bad_path_cray_bos_v2_sessions_list_filtered_invalid(cli_runner, rest_mock):
    """ Test cray bos v2 list session with invalid status filter """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli,
                           ['bos', 'v2', 'sessions', 'list',
                            '--status', 'foo',
                            '--max-age', '1d',
                            '--min-age', '1h'])
    assert result.exit_code != 0
    assert '--status' in result.output


def test_cray_bos_sessions_describe(cli_runner, rest_mock):
    """ Test cray bos describe session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, uri='/sessions/foo')


def test_cray_bos_v2_sessions_describe(cli_runner, rest_mock):
    """ Test cray bos v2 describe session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessions/foo')


# pylint: disable=redefined-outer-name
def test_cray_bos_sessions_create(cli_runner, rest_mock):
    """ Test cray bos create session ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'sessions', 'create',
         '--template-name', 'foo',
         '--name', 'bar',
         '--limit', 'harf,blah',
         '--stage', 'true',
         '--include-disabled', 'true',
         '--operation', 'boot']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == bos_url(config, uri='/sessions')
    compare_dicts(
        {
            'template_name': 'foo',
            'name': 'bar',
            'limit': 'harf,blah',
            'stage': True,
            'include_disabled': True,
            'operation': 'boot',
        },
        data['body']
    )


# pylint: disable=redefined-outer-name
def test_cray_bos_v2_sessions_create(cli_runner, rest_mock):
    """ Test cray bos create v2 session ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'v2', 'sessions', 'create',
         '--template-name', 'foo',
         '--name', 'bar',
         '--limit', 'harf,blah',
         '--stage', 'true',
         '--include-disabled', 'true',
         '--operation', 'boot']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessions')
    compare_dicts(
        {
            'template_name': 'foo',
            'name': 'bar',
            'limit': 'harf,blah',
            'stage': True,
            'include_disabled': True,
            'operation': 'boot',
        },
        data['body']
    )


# pylint: disable=redefined-outer-name
def test_bad_path_cray_bos_sessions_create_missing_required(cli_runner, rest_mock):
    """ Test cray bos create session ... when all required parameters are missing
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'create'])
    assert result.exit_code != 0
    assert '--template-name' in result.output or '--operation' in result.output


# pylint: disable=redefined-outer-name
def test_bad_path_cray_bos_v2_sessions_create_missing_required(cli_runner, rest_mock):
    """ Test cray bos v2 create session ... when all required parameters are missing
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'create'])
    assert result.exit_code != 0
    assert '--template-name' in result.output or '--operation' in result.output


# pylint: disable=redefined-outer-name
def test_bad_path_cray_bos_sessions_create_missing_required_template(cli_runner, rest_mock):
    """ Test cray bos create session ... when a required parameter is missing
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'create',
                                 '--operation', 'reboot'])
    assert result.exit_code != 0
    assert '--template-name' in result.output


# pylint: disable=redefined-outer-name
def test_bad_path_cray_bos_v2_sessions_create_missing_required_template(cli_runner, rest_mock):
    """ Test cray bos v2 create session ... when a required parameter is missing
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'create',
                                 '--operation', 'reboot'])
    assert result.exit_code != 0
    assert '--template-name' in result.output


# pylint: disable=redefined-outer-name
def test_bad_path_cray_bos_sessions_create_missing_required_operation(cli_runner, rest_mock):
    """ Test cray bos create session ... when a required parameter is missing
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'create',
                                 '--template-name', 'foo'])
    assert result.exit_code != 0
    assert '--operation' in result.output


# pylint: disable=redefined-outer-name
def test_bad_path_cray_bos_v2_sessions_create_missing_required_operation(cli_runner, rest_mock):
    """ Test cray bos v2 create session ... when a required parameter is missing
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'create',
                                 '--template-name', 'foo'])
    assert result.exit_code != 0
    assert '--operation' in result.output


# pylint: disable=redefined-outer-name
def test_bad_path_cray_bos_sessions_create_invalid_operation(cli_runner, rest_mock):
    """ Test cray bos create session ... when an invalid operation is specified
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'create',
                                 '--template-name', 'foo', '--operation', 'bar'])
    assert result.exit_code != 0
    assert '--operation' in result.output


# pylint: disable=redefined-outer-name
def test_bad_path_cray_bos_v2_sessions_create_invalid_operation(cli_runner, rest_mock):
    """ Test cray bos v2 create session ... when an invalid operation is specified
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'create',
                                 '--template-name', 'foo', '--operation', 'bar'])
    assert result.exit_code != 0
    assert '--operation' in result.output

def test_bad_path_cray_bos_sessions_update(cli_runner, rest_mock):
    """ Test cray bos session update -- should not work """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'update'])
    assert result.exit_code != 0


def test_bad_path_cray_bos_v2_sessions_update(cli_runner, rest_mock):
    """ Test cray bos v2 session update -- should not work """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'update'])
    assert result.exit_code != 0

# tests: sessions: status

def test_cray_bos_sessions_status_base(cli_runner, rest_mock):
    """ Test cray bos session status base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'status'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_sessions_status_base(cli_runner, rest_mock):
    """ Test cray bos v2 session status base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'status'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_sessions_status_list(cli_runner, rest_mock):
    """ Test cray bos session status list"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'sessions', 'status', 'list', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, uri='/sessions/foo/status')


def test_cray_bos_v2_sessions_status_list(cli_runner, rest_mock):
    """ Test cray bos v2 session status list"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v2', 'sessions', 'status', 'list', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessions/foo/status')


def test_bad_path_cray_bos_sessions_status_list_missing_required_session(
        cli_runner,
        rest_mock
):
    """Test cray bos session status list... when the required Session ID
       parameter missing

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessions', 'status', 'list'])
    assert result.exit_code != 0
    assert 'SESSION_ID' in result.output


def test_bad_path_cray_bos_v2_sessions_status_list_missing_required_session(
        cli_runner,
        rest_mock
):
    """Test cray bos v2 session status list... when the required Session ID
       parameter missing

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessions', 'status', 'list'])
    assert result.exit_code != 0
    assert 'SESSION_ID' in result.output
