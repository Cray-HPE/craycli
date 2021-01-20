""" Test the nmd module.

MIT License

(C) Copyright [2020] Hewlett Packard Enterprise Development LP

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments, unused-argument
import json

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import


# pylint: disable=redefined-outer-name
def test_cray_nmd_help_info(cli_runner, rest_mock):
    """ Test `cray nmd` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['nmd'])
    assert result.exit_code == 0

    outputs = [
        "Node Memory Dump Service",
        "dumps",
        "sdf",
        "status",
        "cli nmd [OPTIONS] COMMAND [ARGS].."
    ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_nmd_dumps(cli_runner, rest_mock):
    """ Test `cray nmd dumps` to make sure the expected dumps commands
    are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['nmd', 'dumps'])
    assert result.exit_code == 0

    outputs = [
        "create",
        "delete",
        "describe",
        "list",
        "cli nmd dumps [OPTIONS] COMMAND [ARGS]..."
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_nmd_dumps_create(cli_runner, rest_mock):
    """ Test `cray nmd dumps create` with valid params """

    runner, cli, config = cli_runner
    xname = 'x0c0s34b0n0'
    sys_restart = 'halt'
    dump_level = 27
    args = [
        'nmd',
        'dumps',
        'create',
        '--xname', xname,
        '--sysrestart', sys_restart,
        '--dumplevel', dump_level
        ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/v2/nmd/dumps'.format(config['default']['hostname'])
    assert data['body'] == {
        'xname': xname,
        'sysrestart': sys_restart,
        'dumplevel': dump_level
    }


# pylint: disable=redefined-outer-name
def test_cray_nmd_dumps_delete(cli_runner, rest_mock):
    """ Test `cray nmd dumps delete` with valid params """

    runner, cli, config = cli_runner
    req_id = 'EA0ACBD5-EA7B-42F8-9E1A-63E0D03A8D72'
    result = runner.invoke(cli, ['nmd', 'dumps', 'delete', req_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    url = '{0}/apis/v2/nmd/dumps/{1}'.format(config['default']['hostname'], req_id)
    assert data['url'] == url


# pylint: disable=redefined-outer-name
def test_cray_nmd_dumps_describe(cli_runner, rest_mock):
    """ Test `cray nmd dumps describe` with valid params """

    runner, cli, config = cli_runner
    req_id = 'EA0ACBD5-EA7B-42F8-9E1A-63E0D03A8D72'
    result = runner.invoke(cli, ['nmd', 'dumps', 'describe', req_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = '{0}/apis/v2/nmd/dumps/{1}'.format(config['default']['hostname'], req_id)
    assert data['url'] == url


# pylint: disable=redefined-outer-name
def test_cray_nmd_dumps_list(cli_runner, rest_mock):
    """ Test `cray nmd dumps list` with valid params """

    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['nmd', 'dumps', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = '{}/apis/v2/nmd/dumps'.format(config['default']['hostname'])
    assert data['url'] == url


# pylint: disable=redefined-outer-name
def test_cray_nmd_sdf_dump(cli_runner, rest_mock):
    """ Test `cray nmd sdf dump` to make sure the expected dumps commands
    are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['nmd', 'sdf', 'dump'])
    assert result.exit_code == 0

    outputs = [
        "discover",
        "targets",
        "cli nmd sdf dump [OPTIONS] COMMAND [ARGS]..."
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_nmd_sdf_dump_discover(cli_runner, rest_mock):
    """ Test `cray nmd sdf dumps discover` to make sure the expected dumps
    commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['nmd', 'sdf', 'dump', 'discover'])
    assert result.exit_code == 0

    outputs = [
        "list",
        "cli nmd sdf dump discover [OPTIONS] COMMAND [ARGS]..."
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_nmd_sdf_dump_discover_list(cli_runner, rest_mock):
    """ Test `cray nmd sdf dump discover list` with valid params """

    runner, cli, config = cli_runner
    session_id = 'EA0ACBD5-EA7B-42F8-9E1A-63E0D03A8D72'
    discovery_version = '1'
    component_ids = 'xname:x0c0s34b0n0,xname:x0c0s34b0n1'
    start_time = '2018-07-28T03:26:01.234567+00:00'
    end_time = '2018-07-29T03:26:01.234567+00:00'
    allow_unsafe = 'false'

    args = [
        'nmd', 'sdf', 'dump', 'discover', 'list',
        '--session-id', session_id,
        '--discovery-version', discovery_version,
        '--component-ids', component_ids,
        '--start-time', start_time,
        '--end-time', end_time,
        '--allow-unsafe', allow_unsafe
        ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = '{}/apis/v2/nmd/sdf/dump/discover'.format(config['default']['hostname'])
    assert data['url'].startswith(url)
    assert 'session_id={}'.format(session_id) in data['url']
    assert 'allow_unsafe=False' in data['url']
    assert 'start_time={}'.format(start_time.split(':')[0]) in data['url']
    assert 'end_time={}'.format(end_time.split(':')[0]) in data['url']
    assert 'component_ids=xname' in data['url']


# pylint: disable=redefined-outer-name
def test_cray_nmd_sdf_dump_targets(cli_runner, rest_mock):
    """ Test `cray nmd sdf dump targets` to make sure the expected dumps
    commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['nmd', 'sdf', 'dump', 'targets'])
    assert result.exit_code == 0

    outputs = [
        "describe",
        "cli nmd sdf dump targets [OPTIONS] COMMAND [ARGS]..."
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_nmd_sdf_dump_targets_describe(cli_runner, rest_mock):
    """ Test `cray nmd sdf dump targets describe` with valid params """

    runner, cli, config = cli_runner
    target_id = 'EA0ACBD5-EA7B-42F8-9E1A-63E0D03A8D72'
    ftype = 'ckdump'

    args = ['nmd', 'sdf', 'dump', 'targets', 'describe', target_id, '--ftype', ftype]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = '{0}/apis/v2/nmd/sdf/dump/targets/{1}?ftype={2}'.format(
        config['default']['hostname'],
        target_id, ftype
    )
    assert data['url'] == url


# pylint: disable=redefined-outer-name
def test_cray_nmd_status(cli_runner, rest_mock):
    """ Test `cray nmd status` to make sure the expected dumps commands
    are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['nmd', 'status'])
    assert result.exit_code == 0

    outputs = [
        "delete",
        "describe",
        "update",
        "cli nmd status [OPTIONS] COMMAND [ARGS]..."
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_nmd_status_delete(cli_runner, rest_mock):
    """ Test `cray nmd status delete` with valid params """

    runner, cli, config = cli_runner
    xname = 'x0c0s34b0n0'
    result = runner.invoke(cli, ['nmd', 'status', 'delete', xname])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    url = '{0}/apis/v2/nmd/status/{1}'.format(config['default']['hostname'], xname)
    assert data['url'] == url


# pylint: disable=redefined-outer-name
def test_cray_nmd_status_describe(cli_runner, rest_mock):
    """ Test `cray nmd status describe` with valid params """

    runner, cli, config = cli_runner
    xname = 'x0c0s34b0n0'
    result = runner.invoke(cli, ['nmd', 'status', 'describe', xname])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = '{0}/apis/v2/nmd/status/{1}'.format(config['default']['hostname'], xname)
    assert data['url'] == url


# pylint: disable=redefined-outer-name
def test_cray_nmd_status_update(cli_runner, rest_mock):
    """ Test `cray nmd status update` with valid params """

    runner, cli, config = cli_runner
    xname = 'x0c0s34b0n0'
    image = 's3://boot-images/c3f4e179-f2d8-4413-98ed-9b79e54f5507/rootfs'
    etag = '262e94e91cef6a451b45eb92d8179fae-177'
    timestamp = '2018-07-28T03:26:01.234567+00:00'
    state = 'dump'
    args = [
        'nmd', 'status', 'update', xname,
        '--image', image,
        '--etag', etag,
        '--timestamp', timestamp,
        '--state', state
        ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    url = '{0}/apis/v2/nmd/status/{1}'.format(config['default']['hostname'], xname)
    assert data['url'].startswith(url)
    assert image == data['body']['image']
    assert etag == data['body']['etag']
    assert state == data['body']['state']
    # timestamp with ':' is hard to match so do it up to ':'
    assert timestamp == data['body']['timestamp']
