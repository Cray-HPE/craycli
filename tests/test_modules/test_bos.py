""" Test the bos module."""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument
import json
import os

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock


def test_cray_bos_base(cli_runner, rest_mock):
    """ Test cray bos base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos'])
    assert result.exit_code == 0

    outputs = [
        'Boot Orchestration Service',
        'Groups:',
        'v1',
        'Commands:',
        'list',
    ]
    for txt in outputs:
        assert txt in result.output

def test_cray_bos_list(cli_runner, rest_mock):
    """ Test cray bos list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/bos/'.format(config['default']['hostname'])

def test_cray_bos_v1_base(cli_runner, rest_mock):
    """ Test cray bos v1 base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1'])
    assert result.exit_code == 0

    outputs = [
        'Groups:',
        'session',
        'sessiontemplate',
        'Commands:',
        'list',
    ]
    for txt in outputs:
        assert txt in result.output

def test_cray_bos_v1_list(cli_runner, rest_mock):
    """ Test cray bos v1 list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/bos/v1'.format(config['default']['hostname'])

def test_cray_bos_sessiontemplate_base(cli_runner, rest_mock):
    """ Test cray bos sessiontemplate base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate'])
    assert result.exit_code == 0

    outputs = [
        'Commands:',
        'create',
        'delete',
        'describe',
        'list',
    ]
    for txt in outputs:
        assert txt in result.output

def test_cray_bos_sessiontemplate_delete(cli_runner, rest_mock):
    """ Test cray bos delete sessiontemplate """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/bos/v1/sessiontemplate/foo'.format(config['default']['hostname'])

def test_cray_bos_sessiontemplate_list(cli_runner, rest_mock):
    """ Test cray bos list sessiontemplate """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/bos/v1/sessiontemplate'.format(config['default']['hostname'])

def test_cray_bos_sessiontemplate_describe(cli_runner, rest_mock):
    """ Test cray bos describe sessiontemplate """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/bos/v1/sessiontemplate/foo'.format(config['default']['hostname'])

def test_cray_bos_sessiontemplate_create(cli_runner, rest_mock):
    """ Test cray bos create sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate', 'create', '--name', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/bos/v1/sessiontemplate'.format(config['default']['hostname'])
    assert data['body'] == {
        'enable_cfs': True,
        'name': 'foo',
    }

def test_cray_bos_sessiontemplate_create_full(cli_runner, rest_mock):
    """ Test cray bos create sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate', 'create',
                                 '--name', 'foo',
                                 '--partition', 'bar',
                                 '--enable-cfs', True,
                                 '--cfs-branch', 'test-branch',
                                 '--cfs-clone-url', 'test-url',
                                 '--description', 'desc',
                                 '--template-body', 'test-body',
                                 '--template-url', 'test-url'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/bos/v1/sessiontemplate'.format(config['default']['hostname'])
    assert data['body'] == {
        'name': 'foo',
        'partition': 'bar',
        'enable_cfs': True,
        'cfs': {'branch': 'test-branch', 'clone_url': 'test-url'},
        'description': 'desc',
        'templateBody': 'test-body',
        'templateUrl': 'test-url',
    }

def test_cray_bos_sessiontemplate_create_missing_required(cli_runner, rest_mock):
    """ Test cray bos create sessiontemplate ... when a required parameter is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'sessiontemplate', 'create'])
    assert result.exit_code == 2
    assert '--name' in result.output

def test_cray_bos_session_base(cli_runner, rest_mock):
    """ Test cray bos session base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session'])
    assert result.exit_code == 0

    outputs = [
        'Groups:',
        'status',
        'Commands:',
        'create',
        'delete',
        'describe',
        'list',
    ]
    for txt in outputs:
        assert txt in result.output

def test_cray_bos_session_delete(cli_runner, rest_mock):
    """ Test cray bos delete session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/bos/v1/session/foo'.format(config['default']['hostname'])

def test_cray_bos_session_list(cli_runner, rest_mock):
    """ Test cray bos list session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/bos/v1/session'.format(config['default']['hostname'])

def test_cray_bos_session_describe(cli_runner, rest_mock):
    """ Test cray bos describe session """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/bos/v1/session/foo'.format(config['default']['hostname'])

def test_cray_bos_session_create(cli_runner, rest_mock):
    """ Test cray bos create session ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'create',
                                 '--template-uuid', 'foo',
                                 '--operation', 'boot'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/bos/v1/session'.format(config['default']['hostname'])
    assert data['body'] == {
        'templateUuid': 'foo',
        'operation': 'boot',
    }

def test_cray_bos_session_create_missing_required(cli_runner, rest_mock):
    """ Test cray bos create session ... when a required parameter is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'create'])
    assert result.exit_code == 2
    assert '--template-uuid' in result.output

# Session status
def test_cray_bos_session_status_base(cli_runner, rest_mock):
    """ Test cray bos session base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status'])
    assert result.exit_code == 0

    outputs = [
        'Commands:',
        'delete',
        'describe',
        'list',
    ]
    for txt in outputs:
        assert txt in result.output

def test_cray_bos_session_status_list(cli_runner, rest_mock):
    """ Test cray bos session status list"""
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status', 'list', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/bos/v1/session/foo/status'.format(config['default']['hostname'])

def test_cray_bos_session_status_list_missing_required_session(cli_runner, rest_mock):
    """ Test cray bos session status list... when the required Session ID parameter missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status', 'list'])
    assert result.exit_code == 2
    assert 'SESSION_ID' in result.output

def test_cray_bos_session_status_describe(cli_runner, rest_mock):
    """ Test cray bos session status describe"""
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status', 'describe', 'boot-set-foo', 'session-id-foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/bos/v1/session/session-id-foo/status/boot-set-foo'.format(config['default']['hostname'])

def test_cray_bos_session_status_describe_missing_required_session(cli_runner, rest_mock):
    """ Test cray bos session status describe... when the required Session ID parameter missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status', 'describe', 'boot-set-foo'])
    assert result.exit_code == 2
    assert 'SESSION_ID' in result.output

def test_cray_bos_session_status_describe_missing_required_boot_set(cli_runner, rest_mock):
    """ Test cray bos session status describe... when the required Boot Set name parameter missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status', 'describe'])
    assert result.exit_code == 2
    assert 'BOOT_SET_NAME' in result.output

def test_cray_bos_session_status_delete(cli_runner, rest_mock):
    """ Test cray bos session status delete"""
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/bos/v1/session/foo/status'.format(config['default']['hostname'])

def test_cray_bos_session_status_delete_missing_required_session(cli_runner, rest_mock):
    """ Test cray bos session status delete missing required Session ID"""
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v1', 'session', 'status', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/bos/v1/session/foo/status'.format(config['default']['hostname'])