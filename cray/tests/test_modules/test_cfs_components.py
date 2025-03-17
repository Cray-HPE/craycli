#
# MIT License
#
# (C) Copyright 2025 Hewlett Packard Enterprise Development LP
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
""" Test the cfs module -- components actions"""
# pylint: disable=unused-argument
# pylint: disable=invalid-name
# pylint: disable=line-too-long
import json
from cray.tests.utils import compare_dicts, verify_commands_equal

DEFAULT_CFS_VERSION = 'v3'
# helper functions

def cfs_url(config, ver=DEFAULT_CFS_VERSION, uri=None) -> str:
    """
    Returns the CFS URL for the specified version and uri.
    If no version is specified, uses the default CFS version.
    """
    base_url = f'{config["default"]["hostname"]}/apis/cfs/{ver}'
    if uri is None:
        return base_url
    return f'{base_url}{uri}'

def test_cray_cfs_components_base(cli_runner, rest_mock):
    """ Test cray cfs components base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['cfs', 'v3', 'components'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'describe', 'list', 'update', 'updatemany']
    for txt in outputs:
        assert txt in result.output

def test_cray_cfs_v2_components_base(cli_runner, rest_mock):
    """ Test cray cfs v2 components base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['cfs', 'v2', 'components'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'describe', 'list', 'update', 'updatemany']
    for txt in outputs:
        assert txt in result.output

def test_cray_cfs_v2_components_update_basic(cli_runner, rest_mock):
    """ Test cray cfs v2 components update"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['cfs', 'v2', 'components', 'update', '--retry-policy', '2', 'fakexname']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, ver="v2", uri='/components/fakexname')
    compare_dicts(
        {
            'retryPolicy': 2
        },
        data['body']
    )

def test_cray_cfs_v3_components_update_basic(cli_runner, rest_mock):
    """ Test cray cfs v3 components update"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['cfs', 'v3', 'components', 'update', '--retry-policy', '2', 'fakexname']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, uri='/components/fakexname')
    compare_dicts(
        {
            'retry_policy': 2
        },
        data['body']
    )

