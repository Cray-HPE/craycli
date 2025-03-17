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
""" Test the bos module -- components actions"""
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json

from cray.tests.utils import compare_dicts, powerset, verify_commands_equal

from cray.tests.test_modules.test_bos import bos_url


# tests

def test_cray_bos_components_base(cli_runner, rest_mock):
    """ Test cray bos components base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'components'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'describe', 'list', 'update', 'updatemany']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_components_base(cli_runner, rest_mock):
    """ Test cray bos v2 components base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'components'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'describe', 'list', 'update', 'updatemany']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_components_update_basic(cli_runner, rest_mock):
    """ Test cray bos v2 components updatemany"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ['bos', 'v2', 'components', 'update', '--retry-policy', '2', 'fakexname']
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == bos_url(config, ver="v2", uri='/components/fakexname')
    compare_dicts(
        {
            'retry_policy': 2
        },
        data['body']
    )


def test_cray_bos_v2_components_update_clear(cli_runner, rest_mock):
    """ Test cray bos v2 components update"""
    runner, cli, config = cli_runner
    common_command_prefix = ['bos', 'v2', 'components', 'update']
    common_command_suffix = ['--enabled', 'False', 'fakexname']
    command_arguments_list = [
        ['--staged-state-session', '',
             '--staged-state-configuration', '',
             '--staged-state-boot-artifacts-initrd', '',
             '--staged-state-boot-artifacts-kernel-parameters', '',
             '--staged-state-boot-artifacts-kernel', '',
             '--desired-state-bss-token', '',
             '--desired-state-configuration', '',
             '--desired-state-boot-artifacts-initrd', '',
             '--desired-state-boot-artifacts-kernel-parameters', '',
             '--desired-state-boot-artifacts-kernel', ''
        ],
        ['--clear-staged-state', '--clear-desired-state'],
        ['--clear-pending-state']
    ]
    result = runner.invoke(
        cli,
        common_command_prefix + command_arguments_list[0] + common_command_suffix
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == bos_url(config, ver="v2", uri='/components/fakexname')
    compare_dicts(
        {
            'enabled': False,
            'staged_state': {
                'session': '',
                'configuration': '',
                'boot_artifacts': {
                    'initrd': '',
                    'kernel_parameters': '',
                    'kernel': ''
                }
            },
            'desired_state': {
                'bss_token': '',
                'configuration': '',
                'boot_artifacts': {
                    'initrd': '',
                    'kernel_parameters': '',
                    'kernel': ''
                }
            }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args + common_command_suffix
                           for command_args in command_arguments_list[1:]])


def test_cray_bos_v2_components_updatemany_by_ids(cli_runner, rest_mock):
    """ Test cray bos v2 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['bos', 'v2', 'components', 'updatemany', '--filter-ids', 'id1,id2']
    command_arguments_list = [
        ['--enabled', 'False'],
        ['--enabled', 'False', '--patch', '{}'],
        ['--patch', '{ "enabled": false }']
    ]
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == bos_url(config, ver="v2", uri='/components')
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


def test_cray_bos_v2_components_updatemany_by_session(cli_runner, rest_mock):
    """ Test cray bos v2 components updatemany"""
    runner, cli, config = cli_runner
    common_command_prefix = ['bos', 'v2', 'components', 'updatemany', '--filter-session', 'test1']
    full_patch_data = {
        'retry_policy': 57,
        'staged_state': {
            'session': '',
            'configuration': '',
            'boot_artifacts': {
                'initrd': '',
                'kernel_parameters': '',
                'kernel': ''
            }
        },
        'desired_state': {
            'bss_token': '',
            'configuration': '',
            'boot_artifacts': {
                'initrd': '',
                'kernel_parameters': '',
                'kernel': ''
            }
        }
    }
    def json_patch(*fields):
        return json.dumps({ k: v for k, v in full_patch_data.items() if k in fields })

    command_arguments_list = []
    all_arguments = ['--retry-policy', '--clear-staged-state', '--clear-desired-state',
                     '--clear-pending-state']
    for explicit_args in powerset(all_arguments):
        args=list(explicit_args)
        patch_fields=[]
        if '--retry-policy' in explicit_args:
            args.insert(args.index('--retry-policy')+1, '57')
        else:
            patch_fields.append('retry_policy')
        if {'--clear-staged-state', '--clear-pending-state'}.isdisjoint(explicit_args):
            patch_fields.append('staged_state')
        if {'--clear-desired-state', '--clear-pending-state'}.isdisjoint(explicit_args):
            patch_fields.append('desired_state')
        command_arguments_list.append(args + ['--patch', json_patch(*patch_fields)])
        if not patch_fields:
            # This means we can equivalently omit the --patch argument
            command_arguments_list.append(args)
    result = runner.invoke(cli, common_command_prefix + command_arguments_list[0])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == bos_url(config, ver="v2", uri='/components')
    compare_dicts(
        {
            'patch': full_patch_data,
            'filters': { 'session': 'test1' }
        },
        data['body']
    )
    # Now make sure that the other versions of the command produce identical results
    verify_commands_equal(runner, cli, data,
                          [common_command_prefix + command_args
                           for command_args in command_arguments_list[1:]])
