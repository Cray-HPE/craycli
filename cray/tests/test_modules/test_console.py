#
#  MIT License
#
#  (C) Copyright 2025 Hewlett Packard Enterprise Development LP
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
""" Tests for Console Services CLI subcommand (`cray console`)
and options. """
# pylint: disable=unused-argument
# pylint: disable=invalid-name
# pylint: disable=line-too-long
import json

def test_cray_console_base(cli_runner):
    """ Test cray console base command """
    runner, cli, _ = cli_runner
    assert type(runner).__name__ == ""
    result = runner.invoke(cli, ['console'])
    assert result.exit_code == 0

    outputs = [
        "interact",
        "tail"
    ]
    for txt in outputs:
        assert txt in result.output

def test_cray_console_interact_no_args(cli_runner):
    """ Test cray console interact ... """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['console', 'interact'])

    assert result.exit_code == 2


def test_cray_console_interact(cli_runner):
    """ Test cray console interact ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['console', 'interact', 'foo'])
    assert result.exit_code == 0
    assert result.output is not None
    assert result.output == "Nothing"
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/console-operator/console-operator/interact/foo'


def test_cray_console_tail(cli_runner):
    """ Test cray console tail ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['console', 'tail', 'foo'])
    assert result.exit_code == 1
    assert result.output is not None
    assert result.output == "Nothing"
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/console-operator/console-operator/tail/foo'
