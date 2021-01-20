""" Test the main CLI command (`cray`) and options.

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
import uuid

from six.moves import urllib

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import


# pylint: disable=redefined-outer-name
def test_cray_pals_base(cli_runner, rest_mock):
    """ Test cray pals with no arguments """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pals'])
    assert result.exit_code == 0

    outputs = [
        "Parallel Application Launch Service",
        "apps",
        "cli pals [OPTIONS] COMMAND [ARGS].."
    ]
    for out in outputs:
        assert out in result.output

    result = runner.invoke(cli, ['pals', 'apps'])
    assert result.exit_code == 0

    outputs = ["files", "signal", "tools"]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_create(cli_runner, rest_mock):
    """ Test cray pals apps create """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pals', 'apps', 'create'])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "PAYLOAD_FILE"
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_list(cli_runner, rest_mock):
    """ Test cray pals apps list """
    # Test with no filters
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pals', 'apps', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps'

    # Test with filters
    result = runner.invoke(
        cli, ['pals', 'apps', 'list', '--nodes', 'nid000001', '--usernames', 'root'])
    assert result.exit_code == 0
    print(result)
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps'
    query_args = url.query.split('&')
    assert len(query_args) == 2
    assert 'usernames=root' in query_args
    assert 'nodes=nid000001' in query_args


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_describe(cli_runner, rest_mock):
    """ Test cray pals apps describe """
    # Test with missing apid argument
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pals', 'apps', 'describe'])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "APID"
        ]
    for out in outputs:
        assert out in result.output

    # Test with apid argument
    apid = str(uuid.uuid4())
    result = runner.invoke(cli, ['pals', 'apps', 'describe', apid])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s' % apid


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_delete(cli_runner, rest_mock):
    """ Test cancelling an application """
    # Test with missing apid argument
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pals', 'apps', 'delete'])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "APID"
        ]
    for out in outputs:
        assert out in result.output

    # Test with apid argument
    apid = str(uuid.uuid4())
    result = runner.invoke(cli, ['pals', 'apps', 'delete', apid])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s' % apid


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_files_create(cli_runner, rest_mock):
    """ Test transferring a file """
    runner, cli, _ = cli_runner
    apid = str(uuid.uuid4())

    result = runner.invoke(
        cli, ['pals', 'apps', 'files', 'create', apid])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing option",
        "--file"
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_files_delete(cli_runner, rest_mock):
    """ Test deleting a file """
    runner, cli, _ = cli_runner
    apid = str(uuid.uuid4())
    fname = 'a.out'

    result = runner.invoke(
        cli, ['pals', 'apps', 'files', 'delete', fname, apid])
    assert result.exit_code == 0

    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s/files/%s' % (apid, fname)


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_files_describe(cli_runner, rest_mock):
    """ Test describing a file """
    runner, cli, _ = cli_runner
    apid = str(uuid.uuid4())
    fname = 'a.out'

    result = runner.invoke(
        cli, ['pals', 'apps', 'files', 'describe', fname, apid])
    assert result.exit_code == 0

    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s/files/%s' % (apid, fname)


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_files_list(cli_runner, rest_mock):
    """ Test listing files for an application """
    runner, cli, _ = cli_runner
    apid = str(uuid.uuid4())

    result = runner.invoke(cli, ['pals', 'apps', 'files', 'list', apid])
    assert result.exit_code == 0

    data = json.loads(result.output)
    assert data['method'] == 'GET'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s/files' % apid


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_signal(cli_runner, rest_mock):
    """ Test signaling an application """
    runner, cli, _ = cli_runner

    result = runner.invoke(cli, ['pals', 'apps', 'signal', 'create'])
    assert result.exit_code == 2
    assert 'Usage: cli pals apps signal create [OPTIONS] APID' in result.output

    apid = str(uuid.uuid4())
    result = runner.invoke(
        cli, ['pals', 'apps', 'signal', 'create', '--signum=15', apid])
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'POST'
    assert data['body']['signum'] == 15
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s/signal' % apid


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_tools_create(cli_runner, rest_mock):
    """ Test cray pals apps tools create """
    runner, cli, _ = cli_runner
    apid = str(uuid.uuid4())
    argv = ['/bin/hostname', '-f']

    result = runner.invoke(cli, ['pals', 'apps', 'tools', 'create'])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "APID"
        ]
    for out in outputs:
        assert out in result.output

    result = runner.invoke(cli, ['pals', 'apps', 'tools', 'create', apid])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing option",
        "--argv"
        ]
    for out in outputs:
        assert out in result.output

    result = runner.invoke(
        cli, ['pals', 'apps', 'tools', 'create', '--argv', ','.join(argv), apid])
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'POST'
    assert data['body']['argv'] == argv
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s/tools' % apid


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_tools_delete(cli_runner, rest_mock):
    """ Test cray pals apps tools delete """
    runner, cli, _ = cli_runner
    apid = str(uuid.uuid4())
    toolid = str(uuid.uuid4())

    result = runner.invoke(cli, ['pals', 'apps', 'tools', 'delete'])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "TOOLID"
        ]
    for out in outputs:
        assert out in result.output

    result = runner.invoke(cli, ['pals', 'apps', 'tools', 'delete', toolid])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "APID"
        ]
    for out in outputs:
        assert out in result.output

    result = runner.invoke(
        cli, ['pals', 'apps', 'tools', 'delete', toolid, apid])
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'DELETE'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s/tools/%s' % (apid, toolid)


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_tools_describe(cli_runner, rest_mock):
    """ Test cray pals apps tools describe """
    runner, cli, _ = cli_runner
    apid = str(uuid.uuid4())
    toolid = str(uuid.uuid4())

    result = runner.invoke(cli, ['pals', 'apps', 'tools', 'describe'])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "TOOLID"
        ]
    for out in outputs:
        assert out in result.output

    result = runner.invoke(cli, ['pals', 'apps', 'tools', 'describe', toolid])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "APID"
        ]
    for out in outputs:
        assert out in result.output

    result = runner.invoke(
        cli, ['pals', 'apps', 'tools', 'describe', toolid, apid])
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'GET'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s/tools/%s' % (apid, toolid)


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_tools_list(cli_runner, rest_mock):
    """ Test cray pals apps tools list """
    runner, cli, _ = cli_runner
    apid = str(uuid.uuid4())

    result = runner.invoke(cli, ['pals', 'apps', 'tools', 'list'])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "APID"
        ]
    for out in outputs:
        assert out in result.output

    result = runner.invoke(cli, ['pals', 'apps', 'tools', 'list', apid])
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'GET'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s/tools' % apid


# pylint: disable=redefined-outer-name
def test_cray_pals_apps_procinfo_list(cli_runner, rest_mock):
    """ Test cray pals apps procinfo list """
    runner, cli, _ = cli_runner
    apid = str(uuid.uuid4())

    result = runner.invoke(cli, ['pals', 'apps', 'procinfo', 'list'])
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument",
        "APID"
        ]
    for out in outputs:
        assert out in result.output

    result = runner.invoke(cli, ['pals', 'apps', 'procinfo', 'list', apid])
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data['method'] == 'GET'
    url = urllib.parse.urlparse(data['url'])
    assert url.path == '/apis/pals/v1/apps/%s/procinfo' % apid
