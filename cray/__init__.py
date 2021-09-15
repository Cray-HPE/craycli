"""
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
# pylint: skip-file

import os

from . import cli, echo
from .core import option, group , argument, command, pass_context
from .config import Config
from . import utils, swagger, constants, errors, exceptions, pals
from .constants import NAME
from .rest import request
from .generator import generate


__all__ = ['option', 'group', 'argument', 'command', 'Config', 'utils', 'NAME',
           'pass_context', 'echo', 'swagger', 'generator', 'request',
           'cli', 'constants', 'generate', 'errors', 'exceptions', 'logging',
           'pals']

# Attempt to fix locale if user sets LC_ALL=C
# See https://click.palletsprojects.com/en/7.x/python3
if os.environ.get('LC_ALL') == 'C':
    os.environ['LC_ALL'] = 'C.UTF-8'
