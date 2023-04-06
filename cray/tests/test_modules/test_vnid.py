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
""" Test the vnid module. """
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json


def test_vnid_help_info(cli_runner, rest_mock):
    """Test `cray vnid` to make sure the expected commands are available"""
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ["vnid"])
    assert result.exit_code == 0

    outputs = [
        "cli vnid [OPTIONS] COMMAND [ARGS]...",
        "Virtual Network Identifier Daemon",
        "jobs",
        "vnis",
        "create",
        "delete",
        "describe",
        "list",
    ]
    for out in outputs:
        assert out in result.output


def test_vnid_create(cli_runner, rest_mock):
    """Test `cray vnid create` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        [
            "vnid",
            "create",
            "--enforce=1",
            "--vni-svc-limit=1",
            "--vni-limit=2",
            "--description=wlm",
            "--partition-name=wlm",
        ],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "POST"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis"
    assert data["body"] == {
        "enforce": True,
        "vniSvcLimit": 1,
        "vniLimit": 2,
        "description": "wlm",
        "partitionName": "wlm",
    }


def test_vnid_delete(cli_runner, rest_mock):
    """Test `cray vnid delete` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        [
            "vnid",
            "delete",
            "wlm",
        ],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "DELETE"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm"


def test_vnid_describe(cli_runner, rest_mock):
    """Test `cray vnid describe` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        [
            "vnid",
            "describe",
            "wlm",
        ],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "GET"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm"


def test_vnid_list(cli_runner, rest_mock):
    """Test `cray vnid list` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ["vnid", "list"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "GET"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis"


def test_vnid_jobs_create(cli_runner, rest_mock):
    """Test `cray vnid jobs create` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        [
            "vnid",
            "jobs",
            "create",
            "wlm",
            "--uid=1",
            "--job-id=1.pbs-server",
        ],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "POST"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm/jobs"
    assert data["body"] == {"UID": 1, "JobID": "1.pbs-server"}


def test_vnid_jobs_delete(cli_runner, rest_mock):
    """Test `cray vnid jobs delete` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ["vnid", "jobs", "delete", "1.pbs-server", "wlm"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "DELETE"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm/jobs/1.pbs-server"


def test_vnid_jobs_describe(cli_runner, rest_mock):
    """Test `cray vnid jobs describe` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ["vnid", "jobs", "describe", "1.pbs-server", "wlm"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "GET"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm/jobs/1.pbs-server"


def test_vnid_jobs_list(cli_runner, rest_mock):
    """Test `cray vnid jobs delete` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ["vnid", "jobs", "list", "wlm"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "GET"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm/jobs"


def test_vnid_vnis_create(cli_runner, rest_mock):
    """Test `cray vnid vnis create` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ["vnid", "vnis", "create", "wlm", "--vni-count=1", "--is-service=0"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "POST"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm/vnis"
    assert data["body"] == {"vniCount": 1, "isService": False}


def test_vnid_vnis_delete(cli_runner, rest_mock):
    """Test `cray vnid vnis delete` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ["vnid", "vnis", "delete", "1024", "wlm"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "DELETE"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm/vnis/1024"


def test_vnid_vnis_describe(cli_runner, rest_mock):
    """Test `cray vnid vnis describe` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ["vnid", "vnis", "describe", "1024", "wlm"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "GET"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm/vnis/1024"


def test_vnid_vnis_list(cli_runner, rest_mock):
    """Test `cray vnid vnis delete` with valid params"""
    runner, cli, config = cli_runner
    result = runner.invoke(
        cli,
        ["vnid", "vnis", "list", "wlm"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "GET"
    assert data[
               "url"] == f"{config['default']['hostname']}" \
                         f"/apis/vnid/fabric/vnis/wlm/vnis"
