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
"""
Tests for Rack Resiliency Service (RRS) CLI subcommand (`cray rrs`) and options.

This module contains unit tests for the RRS CLI commands and verifies that the
appropriate REST API calls are made with correct parameters.
"""

# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json
import os
from typing import List, Any, Dict, Tuple


def compare_output(expected: List[str], cli_output: str) -> None:
    """
    Compare expected output items against actual CLI output.

    This helper function tests if all expected values can be found in the
    CLI output text. It extracts the output lines, skips header information
    before any ":" character, and compares the remaining lines against the
    expected values as unordered sets.

    Args:
        expected: List of strings expected to be in the output
        cli_output: The actual output string from the CLI command

    Raises:
        AssertionError: If the expected values don't match the actual values
    """
    matched = False
    actual = [elem.strip() for elem in cli_output.splitlines()]

    # Skip header lines (everything before the last line containing a colon)
    for i, e in reversed(list(enumerate(actual))):
        if ":" in e:
            matched = True
            del actual[0 : i + 1]
            break

    assert matched, "No header separator found in output"
    assert set(expected) == set(actual), "Output doesn't match expected values"


def test_cray_rrs_base(cli_runner: Tuple[Any, Any, Any], rest_mock: Any) -> None:
    """
    Test the base RRS command without subcommands.

    Verifies that the base 'cray rrs' command executes successfully and
    returns the expected list of available subcommands.

    Args:
        cli_runner: Tuple containing test runner, CLI instance, and config
        rest_mock: Mock object for REST API calls
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ["rrs"])
    assert result.exit_code == 0

    outputs = ["zones", "criticalservices"]

    compare_output(outputs, result.output)


def test_cray_rrs_zones_base(cli_runner: Tuple[Any, Any, Any], rest_mock: Any) -> None:
    """
    Test the RRS zones base command without subcommands.

    Verifies that the 'cray rrs zones' command executes successfully and
    returns the expected list of available subcommands.

    Args:
        cli_runner: Tuple containing test runner, CLI instance, and config
        rest_mock: Mock object for REST API calls
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ["rrs", "zones"])
    assert result.exit_code == 0

    outputs = [
        "describe",
        "list",
    ]

    compare_output(outputs, result.output)


def test_cray_rrs_zones_list(
    cli_runner: Tuple[Any, Any, Dict[str, Dict[str, str]]], rest_mock: Any
) -> None:
    """
    Test the RRS zones list command.

    Verifies that the 'cray rrs zones list' command makes the correct
    GET request to the RRS API endpoint.

    Args:
        cli_runner: Tuple containing test runner, CLI instance, and config
        rest_mock: Mock object for REST API calls
    """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ["rrs", "zones", "list"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "GET"
    assert data["url"] == f'{config["default"]["hostname"]}/apis/rrs/zones'


def test_cray_rrs_zones_describe(
    cli_runner: Tuple[Any, Any, Dict[str, Dict[str, str]]], rest_mock: Any
) -> None:
    """
    Test the RRS zones describe command.

    Verifies that the 'cray rrs zones describe <zone_id>' command makes the correct
    GET request to the RRS API endpoint with the specified zone ID.

    Args:
        cli_runner: Tuple containing test runner, CLI instance, and config
        rest_mock: Mock object for REST API calls
    """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ["rrs", "zones", "describe", "foo"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "GET"
    assert data["url"] == f'{config["default"]["hostname"]}/apis/rrs/zones/foo'


def test_cray_rrs_criticalservices_base(
    cli_runner: Tuple[Any, Any, Any], rest_mock: Any
) -> None:
    """
    Test the RRS critical services base command without subcommands.

    Verifies that the 'cray rrs criticalservices' command executes successfully and
    returns the expected list of available groups and subcommands.

    Args:
        cli_runner: Tuple containing test runner, CLI instance, and config
        rest_mock: Mock object for REST API calls
    """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ["rrs", "criticalservices"])
    assert result.exit_code == 0

    outputs = [
        "Groups:",
        "status",
        "Commands:",
        "describe",
        "list",
        "update",
    ]
    for txt in outputs:
        assert txt in result.output


def test_cray_rrs_criticalservices_list(
    cli_runner: Tuple[Any, Any, Dict[str, Dict[str, str]]], rest_mock: Any
) -> None:
    """
    Test the RRS critical services list command.

    Verifies that the 'cray rrs criticalservices list' command makes the correct
    GET request to the RRS API endpoint.

    Args:
        cli_runner: Tuple containing test runner, CLI instance, and config
        rest_mock: Mock object for REST API calls
    """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ["rrs", "criticalservices", "list"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "GET"
    assert data["url"] == f'{config["default"]["hostname"]}/apis/rrs/criticalservices'


def test_cray_rrs_criticalservices_update(
    cli_runner: Tuple[Any, Any, Dict[str, Dict[str, str]]], rest_mock: Any
) -> None:
    """
    Test the RRS critical services update command.

    Verifies that the 'cray rrs criticalservices update --from-file <file>' command
    makes the correct PATCH request to the RRS API endpoint with the file contents
    in the request body.

    Args:
        cli_runner: Tuple containing test runner, CLI instance, and config
        rest_mock: Mock object for REST API calls
    """
    runner, cli, config = cli_runner
    # Path to the test file containing new services configuration
    newservicesfile = os.path.join(os.path.dirname(__file__), "../files/test.txt")

    result = runner.invoke(
        cli, ["rrs", "criticalservices", "update", "--from-file", newservicesfile]
    )

    # Read the contents of the test file
    with open(newservicesfile, encoding="utf-8") as inf:
        newservicesdata = inf.read()

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["method"] == "PATCH"
    assert data["url"] == f'{config["default"]["hostname"]}/apis/rrs/criticalservices'
    assert data["body"] == {"from_file": newservicesdata}