def test_cray_cfs_v3_components_updatemany_by_ids_filter(cli_runner, rest_mock):
    """ Test cray cfs v3 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v3', 'components', 'updatemany', '--filter-ids', 'id1,id2']
    command_arguments_list = [
        ['--enabled', 'False'],
        ['--enabled', 'False', '--patch', '{}'],
        ['--patch', '{ "enabled": false }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, uri='/components')
    compare_dicts(
        {
            'patch': { 'enabled': False },
            'filters': { 'ids': 'id1,id2' }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])

def test_cray_cfs_v3_components_updatemany_by_status_filter(cli_runner, rest_mock):
    """ Test cray cfs v3 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v3', 'components', 'updatemany', '--filter-status', 'fakestatus']
    command_arguments_list = [
        ['--error-count', 1],
        ['--error-count', 1, '--patch', '{}'],
        ['--patch', '{ "error_count": 1 }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, uri='/components')
    compare_dicts(
        {
            'patch': { 'error_count': 1 },
            'filters': { 'status': 'fakestatus' }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])

def test_cray_cfs_v3_components_updatemany_by_enabled_filter(cli_runner, rest_mock):
    """ Test cray cfs v3 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v3', 'components', 'updatemany', '--filter-enabled', 't']
    command_arguments_list = [
        ['--retry-policy', 1],
        ['--retry-policy', 1, '--patch', '{}'],
        ['--patch', '{ "retry_policy": 1 }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, uri='/components')
    compare_dicts(
        {
            'patch': { 'retry_policy': 1 },
            'filters': { 'enabled': True }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])

def test_cray_cfs_v3_components_updatemany_by_tags_filter(cli_runner, rest_mock):
    """ Test cray cfs v3 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v3', 'components', 'updatemany', '--filter-tags', 'fakecomponent=fakecomponentid']
    command_arguments_list = [
        ['--desired-config', 'fakeconfig'],
        ['--desired-config', 'fakeconfig', '--patch', '{}'],
        ['--patch', '{ "desired_config": "fakeconfig" }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, uri='/components')
    compare_dicts(
        {
            'patch': { 'desired_config': "fakeconfig" },
            'filters': { 'tags': 'fakecomponent=fakecomponentid' }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])

def test_cray_cfs_v3_components_updatemany_by_config_name_filter(cli_runner, rest_mock):
    """ Test cray cfs v3 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v3', 'components', 'updatemany', '--filter-config-name', 'fakeconfiguration']
    command_arguments_list = [
        ['--enabled', 'False'],
        ['--enabled', 'False', '--patch', '{}'],
        ['--patch', '{ "enabled": false }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, uri='/components')
    compare_dicts(
        {
            'patch': { 'enabled': False },
            'filters': { 'config_name': 'fakeconfiguration' }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])

def test_cray_cfs_v2_components_updatemany_by_ids_filter(cli_runner, rest_mock):
    """ Test cray cfs v2 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v2', 'components', 'updatemany', '--filter-ids', 'id1,id2']
    command_arguments_list = [
        ['--enabled', 'False'],
        ['--enabled', 'False', '--patch', '{}'],
        ['--patch', '{ "enabled": false }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, ver="v2", uri='/components')
    compare_dicts(
        {
            'patch': { 'enabled': False },
            'filters': { 'ids': 'id1,id2' }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])

def test_cray_cfs_v2_components_updatemany_by_status_filter(cli_runner, rest_mock):
    """ Test cray cfs v2 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v2', 'components', 'updatemany', '--filter-status', 'fakestatus']
    command_arguments_list = [
        ['--error-count', 1],
        ['--error-count', 1, '--patch', '{}'],
        ['--patch', '{ "errorCount": 1 }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, ver="v2", uri='/components')
    compare_dicts(
        {
            'patch': { 'errorCount': 1 },
            'filters': { 'status': 'fakestatus' }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])

def test_cray_cfs_v2_components_updatemany_by_enabled_filter(cli_runner, rest_mock):
    """ Test cray cfs v2 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v2', 'components', 'updatemany', '--filter-enabled', 't']
    command_arguments_list = [
        ['--retry-policy', 1],
        ['--retry-policy', 1 , '--patch', '{}'],
        ['--patch', '{ "retryPolicy": 1 }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, ver="v2", uri='/components')
    compare_dicts(
        {
            'patch': { 'retryPolicy': 1 },
            'filters': { 'enabled': True }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])

def test_cray_cfs_v2_components_updatemany_by_tags_filter(cli_runner, rest_mock):
    """ Test cray cfs v2 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v2', 'components', 'updatemany', '--filter-tags', 'fakecomponent=fakecomponentid']
    command_arguments_list = [
        ['--desired-config', 'fakeconfig'],
        ['--desired-config', 'fakeconfig', '--patch', '{}'],
        ['--patch', '{ "desiredConfig": "fakeconfig" }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, ver="v2", uri='/components')
    compare_dicts(
        {
            'patch': { 'desiredConfig': 'fakeconfig' },
            'filters': { 'tags': 'fakecomponent=fakecomponentid' }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])

def test_cray_cfs_v2_components_updatemany_by_config_name_filter(cli_runner, rest_mock):
    """ Test cray cfs v2 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['cfs', 'v2', 'components', 'updatemany', '--filter-config-name', 'fakeconfiguration']
    command_arguments_list = [
        ['--enabled', 'False'],
        ['--enabled', 'False', '--patch', '{}'],
        ['--patch', '{ "enabled": false }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == cfs_url(config, ver="v2", uri='/components')
    compare_dicts(
        {
            'patch': { 'enabled': False },
            'filters': { 'config_name': 'fakeconfiguration' }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])
