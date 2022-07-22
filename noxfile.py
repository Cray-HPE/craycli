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

""" Nox definitions for tests, docs, and linting
"""
from __future__ import absolute_import
import os

import nox  # pylint: disable=import-error


COVERAGE_FAIL = 85
ERROR_ON_GENERATE = True
MODULE_PATH_TEMPLATE = 'cray/modules/{}'

# The version available in python 3.4 doesn't support this.
# So we have to hack around it for the jenkins pipelines.
if vars(nox).get('options'):
    nox.options.keywords = 'not generate'
    external = {"external": True}
else:
    ERROR_ON_GENERATE = False
    external = {}


def convert_file(session, path, filename):
    session.run('/bin/bash', 'utils/convert.sh', path, filename, **external)


@nox.session(python='3')
def generate(session):
    """Generate a new CLI module"""

    BASE_CLI_FILE = """\"\"\"{}\"\"\"
# pylint: disable=invalid-name
from cray.generator import generate


cli = generate(__file__)
"""

    if len(session.posargs) != 2:
        msg = 'Usage: nox -s generate -- [module name] [stash link to swagger]'
        global ERROR_ON_GENERATE
        if ERROR_ON_GENERATE:
            raise Exception(msg)
        else:
            print(msg)
            print("Ignore this is a full.")
            return

    from string import Template

    module_name = session.posargs[0]
    swagger_file = session.posargs[1]


    test_template = 'tests/files/template.txt'
    module_path = MODULE_PATH_TEMPLATE.format(module_name)
    test_file = 'tests/test_modules/test_{}.py'.format(module_name)
    init_file = '{}/__init__.py'.format(module_path)
    cli_file = '{}/cli.py'.format(module_path)

    is_local_file = os.path.exists(swagger_file)


    if not os.path.exists(module_path):
        os.makedirs(module_path)
    if not os.path.isfile(init_file):
        with open(init_file, 'a'):
            os.utime(init_file, None)
    if not os.path.isfile(cli_file):
        with open(cli_file, 'w') as f:
            f.write(BASE_CLI_FILE.format(module_name))
    if not os.path.isfile(test_file):
        with open (test_template) as test_template:
            data = {'name': module_name}
            tmp = Template(test_template.read()).substitute(data)
        with open(test_file, 'w') as f:
            f.write(tmp)

    if is_local_file:
        from shutil import copy2
        copy2(swagger_file, module_path)
        convert_file_name = os.path.basename(swagger_file)
    else:
        raise Exception("Please use a local file. .remote files with urls are deprecated.")
    convert_file(session, module_path, convert_file_name)


@nox.session(python=None)
def swagger(session):
    """Run each swagger file through the converter in case anything changed.
    This should be run before running unit tests"""

    walk_path = 'cray/modules'
    if session.posargs:
        module = session.posargs[0]
        module_path = MODULE_PATH_TEMPLATE.format(module)
        if os.path.exists(module_path):
            walk_path = module_path
        else:
            raise Exception("Module {} not found.".format(module))
    else:
        # If here we are doing all files so do test files too.
        convert_file(session, './tests/files/', 'swagger.json')

    for path, _, files in os.walk(walk_path):
        swaggers = [f for f in files if f.startswith('swagger.')]
        remotes = [f for f in files if f == '.remote']
        swagger_file = None
        remote_file = None
        for f in files:
            if f.startswith('swagger.'):
                swagger_file = f
                break
            if f == '.remote':
                remote_file = f
                continue
        if swagger_file:
            convert_file(session, path, swagger_file)
            continue

        if remote_file:
            convert_file(session, path, remote_file)
            continue


@nox.session(python='3')
def lint_modules(session):
    """Validate .remote files and confirm other integration settings"""
    for path, _, files in os.walk('./cray/modules'):
        remotes = [f for f in files if f == '.remote']
        swaggers = [f for f in files if f.startswith('swagger.')]
        if remotes:
            with open('{}/{}'.format(path, remotes[0])) as remote:
                data = remote.read().rstrip()
            if os.path.exists('{}/{}'.format(path, data)):
                # remote used for local file
                continue
            else:
                import warnings
                warnings.warn(("URLs in .remote files are being deprecated. " 
                               "Please use a local file"), DeprecationWarning)
            continue
        if remotes and swaggers:
            raise Exception("Both a .remote and swagger file are provided. Please choose one.")


@nox.session(python='3')
def tests(session):
    """Default unit test session.
    This is meant to be run against any python version intended to be used.
    """
    # Install all test dependencies, then install this package in-place.
    path = 'tests'
    session.install('-r', 'requirements-test.txt')
    session.install('-e', '.')

    if session.posargs:
        path = session.posargs[0]


    # Run py.test against the tests.
    session.run(
        'py.test',
        '--quiet',
        '--cov=cray',
        '--cov=tests',
        '--cov-append',
        '--cov-config=.coveragerc',
        '--cov-report=',
        '--cov-fail-under={}'.format(COVERAGE_FAIL),
        path,
        *session.posargs
    )


@nox.session(python='3')
def lint(session):
    """Run linters.
    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    run_cmd_code = ['pylint', 'cray']
    if 'prod' not in session.posargs:
        run_cmd_code.append('--disable=import-error')
        run_cmd_code.append('--enable=fixme')

    run_cmd_tests = ['pylint', 'tests']
    if 'prod' not in session.posargs:
        run_cmd_tests.append('--disable=import-error')
        run_cmd_tests.append('--disable=fixme')

    session.install('-r', 'requirements-lint.txt')
    session.install('.')
    session.run(*run_cmd_code)
    session.run(*run_cmd_tests)


@nox.session(python='3')
def docs(session):
    """Run sphinx.
    """
    session.install('-r', 'requirements-docs.txt')
    session.install('.')
    session.chdir('docs')
    session.run('make', 'clean', **external)
    session.run('make', 'html', **external)


@nox.session(python='3')
def cover(session):
    """Run the final coverage report.
    This outputs the coverage report aggregating coverage from the unit
    test runs, and then erases coverage data.
    """
    session.install('coverage', 'pytest-cov')
    session.run('coverage', 'report', '--show-missing',
                '--fail-under={}'.format(COVERAGE_FAIL))
    session.run('coverage', 'erase')
