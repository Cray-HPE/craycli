"""
Tests for Image Management Service (IMS) CLI subcommand (`cray ims`)
and options.
"""
# pylint: disable=redefined-outer-name, unused-import, invalid-name
# pylint: disable=too-many-arguments, import-error, duplicate-code
# pylint: disable=unused-argument
import json
import os

import pytest

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock
from ..utils.utils import new_random_string


def test_cray_ims_base(cli_runner, rest_mock):
    """ Test cray ims base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims'])
    assert result.exit_code == 0

    outputs = [
        "images",
        "jobs",
        "public-keys",
        "recipes",
    ]
    for txt in outputs:
        assert txt in result.output


def test_cray_ims_public_keys_base(cli_runner, rest_mock):
    """ Test cray ims public-keys base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys'])
    assert result.exit_code == 0

    outputs = [
        "create",
        "delete",
        "describe",
        "list",
    ]
    for txt in outputs:
        assert txt in result.output


def test_cray_ims_public_keys_delete(cli_runner, rest_mock):
    """ Test cray ims public_keys delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/public-keys/foo'.format(config['default']['hostname'])


def test_cray_ims_public_keys_list(cli_runner, rest_mock):
    """ Test cray ims public_keys list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/public-keys'.format(config['default']['hostname'])


def test_cray_ims_public_keys_describe(cli_runner, rest_mock):
    """ Test cray ims public_keys describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/public-keys/foo'.format(config['default']['hostname'])


def test_cray_ims_public_keys_create(cli_runner, rest_mock):
    """ Test cray ims public_keys create ... happy path """
    runner, cli, config = cli_runner
    usersshpubkeyfile = os.path.join(os.path.dirname(__file__), '../files/text.txt')
    result = runner.invoke(cli, ['ims', 'public-keys', 'create', '--name', 'foo',
                                 '--public-key', usersshpubkeyfile])
    with open(usersshpubkeyfile) as inf:
        pubkeydata = inf.read()
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ims/public-keys'.format(config['default']['hostname'])
    assert data['body'] == {
        'name': 'foo',
        'public_key': pubkeydata
    }


def test_cray_ims_public_keys_create_missing_required(cli_runner, rest_mock):
    """ Test cray ims public_keys create ... when a required parameter is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys', 'create', '--name', 'foo'])
    assert result.exit_code == 2
    assert '--public-key' in result.output


def test_cray_ims_recipes_base(cli_runner, rest_mock):
    """ Test cray ims recipes base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes'])
    assert result.exit_code == 0

    outputs = [
        "create",
        "delete",
        "describe",
        "list",
    ]
    for txt in outputs:
        assert txt in result.output


def test_cray_ims_recipes_delete(cli_runner, rest_mock):
    """ Test cray ims recipes delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/recipes/foo?cascade=True'.format(config['default']['hostname'])


def test_cray_ims_recipes_delete_cascade_false(cli_runner, rest_mock):
    """ Test cray ims recipes delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes', 'delete', '--cascade', 'False', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/recipes/foo?cascade=False'.format(config['default']['hostname'])


def test_cray_ims_recipes_list(cli_runner, rest_mock):
    """ Test cray ims recipes list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/recipes'.format(config['default']['hostname'])


def test_cray_ims_recipes_describe(cli_runner, rest_mock):
    """ Test cray ims recipes describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/recipes/foo'.format(config['default']['hostname'])


def test_cray_ims_recipes_create(cli_runner, rest_mock):
    """ Test cray ims recipes create ... happy path """
    runner, cli, config = cli_runner
    s3_link_path = new_random_string()
    s3_link_etag = new_random_string()
    result = runner.invoke(cli, ['ims', 'recipes', 'create',
                                 '--name', 'foo',
                                 '--linux-distribution', 'sles15',
                                 '--recipe-type', 'kiwi-ng',
                                 '--link-type', 's3',
                                 '--link-path', s3_link_path,
                                 '--link-etag', s3_link_etag])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ims/recipes'.format(config['default']['hostname'])
    assert 'name' in data['body'] and data['body']['name'] == 'foo'
    assert 'linux_distribution' in data['body'] and data['body']['linux_distribution'] == 'sles15'
    assert 'recipe_type' in data['body'] and data['body']['recipe_type'] == 'kiwi-ng'
    assert 'link' in data['body']
    assert 'type' in data['body']['link'] and data['body']['link']['type'] == 's3'
    assert 'path' in data['body']['link'] and data['body']['link']['path'] == s3_link_path
    assert 'etag' in data['body']['link'] and data['body']['link']['etag'] == s3_link_etag


def test_cray_ims_recipes_create_missing_required(cli_runner, rest_mock):
    """ Test cray ims recipes create ... when a required parameter is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes', 'create',
                                 '--name', 'foo',
                                 '--recipe-type', 'kiwi-ng'])
    assert result.exit_code == 2
    assert '--linux-distribution' in result.output


def test_cray_ims_images_base(cli_runner, rest_mock):
    """ Test cray ims images base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'images'])
    assert result.exit_code == 0

    outputs = [
        "create",
        "delete",
        "describe",
        "list",
    ]
    for txt in outputs:
        assert txt in result.output


def test_cray_ims_images_delete(cli_runner, rest_mock):
    """ Test cray ims images delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'images', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/images/foo?cascade=True'.format(config['default']['hostname'])


def test_cray_ims_images_delete_cascade_false(cli_runner, rest_mock):
    """ Test cray ims images delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'images', 'delete', '--cascade', 'False', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/images/foo?cascade=False'.format(config['default']['hostname'])


def test_cray_ims_images_list(cli_runner, rest_mock):
    """ Test cray ims images list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'images', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/images'.format(config['default']['hostname'])


def test_cray_ims_images_describe(cli_runner, rest_mock):
    """ Test cray ims images describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'images', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/images/foo'.format(config['default']['hostname'])


def test_cray_ims_images_create(cli_runner, rest_mock):
    """ Test cray ims images create ... happy path """
    runner, cli, config = cli_runner
    s3_link_path = new_random_string()
    s3_link_etag = new_random_string()
    result = runner.invoke(cli, ['ims', 'images', 'create',
                                 '--name', 'foo',
                                 '--link-type', 's3',
                                 '--link-path', s3_link_path,
                                 '--link-etag', s3_link_etag])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ims/images'.format(config['default']['hostname'])
    assert 'name' in data['body'] and data['body']['name'] == 'foo'
    assert 'link' in data['body']
    assert 'type' in data['body']['link'] and data['body']['link']['type'] == 's3'
    assert 'path' in data['body']['link'] and data['body']['link']['path'] == s3_link_path
    assert 'etag' in data['body']['link'] and data['body']['link']['etag'] == s3_link_etag


def test_cray_ims_images_create_missing_required(cli_runner, rest_mock):
    """ Test cray ims images create ... happy path """
    runner, cli, config = cli_runner
    s3_link_path = new_random_string()
    s3_link_etag = new_random_string()
    result = runner.invoke(cli, ['ims', 'images', 'create'])
    assert result.exit_code == 2
    assert '--name' in result.output
