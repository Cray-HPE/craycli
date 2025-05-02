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

import json
import os

from cray.tests.utils import new_random_string


def compare_output(expected, cli_output):
    """
    Function helper to test if the expected values can
    be found in the output text.
    """
    found = False
    actual = [elem.strip() for elem in cli_output.splitlines()]
    for i, e in reversed(list(enumerate(actual))):
        if ':' in e:
            found = True
            del actual[0:i + 1]
            break
    assert found
    assert set(expected) == set(actual)


def test_cray_console_base(cli_runner, rest_mock):
    """ Test cray ims base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['console'])
    assert result.exit_code == 0

    outputs = [
        "interact",
        "tail"
    ]

    compare_output(outputs, result.output)


def test_cray_ims_console_interact(cli_runner, rest_mock):
    """ Test cray console interact ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['console', 'interact', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/console-operator/console-operator/interact/foo'


def test_cray_ims_console_tail(cli_runner, rest_mock):
    """ Test cray console tail ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['console', 'tail', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/console-operator/console-operator/tail/foo'
