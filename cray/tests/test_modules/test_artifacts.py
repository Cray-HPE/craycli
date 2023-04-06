#
#  MIT License
#
#  (C) Copyright 2020-2023 Hewlett Packard Enterprise Development LP
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.
#
"""
Tests for artifacts CLI subcommand (`cray artifacts/buckets`) and options.
"""


# pylint: disable=unused-argument
# pylint: disable=invalid-name

def test_cray_buckets_help_output(cli_runner):
    """ Test cray buckets help output """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['artifacts'])
    assert result.exit_code == 0

    outputs = [
        "buckets",
        "list",
        "create",
        "describe",
        "get",
        "delete",
    ]
    for out in outputs:
        assert out in result.output


def test_cray_artifacts_help_output(cli_runner):
    """ Test cray artifacts help output """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['artifacts'])
    assert result.exit_code == 0

    outputs = [
        "buckets",
        "list",
        "create",
        "describe",
        "get",
        "delete",
    ]
    for out in outputs:
        assert out in result.output


def test_cray_artifacts_list(cli_runner):
    """ Test cray artifacts list ... """
    runner, cli, _ = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'list'])
    assert result.exit_code == 2


def test_cray_artifacts_create(cli_runner):
    """ Test cray artifacts create  ... """
    runner, cli, _ = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'create', ])
    assert result.exit_code == 2


def test_cray_artifacts_describe(cli_runner):
    """ Test cray artifacts describe  ... """
    runner, cli, _ = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'describe', ])
    assert result.exit_code == 2


def test_cray_artifacts_get(cli_runner):
    """ Test cray artifacts get  ... """
    runner, cli, _ = cli_runner

    # Missing bucket name
    result = runner.invoke(cli, ['artifacts', 'get', ])
    assert result.exit_code == 2
