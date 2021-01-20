""" Test the fas module.

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
from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name
def test_cray_fas_base(cli_runner, rest_mock):
    """ Test `cray init` for creating the default configuration """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas'])
    assert result.exit_code == 0

    outputs = [
        # "cray fas [OPTIONS] COMMAND [ARGS]...",
        "fas",
        "actions",
        "snapshots",
        "operations",
        "service",
        "images"
        ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_cray_fas_describe_actions_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'actions', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "ACTIONID"
        ]
    for out in outputs:
        assert out in result.output

# pylint: disable=redefined-outer-name
def test_cray_fas_describe_images_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'images', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "IMAGEID"
        ]
    for out in outputs:
        assert out in result.output


# pylint: disable=redefined-outer-name
def test_cray_fas_describe_snapshots_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'snapshots', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "NAME"
        ]
    for out in outputs:
        assert out in result.output


def test_cray_fas_describe_operations_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'operations', 'describe'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "OPERATIONID"
        ]
    for out in outputs:
        assert out in result.output


def test_cray_fas_describe_actions_groups_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'actions'])
    assert result.exit_code == 0
    outputs = [
        'Groups:',
        "operations",
        "status",
        "instance"
        ]
    for out in outputs:
        assert out in result.output


def test_cray_fas_describe_actions_status_missing_param(cli_runner, rest_mock):
    """ Test `cray init` for describing an application """
    # pylint: disable=protected-access
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['fas', 'actions', 'status', 'list'])
    assert result.exit_code == 2
    outputs = [
        'Error: Missing argument',
        "ACTIONID"
        ]
    for out in outputs:
        assert out in result.output
