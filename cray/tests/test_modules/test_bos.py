#
# MIT License
#
# (C) Copyright 2020-2023 Hewlett Packard Enterprise Development LP
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
""" Test the bos module."""
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json

from cray.tests.utils import compare_dicts

DEFAULT_BOS_VERSION = 'v2'


def test_cray_bos_base(cli_runner, rest_mock):
    """ Test cray bos base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos'])
    assert result.exit_code == 0

    outputs = ['Boot Orchestration Service', 'Groups:', 'v1', 'Commands:',
               'list', ]
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_list(cli_runner, rest_mock):
    """ Test cray bos list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/{DEFAULT_BOS_VERSION}'


def test_cray_bos_v1_base(cli_runner, rest_mock):
    """ Test cray bos v1 base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1'])
    assert result.exit_code == 0

    outputs = ['Groups:', 'session', 'sessiontemplate', 'Commands:', 'list', ]
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v1_list(cli_runner, rest_mock):
    """ Test cray bos v1 list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/bos/v1'


def test_cray_bos_sessiontemplate_base(cli_runner, rest_mock):
    """ Test cray bos sessiontemplate base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'create', 'delete', 'describe', 'list', ]
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_sessiontemplate_delete(cli_runner, rest_mock):
    """ Test cray bos delete sessiontemplate """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v1', 'sessiontemplate', 'delete', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/sessiontemplate/foo'


def test_cray_bos_sessiontemplate_list(cli_runner, rest_mock):
    """ Test cray bos list sessiontemplate """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/sessiontemplate'


def test_cray_bos_sessiontemplate_describe(cli_runner, rest_mock):
    """ Test cray bos describe sessiontemplate """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v1', 'sessiontemplate', 'describe', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/sessiontemplate/foo'


def test_cray_bos_sessiontemplate_create(cli_runner, rest_mock):
    """ Test cray bos create sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v1', 'sessiontemplate', 'create', '--name', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/sessiontemplate'
    compare_dicts(
        {
            'enable_cfs': True, 'name': 'foo',
        }, data['body']
    )


def test_cray_bos_sessiontemplate_create_full(cli_runner, rest_mock):
    """ Test cray bos create sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'v1', 'sessiontemplate', 'create', '--name', 'foo',
         '--partition', 'bar', '--enable-cfs', True, '--cfs-configuration',
         'test-config', '--description', 'desc']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/sessiontemplate'
    expected = {
        'name': 'foo',
        'partition': 'bar',
        'enable_cfs': True,
        'cfs': {'configuration': 'test-config'},
        'description': 'desc'
    }
    compare_dicts(expected, data['body'])


def test_cray_bos_sessiontemplate_create_missing_required(
        cli_runner,
        rest_mock
):
    """Test cray bos create sessiontemplate ... when a required parameter
    is missing

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate', 'create'])
    assert result.exit_code == 2
    assert '--name' in result.output


def test_cray_bos_sessiontemplateteplate_list(cli_runner, rest_mock):
    """ Test cray bos sessiontemplatetemplate list """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'sessiontemplatetemplate', 'list']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/{DEFAULT_BOS_VERSION}' \
                          f'/sessiontemplatetemplate'


def test_cray_bos_v1_sessiontemplateteplate_list(cli_runner, rest_mock):
    """ Test cray bos v1 sessiontemplatetemplate list """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v1', 'sessiontemplatetemplate', 'list']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/sessiontemplatetemplate'


def test_cray_bos_session_base(cli_runner, rest_mock):
    """ Test cray bos session base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session'])
    assert result.exit_code == 0

    outputs = ['Groups:', 'status', 'Commands:', 'create', 'delete',
               'describe', 'list', ]
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_session_delete(cli_runner, rest_mock):
    """ Test cray bos delete session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/session/foo'


def test_cray_bos_session_list(cli_runner, rest_mock):
    """ Test cray bos list session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/session'


def test_cray_bos_session_describe(cli_runner, rest_mock):
    """ Test cray bos describe session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/session/foo'


def test_cray_bos_session_create(cli_runner, rest_mock):
    """ Test cray bos create session ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'v1', 'session', 'create', '--template-uuid', 'foo',
         '--operation', 'boot']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/session'
    compare_dicts(
        {
            'templateUuid': 'foo', 'operation': 'boot',
        }, data['body']
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
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v2/sessions'
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
def test_cray_bos_session_create_missing_required(cli_runner, rest_mock):
    """ Test cray bos create session ... when a required parameter is missing

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'create'])
    assert result.exit_code == 2
    assert '--template-uuid' in result.output or '--operation' in result.output


# Session status

def test_cray_bos_session_status_base(cli_runner, rest_mock):
    """ Test cray bos session base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'delete', 'describe', 'list', ]
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_session_status_list(cli_runner, rest_mock):
    """ Test cray bos session status list"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v1', 'session', 'status', 'list', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/session/foo/status'


def test_cray_bos_session_status_list_missing_required_session(
        cli_runner,
        rest_mock
):
    """Test cray bos session status list... when the required Session ID
       parameter missing

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status', 'list'])
    assert result.exit_code == 2
    assert 'SESSION_ID' in result.output


def test_cray_bos_session_status_describe(cli_runner, rest_mock):
    """ Test cray bos session status describe"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'v1', 'session', 'status', 'describe', 'category-foo',
         'phase-foo', 'boot-set-foo', 'session-id-foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert (data[
                'url'] == f'{config["default"]["hostname"]}'
                          f'/apis/bos/v1/session/session-id-foo'
                          f'/status/boot-set-foo/phase-foo/category-foo')


def test_cray_bos_session_status_describe_missing_required_session(
        cli_runner,
        rest_mock
):
    """Test cray bos session status describe... when the required Session
       ID parameter missing

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v1', 'session', 'status', 'describe', 'boot-set-foo']
    )
    assert result.exit_code == 2
    assert 'SESSION_ID' in result.output


def test_cray_bos_session_status_describe_missing_required_boot_set(
        cli_runner,
        rest_mock
):
    """Test cray bos session status describe... when the required Boot
    Set name parameter missing

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status', 'describe'])
    assert result.exit_code == 2
    assert 'BOOT_SET_NAME' in result.output


def test_cray_bos_session_status_delete(cli_runner, rest_mock):
    """ Test cray bos session status delete"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'v1', 'session', 'status', 'delete', 'boot-set-foo',
         'session-foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == f'{config["default"]["hostname"]}' \
                          f'/apis/bos/v1/session/session-foo' \
                          f'/status/boot-set-foo'


def test_cray_bos_session_status_delete_missing_required_session(
        cli_runner,
        rest_mock
):
    """Test cray bos session status delete missing required Session ID

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v1', 'session', 'status', 'delete', 'foo']
    )
    assert result.exit_code == 2
    assert 'SESSION_ID' in result.output


def test_update_many(cli_runner, rest_mock):
    """ Test cray bos components updatemany"""
    runner, cli, _ = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'v2', 'components', 'updatemany', '--filter-ids',
         'test1,test2', '--patch', '{}']
    )
    assert result.exit_code == 0