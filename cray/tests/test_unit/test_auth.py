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

import click
import json
import os

from cray import auth
from cray.tests.conftest import cli_runner

TOKEN = {}
TOKEN_PATH = os.path.realpath(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)
        ), '../files/token'
    )
)
with open(TOKEN_PATH, encoding='utf-8') as token_file:
    TOKEN = json.load(token_file)


def test_basic_auth_obj(cli_runner: cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    username = opts['default']['username']
    hostname = opts['default']['hostname']

    @cli.command('test')
    @click.pass_context
    def cli_obj(ctx):
        """ Sub cli """
        a = auth.AuthUsername(username, hostname, ctx=ctx)
        assert a
        name = hostname.replace('https://', '')
        assert a.name == '{}.{}'.format(name, username)
        assert a.url == '{}{}'.format(hostname, a.TOKEN_URI.format(a.tenant))

    result = runner.invoke(cli, ['test'])
    print(result.output)
    assert result.exit_code == 0


def test_auth_save(cli_runner: cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    username = opts['default']['username']
    hostname = opts['default']['hostname']
    token = {'test': 123}
    auth_obj = None

    @cli.command('test')
    @click.pass_context
    def cli_obj(ctx):
        """ Sub cli """
        auth_obj = auth.AuthUsername(username, hostname, ctx=ctx)
        auth_obj.save(token)
        with open(auth_obj._token_path, encoding='utf-8') as token_file:
            data = json.load(token_file)
        assert data['test'] == token['test']
        assert data['client_id'] == auth_obj.client_id

    result = runner.invoke(cli, ['test'])
    print(result.output)
    assert result.exit_code == 0


def test_auth_load(cli_runner: cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    username = opts['default']['username']
    hostname = opts['default']['hostname']
    # token = {'test': 123, 'client_id': 'cray'}
    auth_obj = None

    @cli.command('test')
    @click.pass_context
    def cli_obj(ctx):
        """ Sub cli """
        auth_obj = auth.AuthUsername(username, hostname, ctx=ctx)
        with open(auth_obj._token_path, 'w', encoding='utf-8') as token_file:
            json.dump(TOKEN, token_file)
        auth_obj.load()
        assert auth_obj

    result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0


def test_auth_login(cli_runner: cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    username = opts['default']['username']
    password = 'test'
    hostname = opts['default']['hostname']
    auth_obj = None

    @cli.command('test')
    @click.pass_context
    def cli_obj(ctx):
        """ Sub cli """
        auth_obj = auth.AuthUsername(username, hostname, ctx=ctx)
        auth_obj.login(password, username)

    result = runner.invoke(cli, ['test'])
    print(result.output)
    assert result.exit_code == 2
    assert 'Unable to login!' in result.output


def test_auth_login_rsa(cli_runner: cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    username = opts['default']['username']
    password = 'test'
    hostname = opts['default']['hostname']
    auth_obj = None
    rsa_token = 'test'

    @cli.command('test')
    @click.pass_context
    def cli_obj(ctx):
        """ Sub cli """
        auth_obj = auth.AuthUsername(username, hostname, ctx=ctx)
        auth_obj.login(password, username, rsa_token)

    result = runner.invoke(cli, ['test'])
    print(result.output)
    assert result.exit_code == 2
    assert 'Unable to login!' in result.output


def test_auth_existing(cli_runner: cli_runner):
    """ Test `cray init` for creating the default configuration """
    runner, cli, opts = cli_runner
    username = opts['default']['username']
    hostname = opts['default']['hostname']
    auth_obj = None

    @cli.command('test')
    @click.pass_context
    def cli_obj(ctx):
        """ Sub cli """
        auth_obj = auth.AuthUsername(username, hostname, ctx=ctx)
        path = auth_obj._token_path
        with open(path, 'w', encoding='utf-8') as token_file:
            json.dump(TOKEN, token_file)
        auth_obj = auth.AuthFile(path, hostname, ctx=ctx)
        assert auth_obj
        assert auth_obj.name == os.path.basename(path)
        assert auth_obj.path == os.path.dirname(path)

    result = runner.invoke(cli, ['test'])
    print(result.output)
    assert result.exit_code == 0
