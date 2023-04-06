#
# MIT License
#
# (C) Copyright [2020-2022] Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
"""Cray module."""
import os

from cray import cli
from cray import constants
from cray import echo
from cray import errors
from cray import pals
from cray import swagger
from cray import utils
from cray.config import Config
from cray.constants import NAME
from cray.core import argument
from cray.core import command
from cray.core import group
from cray.core import option
from cray.core import pass_context
from cray.generator import generate
from cray.rest import request

__all__ = [
    'Config',
    'NAME',
    'argument',
    'cli',
    'command',
    'constants',
    'echo',
    'errors',
    'generate',
    'generator',
    'group',
    'option',
    'pals',
    'pass_context',
    'request',
    'swagger',
    'utils',
]

# Attempt to fix locale if user sets LC_ALL=C
# See https://click.palletsprojects.com/en/7.x/python3
if os.environ.get('LC_ALL') == 'C':
    os.environ['LC_ALL'] = 'C.UTF-8'
