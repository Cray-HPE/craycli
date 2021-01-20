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
# pylint: disable=redefined-outer-name, unused-import, invalid-name
# pylint: disable=too-many-arguments, unused-variable, import-error
# pylint: disable=protected-access
import os
import json

import click
import pytest

import cray
from cray import echo

from ..utils.runner import cli_runner


def log(ctx):
    """ Sub cli """
    echo.echo("force", level=echo.LOG_FORCE, ctx=ctx)
    echo.echo("warn", level=echo.LOG_WARN, ctx=ctx)
    echo.echo("info", level=echo.LOG_INFO, ctx=ctx)
    echo.echo("debug", level=echo.LOG_DEBUG, ctx=ctx)
    echo.echo("raw", level=echo.LOG_RAW, ctx=ctx)


def test_logging_default(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner

    f = click.pass_context(log)
    f = cli.command('test')(f)

    result = runner.invoke(cli, ['test'])
    print(result.output)
    assert result.exit_code == 0
    haves = ['force', 'warn']
    have_nots = ['info', 'debug', 'raw']

    for have in haves:
        assert have in result.output

    for have_not in have_nots:
        assert have_not not in result.output


def test_logging_v(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner

    f = click.pass_context(log)
    f = cli.command('test')(f)

    result = runner.invoke(cli, ['test', '-v'])
    print(result.output)
    assert result.exit_code == 0
    haves = ['force', 'warn', 'info']
    have_nots = ['debug', 'raw']

    for have in haves:
        assert have in result.output

    for have_not in have_nots:
        assert have_not not in result.output


def test_logging_vv(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner

    f = click.pass_context(log)
    f = cli.command('test')(f)

    result = runner.invoke(cli, ['test', '-vv'])
    print(result.output)
    assert result.exit_code == 0
    haves = ['force', 'warn', 'info', 'debug']
    have_nots = ['raw']

    for have in haves:
        assert have in result.output

    for have_not in have_nots:
        assert have_not not in result.output


def test_logging_vvv(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner

    f = click.pass_context(log)
    f = cli.command('test')(f)

    result = runner.invoke(cli, ['test', '-vvv'])
    print(result.output)
    assert result.exit_code == 0
    haves = ['force', 'warn', 'info', 'debug', 'raw']

    for have in haves:
        assert have in result.output


def test_logging_vvv_quiet(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner

    f = click.pass_context(log)
    f = cli.command('test')(f)

    result = runner.invoke(cli, ['test', '-vvv', '--quiet'])
    print(result.output)
    assert result.exit_code == 0
    have_nots = ['force', 'warn', 'info', 'debug', 'raw']

    for have_not in have_nots:
        assert have_not not in result.output


def test_logging_quiet(cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, _ = cli_runner

    f = click.pass_context(log)
    f = cli.command('test')(f)

    result = runner.invoke(cli, ['test', '--quiet'])
    print(result.output)
    assert result.exit_code == 0
    have_nots = ['force', 'warn', 'info', 'debug', 'raw']

    for have_not in have_nots:
        assert have_not not in result.output
