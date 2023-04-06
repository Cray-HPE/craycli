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
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import os


def test_cray_uas_base(cli_runner, rest_mock):
    """ Test `cray uas` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['uas'])
    assert result.exit_code == 0

    outputs = [
        "User Access Service",
        "create",
        "delete",
        "list",
        "images",
        "mgr-info",
        "uais",
        "cli uas [OPTIONS] COMMAND [ARGS].."
    ]
    for out in outputs:
        assert out in result.output


def test_cray_uas_images(cli_runner, rest_mock):
    """ Test `cray uas images` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['uas', 'images'])
    assert result.exit_code == 0

    outputs = [
        "cli uas images [OPTIONS] COMMAND [ARGS]..",
        "list"
    ]
    for out in outputs:
        assert out in result.output


def test_cray_uas_mgr_info(cli_runner, rest_mock):
    """ Test `cray uas mgr-info` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['uas', 'mgr-info'])
    assert result.exit_code == 0

    outputs = [
        "cli uas mgr-info [OPTIONS] COMMAND [ARGS]..",
        "list"
    ]
    for out in outputs:
        assert out in result.output


def test_cray_uas_uais(cli_runner, rest_mock):
    """ Test `cray uas uais` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['uas', 'uais'])
    assert result.exit_code == 0

    outputs = [
        "cli uas uais [OPTIONS] COMMAND [ARGS]..",
        "list",
        "delete"
    ]
    for out in outputs:
        assert out in result.output


def test_cray_uas_create_missing_publickey_param(cli_runner, rest_mock):
    """ Test `cray uas create` to ensure an error is thrown """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['uas', 'create', 'foo', 'bar'])
    print(result.output)
    assert result.exit_code == 2
    outputs = [
        "Usage: cli uas create [OPTIONS]",
        "Error: Missing option '--publickey'."
    ]
    for out in outputs:
        assert out in result.output


# def test_cray_uas_create(cli_runner, rest_mock):
#     """ Test `cray uas create` with valid params """
#
#     runner, cli, opts = cli_runner
#     url_template = '/apis/uas-mgr/v1/uas?imagename={image}'
#     publickey = os.path.join(os.path.dirname(__file__),
#                              '../files/test_public_key')
#     image = 'bar'
#     config = opts['default']
#     hostname = config['hostname']
#     result = runner.invoke(cli, ['uas', 'create', '--imagename', image,
#                                  '--publickey', publickey])
#     print(result.output)
#     assert result.exit_code == 0
#     data = json.loads(result.output)
#     assert data['method'].lower() == 'post'
#     assert data.get('body')
#     body = data.get('body')
#     assert 'test_public_key' in body
#     assert 'form-data' in body
#     assert 'name="publickey"' in body
#     # assert body.get('usersshpubkey') == {'file': usersshpubkeyfile}
#     uri = data['url'].split(hostname)[-1]
#     assert uri == url_template.format(image=image)


def test_cray_uas_create_with_private_key(cli_runner, rest_mock):
    """ Test `cray uas create` to ensure an error is thrown

    Specifying a file containing a private key should fail with a
    informative error message.
    """

    runner, cli, _ = cli_runner
    privatekey = os.path.join(
        os.path.dirname(__file__),
        '../files/test_private_key'
    )
    result = runner.invoke(cli, ['uas', 'create', '--publickey', privatekey])
    print(result.output)
    assert result.exit_code == 2
    outputs = [
        "Usage: cli uas create [OPTIONS]",
        "Error: Please specify a properly formatted public key.",
        "It appears that you are trying to use your private key.",
    ]
    for out in outputs:
        assert out in result.output
