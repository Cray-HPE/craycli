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
""" Test the bos module."""
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json

from cray.tests.utils import compare_dicts

DEFAULT_BOS_VERSION = 'v2'

BOS_V2_GROUPS = ['applystaged', 'components', 'healthz', 'options', 'sessions',
                  'sessiontemplates', 'sessiontemplatesvalid', 'sessiontemplatetemplate',
                  'v2', 'version']

# helper functions

def bos_url(config, ver=DEFAULT_BOS_VERSION, uri=None) -> str:
    """
    Returns the BOS URL for the specified version and uri.
    If no version is specified, uses the default BOS version.
    """
    base_url = f'{config["default"]["hostname"]}/apis/bos/{ver}'
    if uri is None:
        return base_url
    return f'{base_url}{uri}'

# tests: base

def test_cray_bos_base(cli_runner, rest_mock):
    """ Test cray bos base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos'])
    assert result.exit_code == 0

    outputs = ['Boot Orchestration Service', 'Groups:'] + BOS_V2_GROUPS + ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output
    # v1 should no longer be listed
    assert 'v1' not in result.output


def test_cray_bos_list(cli_runner, rest_mock):
    """ Test cray bos list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config)


def test_cray_bos_v2_base(cli_runner, rest_mock):
    """ Test cray bos v2 base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2'])
    assert result.exit_code == 0

    outputs = ['Groups:'] + BOS_V2_GROUPS + ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_list(cli_runner, rest_mock):
    """ Test cray bos v2 list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == bos_url(config, ver="v2")

# tests: applystaged

def test_cray_bos_applystaged_base(cli_runner, rest_mock):
    """ Test cray bos applystaged base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'applystaged'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'create']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_applystaged_base(cli_runner, rest_mock):
    """ Test cray bos v2 applystaged base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'applystaged'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'create']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_applystaged_create(cli_runner, rest_mock):
    """ Test cray bos applystaged create command """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'applystaged', 'create', '--xnames', 'foo,bar'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == bos_url(config, uri='/applystaged')
    compare_dicts(
        { 'xnames': ['foo','bar'] },
        data['body']
    )


def test_cray_bos_v2_applystaged_create(cli_runner, rest_mock):
    """ Test cray bos v2 applystaged create command """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'applystaged', 'create', '--xnames', 'foo,bar'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == bos_url(config, ver="v2", uri='/applystaged')
    compare_dicts(
        { 'xnames': ['foo','bar'] },
        data['body']
    )

# tests: healthz

def test_cray_bos_healthz_base(cli_runner, rest_mock):
    """ Test cray bos healthz base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'healthz'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_healthz_base(cli_runner, rest_mock):
    """ Test cray bos v2 healthz base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'healthz'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output

# tests: options

def test_cray_bos_options_base(cli_runner, rest_mock):
    """ Test cray bos options base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'options'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list', 'update']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_options_base(cli_runner, rest_mock):
    """ Test cray bos v2 options base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'options'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list', 'update']
    for txt in outputs:
        assert txt in result.output

# tests: version

def test_cray_bos_version_base(cli_runner, rest_mock):
    """ Test cray bos version base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'version'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output


def test_cray_bos_v2_version_base(cli_runner, rest_mock):
    """ Test cray bos v2 version base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['bos', 'v2', 'version'])
    assert result.exit_code == 0

    outputs = ['Commands:', 'list']
    for txt in outputs:
        assert txt in result.output

# verify that v1 is gone

def test_bad_path_cray_bos_v1(cli_runner, rest_mock):
    """ Test cray bos v1 """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli,
                           ['bos', 'v1'])
    assert result.exit_code != 0
