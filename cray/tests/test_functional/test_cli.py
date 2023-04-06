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
""" Test the main CLI command (`cray`) and options. """

from cray.tests.conftest import cli_runner
from cray.tests.conftest import pets


def test_cray_help(cli_runner: cli_runner):
    """ Test `cray init` for creating the default configuration """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    outputs = [
        "Options:", "Groups:", "Commands:", "init", "auth", "config"
    ]
    for txt in outputs:
        assert txt in result.output


def test_cray_upper_hidden(cli_runner: cli_runner, pets: pets):
    """ Test `cray init` for creating the default configuration """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pets', '--help'])
    print(result.output)
    assert result.exit_code == 0
    outputs = [
        "upperCase"
    ]
    for txt in outputs:
        assert txt in result.output
    not_outputs = [
        "UpperCase"
    ]
    for txt in not_outputs:
        assert txt not in result.output


def test_cray_nested_upper_hidden(cli_runner: cli_runner, pets: pets):
    """ Test `cray init` for creating the default configuration """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pets', 'upperCase', '--help'])
    print(result.output)
    assert result.exit_code == 0
    outputs = [
        "test"
    ]
    for txt in outputs:
        assert txt in result.output
    not_outputs = [
        "Test",
        "(DEPRECATED)"
    ]
    for txt in not_outputs:
        assert txt not in result.output


def test_cray_deprecated_upper(cli_runner: cli_runner, pets: pets):
    """ Test `cray init` for creating the default configuration """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pets', 'UpperCase', '--help'])
    print(result.output)
    assert result.exit_code == 0
    outputs = [
        "(DEPRECATED)"
    ]
    for txt in outputs:
        assert txt in result.output
