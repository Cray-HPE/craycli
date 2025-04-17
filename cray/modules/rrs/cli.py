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
""" rrs """
# pylint: disable=invalid-name
from typing import Callable, Optional, Any
import click
from cray.generator import generate

# Generates a Click CLI from the current file
cli = generate(__file__)

def _file_cb(
    cb: Optional[Callable[[click.Context, click.Parameter, str], Any]]
) -> Callable[[click.Context, click.Parameter, click.File], Any]:
    """
    Creates a callback wrapper for file parameters.
    
    This function wraps an existing callback to handle file objects.
    It reads the file content and passes the string data to the original callback.
    
    Args:
        cb: Optional original callback function that would process string data
        
    Returns:
        A new callback function that accepts a file object
    """
    def _cb(ctx: click.Context, param: click.Parameter, value: click.File) -> Any:
        """
        File parameter callback that reads file content and passes it to the original callback.
        
        Args:
            ctx: Click context
            param: Click parameter
            value: File object opened by Click
            
        Returns:
            Result of the original callback or the file contents if no callback exists
        """
        data = value.read()
        if cb:
            return cb(ctx, param, data)
        return data
    return _cb

# Find the 'from_file' parameter in the 'criticalservices update' command
# and modify it to accept a file path and process the file content
for p in cli.commands['criticalservices'].commands['update'].params:
    if getattr(p, 'payload_name', None) == 'from_file':
        # Change parameter type to accept a file path
        p.type = click.File(mode='r')
        # Set up callback to read the file and pass its contents to the original handler
        p.callback = _file_cb(p.callback)
        break
