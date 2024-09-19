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
""" Test the bos module - sessiontemplates actions."""
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json

from cray.tests.utils import compare_dicts
from cray.tests.test_modules.test_bos import bos_url

def test_cray_bos_sessiontemplates_base(cli_runner, rest_mock):
    """ Test cray bos sessiontemplates base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessiontemplates'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'create', 'delete', 'describe', 'list', 'update']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_sessiontemplates_base(cli_runner, rest_mock):
    """ Test cray bos v2 sessiontemplates base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessiontemplates'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'create', 'delete', 'describe', 'list', 'update']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_sessiontemplates_delete(cli_runner, rest_mock):
    """ Test cray bos delete sessiontemplates """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'sessiontemplates', 'delete', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == bos_url(config, uri='/sessiontemplates/foo')


def test_cray_bos_v2_sessiontemplates_delete(cli_runner, rest_mock):
    """ Test cray bos v2 delete sessiontemplates """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v2', 'sessiontemplates', 'delete', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessiontemplates/foo')


def test_cray_bos_sessiontemplates_list(cli_runner, rest_mock):
    """ Test cray bos list sessiontemplates """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'sessiontemplates', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, uri='/sessiontemplates')


def test_cray_bos_v2_sessiontemplates_list(cli_runner, rest_mock):
    """ Test cray bos v2 list sessiontemplates """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessiontemplates', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessiontemplates')


def test_cray_bos_sessiontemplates_describe(cli_runner, rest_mock):
    """ Test cray bos describe sessiontemplate """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'sessiontemplates', 'describe', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, uri='/sessiontemplates/foo')


def test_cray_bos_v2_sessiontemplates_describe(cli_runner, rest_mock):
    """ Test cray bos v2 describe sessiontemplate """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v2', 'sessiontemplates', 'describe', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessiontemplates/foo')


def test_cray_bos_sessiontemplates_create(cli_runner, rest_mock):
    """ Test cray bos create sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'sessiontemplates', 'create', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == bos_url(config, uri='/sessiontemplates/foo')
    compare_dicts(
        {
            'enable_cfs': True
        }, data['body']
    )


def test_cray_bos_v2_sessiontemplates_create(cli_runner, rest_mock):
    """ Test cray bos v2 create sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v2', 'sessiontemplates', 'create', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessiontemplates/foo')
    compare_dicts(
        {
            'enable_cfs': True
        }, data['body']
    )


def test_cray_bos_sessiontemplates_create_full(cli_runner, rest_mock):
    """ Test cray bos create sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'sessiontemplates', 'create',
         '--enable-cfs', False, '--cfs-configuration',
         'test-config', '--description', 'desc', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == bos_url(config, uri='/sessiontemplates/foo')
    expected = {
        'enable_cfs': False,
        'cfs': {'configuration': 'test-config'},
        'description': 'desc'
    }
    compare_dicts(expected, data['body'])


def test_cray_bos_v2_sessiontemplates_create_full(cli_runner, rest_mock):
    """ Test cray bos v2 create sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'v2', 'sessiontemplates', 'create',
         '--enable-cfs', False, '--cfs-configuration',
         'test-config', '--description', 'desc', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessiontemplates/foo')
    expected = {
        'enable_cfs': False,
        'cfs': {'configuration': 'test-config'},
        'description': 'desc'
    }
    compare_dicts(expected, data['body'])


def test_cray_bos_sessiontemplates_update(cli_runner, rest_mock):
    """ Test cray bos update sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'sessiontemplates', 'update',
         '--enable-cfs', False, '--cfs-configuration',
         'test-config', '--description', 'desc', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == bos_url(config, uri='/sessiontemplates/foo')
    expected = {
        'enable_cfs': False,
        'cfs': {'configuration': 'test-config'},
        'description': 'desc'
    }
    compare_dicts(expected, data['body'])


def test_cray_bos_v2_sessiontemplates_update(cli_runner, rest_mock):
    """ Test cray bos v2 update sessiontemplate ... happy path """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'v2', 'sessiontemplates', 'update',
         '--enable-cfs', False, '--cfs-configuration',
         'test-config', '--description', 'desc', 'foo']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessiontemplates/foo')
    expected = {
        'enable_cfs': False,
        'cfs': {'configuration': 'test-config'},
        'description': 'desc'
    }
    compare_dicts(expected, data['body'])


def test_bad_path_cray_bos_sessiontemplates_create_missing_required(
        cli_runner,
        rest_mock
):
    """Test cray bos create sessiontemplate ... when a required parameter
    is missing
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessiontemplates', 'create'])
    assert result.exit_code != 0
    assert 'SESSION_TEMPLATE_ID' in result.output


def test_bad_path_cray_bos_v2_sessiontemplates_create_missing_required(
        cli_runner,
        rest_mock
):
    """Test cray bos v2 create sessiontemplate ... when a required parameter
    is missing
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessiontemplates', 'create'])
    assert result.exit_code != 0
    assert 'SESSION_TEMPLATE_ID' in result.output

# tests: sessiontemplatesvalid

def test_cray_bos_sessiontemplatesvalid_base(cli_runner, rest_mock):
    """ Test cray bos sessiontemplatesvalid base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessiontemplatesvalid'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'describe']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_sessiontemplatesvalid_base(cli_runner, rest_mock):
    """ Test cray bos v2 sessiontemplatesvalid base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessiontemplatesvalid'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'describe']
    for txt in outputs:
        assert txt in result.output

# tests: sessiontemplatetemplate

def test_cray_bos_sessiontemplatetemplate_base(cli_runner, rest_mock):
    """ Test cray bos sessiontemplatetemplate base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'sessiontemplatetemplate'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_sessiontemplatetemplate_base(cli_runner, rest_mock):
    """ Test cray bos v2 sessiontemplatetemplate base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'sessiontemplatetemplate'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_sessiontemplatetemplate_list(cli_runner, rest_mock):
    """ Test cray bos sessiontemplatetemplate list """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'sessiontemplatetemplate', 'list']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, uri='/sessiontemplatetemplate')


def test_cray_bos_v2_sessiontemplatetemplate_list(cli_runner, rest_mock):
    """ Test cray bos v2 sessiontemplatetemplate list """
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli, ['bos', 'v2', 'sessiontemplatetemplate', 'list']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, ver="v2", uri='/sessiontemplatetemplate')
