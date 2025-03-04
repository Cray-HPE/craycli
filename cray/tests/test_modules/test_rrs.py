#
#  MIT License
#
#  (C) Copyright [2025] Hewlett Packard Enterprise Development LP
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
""" Tests for Rack Resiliency Service (RRS) CLI subcommand (`cray rrs`)
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


def test_cray_rrs_base(cli_runner, rest_mock):
    """ Test cray rrs base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['rrs'])
    assert result.exit_code == 0

    outputs = [
        "zones",
        "criticalservices"
    ]

    compare_output(outputs, result.output)


def test_cray_rrs_zones_base(cli_runner, rest_mock):
    """ Test cray rrs zones base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['rrs', 'zones'])
    assert result.exit_code == 0

    outputs = [
        "describe",
        "list",
    ]

    compare_output(outputs, result.output)


def test_cray_rrs_zones_list(cli_runner, rest_mock):
    """ Test cray rrs zones list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['rrs', 'zones', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/rrs/zones'


def test_cray_rrs_zones_describe(cli_runner, rest_mock):
    """ Test cray rrs zones describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['rrs', 'zones', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/rrs/zones/foo'


def test_cray_rrs_criticalservices_base(cli_runner, rest_mock):
    """ Test cray rrs criticalservices base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['rrs', 'criticalservices'])
    assert result.exit_code == 0

    outputs = [
        "describe",
        "list",
        "update",
    ]

    compare_output(outputs, result.output)


def test_cray_rrs_criticalservices_list(cli_runner, rest_mock):
    """ Test cray rrs criticalservices list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['rrs', 'criticalservices', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/rrs/criticalservices'


def test_cray_rrs_criticalservices_describe(cli_runner, rest_mock):
    """ Test cray rrs criticalservices describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['rrs', 'criticalservices', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/rrs/criticalservices/foo'


def test_cray_rrs_criticalservices_update(cli_runner, rest_mock):
    """ Test cray rrs criticalservices update ... happy path """
    runner, cli, config = cli_runner
    newservicesfile = os.path.join(
        os.path.dirname(__file__),
        '../files/test.txt'
    )
    result = runner.invoke(
        cli,
        ['rrs', 'criticalservices', 'update',
         '--new-services', newservicesfile]
    )
    with open(newservicesfile, encoding='utf-8') as inf:
        newservicesdata = inf.read()
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == f'{config["default"]["hostname"]}/apis/rrs/criticalservices'
    assert data['body'] == {
        'new_services': newservicesdata
    }