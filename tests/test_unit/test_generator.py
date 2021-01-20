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
# pylint: disable=unused-variable, import-error, unused-argument
import json


from ..utils.runner import cli_runner
from ..utils.pets import pets
from ..utils.rest import rest_mock
from ..utils.utils import strip_confirmation


def test_generator_help(cli_runner, pets):
    """ Test `cray init` for creating the default configuration """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pets', 'pet', 'create', '--help'])
    assert result.exit_code == 0
    outputs = [
        "--name TEXT", "doggie  [required]",
        "--photo-urls TEXT,...", "[required]",
        "--configuration CONFIG", "name of configuration to use.",
        "`cray init`", "[env var: CRAY_CONFIG; required]",
        "Usage: cli pets pet create [OPTIONS]"
        ]
    for out in outputs:
        assert out in result.output


def test_generator_read_only(cli_runner, pets):
    """ Test `cray init` for creating the default configuration """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['pets', 'pet', 'create', '--help'])
    print(result.output)
    assert result.exit_code == 0
    assert "--read-only-true" not in result.output
    assert "--read-only-false" in result.output


def test_generator_execute(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    pet_id = '1'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['pets', 'pet', 'describe', pet_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['url'] == '{}/v2/pet/{}'.format(hostname, pet_id)
    assert data['method'].lower() == 'get'
    assert data.get('body') is None


def test_generator_execute_post(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['pets', 'user', 'create', '--username', name])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['url'] == '{}/v2/user'.format(hostname)
    assert data['method'].lower() == 'post'
    assert data['body'].get('username') == 'testuser'


def test_generator_execute_camelcase(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    urls = ['test', '123']
    name = 'foobar'
    result = runner.invoke(cli, ['pets', 'pet', 'create', '--name', name,
                                 '--photo-urls', ','.join(urls)])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['url'] == '{}/v2/pet'.format(hostname)
    assert data['method'].lower() == 'post'
    assert data['body'].get('name') == name
    assert data['body'].get('photoUrls') == urls



def test_generator_danger_tag_default_abort(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    petId = "1"
    result = runner.invoke(cli, ['pets', 'pet', 'delete', petId], input='n')
    print(result.output)
    assert result.exit_code == 1
    outputs = [
        "Are you sure?",
        "Aborted!"]
    for out in outputs:
        assert out in result.output


def test_generator_danger_tag_default_confirm(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    petId = "1"
    result = runner.invoke(cli, ['pets', 'pet', 'delete', petId], input='y')
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(strip_confirmation(result.output))
    assert data['url'] == '{}/v2/pet/{}'.format(hostname, petId)
    assert data['method'].lower() == 'delete'


def test_generator_danger_tag_custom_abort(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    storeId = "1"
    result = runner.invoke(cli, ['pets', 'store', 'order', 'delete', storeId], input='n')
    print(result.output)
    assert result.exit_code == 1
    outputs = [
        "Delete this order?",
        "Aborted!"]
    for out in outputs:
        assert out in result.output


def test_generator_danger_tag_custom_confirm(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    orderId = "1"
    result = runner.invoke(cli, ['pets', 'store', 'order', 'delete', orderId], input='y')
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(strip_confirmation(result.output))
    assert data['url'] == '{}/v2/store/order/{}'.format(hostname, orderId)
    assert data['method'].lower() == 'delete'


def test_generator_danger_tag_force(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    orderId = "1"
    result = runner.invoke(cli, ['pets', 'store', 'order', 'delete', orderId, '-y'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['url'] == '{}/v2/store/order/{}'.format(hostname, orderId)
    assert data['method'].lower() == 'delete'


def test_generator_danger_tag_quiet_ignored(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    orderId = "1"
    result = runner.invoke(cli, ['pets', 'store', 'order', 'delete', orderId, '--quiet'], 'n')
    print(result.output)
    assert result.exit_code == 1
    outputs = [
        "Delete this order?",
        "Aborted!"]
    for out in outputs:
        assert out in result.output

def test_generator_danger_tag_quiet_and_force(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    orderId = "1"
    result = runner.invoke(cli, ['pets', 'store', 'order', 'delete', orderId, '--quiet', '-y'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['url'] == '{}/v2/store/order/{}'.format(hostname, orderId)
    assert data['method'].lower() == 'delete'


def test_generator_hidden_tag_not_exists(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['pets', 'user'])
    print(result.output)
    assert result.exit_code == 0
    assert 'logout' not in result.output
    assert 'login' not in result.output
    outputs = [
        "createWithArray",
        "createWithList",
        "create",
        "delete",
        "describe",
        "update"]
    for out in outputs:
        assert out in result.output


def test_generator_hidden_tag_is_callable(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['pets', 'user', 'logout', 'list'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['url'] == '{}/v2/user/logout'.format(hostname)
    assert data['method'].lower() == 'get'


def test_generator_hidden_tag_only_hides_self(cli_runner, pets, rest_mock):
    """ Test `cray init` for creating the default configuration """
    name = 'testuser'
    runner, cli, opts = cli_runner
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['pets', 'pet'])
    print(result.output)
    assert result.exit_code == 0
    assert 'create' not in result.output
    outputs = [
        "delete",
        "describe",
        "update",
        "findByStatus",
        "findByTags",
        "uploadImage"]
    for out in outputs:
        assert out in result.output
