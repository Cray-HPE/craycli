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
"""rrs"""
# pylint: disable=invalid-name
import json
from typing import Callable, Any, Dict

from cray.constants import FROM_FILE_TAG
from cray.core import option
from cray.generator import _opt_callback
from cray.generator import generate

SWAGGER_OPTS = {}

# Generates a Click CLI from the current file
cli = generate(__file__, swagger_opts=SWAGGER_OPTS))


def create_templates_critical_services(func: Callable) -> Callable:
    """
    Creates a callback wrapper that handles file-based critical services configuration.

    This function wraps the original command callback to intercept the --from-file parameter,
    read JSON data from the specified file, and pass it as a payload to the API call.

    Args:
        func: The original command callback function to be wrapped

    Returns:
        A decorated function that handles file input for critical services configuration
    """

    def _decorator(from_file: Dict[str, Any], **kwargs: Dict[str, Any]) -> Any:
        """
        Decorator function that processes the --from-file parameter.

        If no file is specified, it calls the original function unchanged.
        If a file is specified, it reads the JSON content and passes it as payload.

        Args:
            from_file: Dictionary containing the file path value from --from-file option
            **kwargs: Additional keyword arguments passed to the original function

        Returns:
            Result of the original function call
        """
        # If no file specified, proceed with normal operation
        if not from_file.get("value"):
            return func(**kwargs)

        # Read and parse JSON data from the specified file
        with open(from_file["value"], "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        payload = data
        # Hack to tell the CLI we are passing our own payload; don't generate
        kwargs[FROM_FILE_TAG] = {"value": payload, "name": FROM_FILE_TAG}
        return func(**kwargs)

    return _decorator


def setup_critical_services_from_file(command: Any) -> None:
    """
    Adds a --from-file parameter to a command for JSON file input.

    This function modifies an existing CLI command by:
    1. Adding a --from-file option that accepts a file path
    2. Reordering parameters to place the new option first
    3. Filtering out deprecated parameters
    4. Wrapping the original callback with file handling logic

    Args:
        command: The CLI command object to be modified
    """
    # Add the --from-file option to the command
    option(
        "--from-file",
        callback=_opt_callback,
        type=str,
        default="",
        metavar="TEXT",
        help="A file containing the JSON for critical services configuration",
    )(command)

    # Reorder parameters: put the new --from-file parameter first,
    # followed by non-deprecated existing parameters
    params = [command.params[-1]]  # The newly added --from-file parameter
    for param in command.params[:-1]:
        # Only include parameters that are not marked as deprecated
        if not getattr(param, "help", None) or "DEPRECATED" not in param.help:
            params.append(param)
    command.params = params

    # Wrap the original callback with file handling functionality
    command.callback = create_templates_critical_services(command.callback)


# Apply the file-based configuration setup to the criticalservices update command
# This enables users to use: cray rrs criticalservices update --from-file <json_file>
setup_critical_services_from_file(cli.commands["criticalservices"].commands["update"])
