"""
Tests for Artifact Repository Service (ARS) CLI subcommand (`cray ars`)
and options.
"""
# pylint: disable=redefined-outer-name, unused-import, invalid-name
# pylint: disable=too-many-arguments, import-error, duplicate-code
# pylint: disable=unused-argument
import json
import os
import re
import tempfile

import pytest

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock


def test_cray_ars_base(cli_runner, rest_mock):
    """ Test cray ars base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ars'])
    assert result.exit_code == 0

    outputs = [
        "Artifact Repository Service API",
        "Options:",
        "--help  Show this message and exit.",
        "Groups:",
        "artifacts",
        "uploads"
    ]

    for txt in outputs:
        assert txt in result.output

# TEST Artifacts Command
def test_cray_ars_artifacts(cli_runner, rest_mock):
    """ Test cray ars artifacts command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ars', 'artifacts'])
    assert result.exit_code == 0

    outputs = [
        "ars artifacts [OPTIONS] COMMAND [ARGS]...",
        "create",
        "delete",
        "describe",
        "list"
    ]

    for txt in outputs:
        assert txt in result.output


def test_cray_ars_artifacts_create(cli_runner, rest_mock):
    """ Test cray ars create ... """
    runner, cli, config = cli_runner
    version = "0.1"
    atype = 'generic'
    name = 'test-name'
    result = runner.invoke(cli, ['ars', 'artifacts', 'create', '--version', version, '--atype',
                                 atype, '--name', name])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ars/artifacts'.format(config['default']['hostname'])
    assert data['body'] == {
        'version': version,
        'atype': atype,
        'name': name
    }


def test_cray_ars_artifacts_delete(cli_runner, rest_mock):
    """ Test cray ars artifacts delete ... """
    runner, cli, config = cli_runner
    name = 'test-artifact'
    result = runner.invoke(cli, ['ars', 'artifacts', 'delete', name])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ars/artifacts/{}'.format(config['default']['hostname'], name)


def test_cray_ars_artifacts_list(cli_runner, rest_mock):
    """ Test cray ars artifacts list ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ars', 'artifacts', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ars/artifacts'.format(config['default']['hostname'])


def test_cray_ars_artifacts_describe(cli_runner, rest_mock):
    """ Test cray ars artifacts describe ... """
    runner, cli, config = cli_runner
    artifact_id = 'foo'
    result = runner.invoke(cli, ['ars', 'artifacts', 'describe', artifact_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ars/artifacts/{}'.format(config['default']['hostname'],
                                                            artifact_id)


def test_cray_ars_artifacts_create_missing_required_name(cli_runner, rest_mock):
    """ Test cray ars artifacts  create ... when a required parameter 'name' is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ars', 'artifacts', 'create',
                                 '--version', '0.1',
                                 '--atype', 'generic'])
    assert result.exit_code == 2
    assert '--name' in result.output


def test_cray_ars_artifacts_create_missing_required_atype(cli_runner, rest_mock):
    """ Test cray ars artifacts  create ... when a required parameter 'atype' is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ars', 'artifacts', 'create',
                                 '--version', '0.1',
                                 '--name', 'foo'])
    assert result.exit_code == 2
    assert '--atype' in result.output


def test_cray_ars_artifacts_create_missing_required_version(cli_runner, rest_mock):
    """ Test cray ars artifacts  create ... when a required parameter 'version' is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ars', 'artifacts', 'create',
                                 '--atype', 'generic',
                                 '--name', 'foo'])
    assert result.exit_code == 2
    assert '--version' in result.output

def test_cray_ars_artifacts_create_invalid_atype(cli_runner, rest_mock):
    """ Test cray ars artifacts create ... with an invalid atype value """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ars', 'artifacts', 'create',
                                 '--version', '0.1',
                                 '--name', 'foo',
                                 '--atype', 'invalid-type'])
    assert result.exit_code == 2
    assert 'Invalid value for' in result.output
    assert "--atype" in result.output


# TEST Uploads Command
def test_cray_ars_uploads(cli_runner, rest_mock):
    """ Test cray ars artifacts uploads command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ars', 'uploads'])
    assert result.exit_code == 0

    outputs = [
        "ars uploads [OPTIONS] COMMAND [ARGS]...",
        "create",
        "delete",
        "describe",
        "list",
        "update"
    ]

    for txt in outputs:
        assert txt in result.output


def test_cray_ars_uploads_create(cli_runner, rest_mock):
    """ Test cray ars uploads create ... """
    runner, cli, config = cli_runner
    artifact_id = 'foo'
    result = runner.invoke(cli, ['ars', 'uploads', 'create', '--artifact-id', artifact_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ars/uploads'.format(config['default']['hostname'])
    assert data['body'] == {
        'artifact_id': artifact_id
    }


def test_cray_ars_uploads_delete(cli_runner, rest_mock):
    """ Test cray ars uploads delete ... """
    # TODO should I use a uuid for the upload_id?
    runner, cli, config = cli_runner
    upload_id = 'test-upload-id'
    result = runner.invoke(cli, ['ars', 'uploads', 'delete', upload_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ars/uploads/{}'.format(config['default']['hostname'], upload_id)


def test_cray_ars_uploads_list(cli_runner, rest_mock):
    """ Test cray ars uploads list ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ars', 'uploads', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ars/uploads'.format(config['default']['hostname'])


def test_cray_ars_uploads_describe(cli_runner, rest_mock):
    """ Test cray ars uploads describe ... """
    runner, cli, config = cli_runner
    upload_id = 'foo'
    result = runner.invoke(cli, ['ars', 'uploads', 'describe', upload_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ars/uploads/{}'.format(config['default']['hostname'],
                                                          upload_id)


# def test_cray_ars_uploads_update(cli_runner, rest_mock):
#     """ Test cray ars uploads describe ... """
#     runner, cli, config = cli_runner
#     upload_id = 'foo'
#     with tempfile.NamedTemporaryFile() as fp:
#         file_name = fp.name
#         result = runner.invoke(cli, ['ars', 'uploads', 'update', '--artifact', file_name,
#                                      upload_id])
#     assert result.exit_code == 0
#     data = json.loads(result.output)
#     assert data['method'] == 'PUT'
#     assert data['url'] == '{}/apis/ars/uploads/{}'.format(config['default']['hostname'],
#                                                           upload_id)
#     # The body comes back as a unicode string version of the multipart/form-data
#     # format.  It does not come back as a nice dictionary.
#     # Thus, the following does not work.
#     #assert data['body'] == {
#     #    'artifact': os.path.basename(file_name)
#     #}
#     # Instead, I parsed the data using regular expressions.
#     name_regex = re.compile(r'name=\"(.*)\";')
#     filename_regex = re.compile(r'filename=\"(.*)\"')
#     returned_name = name_regex.search(data['body']).group(1)
#     returned_file_name = filename_regex.search(data['body']).group(1)
#     assert returned_name == 'artifact'
#     assert returned_file_name == os.path.basename(file_name)

def test_cray_ars_uploads_update_missing_required_artifact_path(cli_runner, rest_mock):
    """ Test cray ars uploads describe ... """
    runner, cli, _ = cli_runner
    upload_id = 'foo'
    result = runner.invoke(cli, ['ars', 'uploads', 'update', upload_id])
    assert result.exit_code == 2
    assert '--artifact' in result.output


def test_cray_ars_uploads_create_missing_required_artifact_id(cli_runner, rest_mock):
    """ Test cray ars uploads create ... when a required parameter 'name' is missing """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ars', 'uploads', 'create'])
    assert result.exit_code == 2
    assert '--artifact-id' in result.output
