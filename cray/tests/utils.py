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
""" Test utilities that make testing easier. """
# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name
import os
import uuid
import json
from urllib.parse import urlparse
from itertools import chain, combinations
import names
import toml


def _uuid():
    return str(uuid.uuid4())


def new_username():
    return names.get_full_name().replace(' ', '')


def new_hostname():
    return f"https://{_uuid().replace('-', '')}"


def new_tenant():
    return f"vcluster-{_uuid().replace('-', '')}"


def new_configname():
    return _uuid().replace('-', '')


def new_random_string():
    return _uuid().replace('-', '')


def create_config_file(filename, hostname, tenant, username):
    data = {
        'core': {'hostname': hostname, 'tenant': tenant},
        'auth': {'login': {'username': username}}
    }
    path = '.config/cray/configurations'
    full_path = os.path.join(path, filename)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(full_path, 'w', encoding='utf-8') as file:
        toml.dump(data, file)


def strip_confirmation(output):
    return "\n".join(output.splitlines()[1:])


def compare_dicts(expected, actual):
    """ Compare dictionaries because ordering can be non-deterministic """
    assert expected.keys() == actual.keys()
    for key in expected:
        if isinstance(expected[key], dict) and isinstance(actual[key], dict):
            # Handle nested dicts because they can be non-deterministic too.
            compare_dicts(expected[key], actual[key])
        else:
            assert actual[key] == expected[key]


def compare_urls(expected, actual):
    """ Compare two URLs because the query portions may be differently ordered"""
    parsed_exp = urlparse(expected)
    parsed_act = urlparse(actual)
    assert parsed_exp.scheme == parsed_act.scheme
    assert parsed_exp.path == parsed_act.path
    if parsed_exp.query:
        query_exp = parsed_exp.query.split('&')
        query_act = parsed_act.query.split('&')
        for term in query_exp:
            assert term in query_act
        for term in query_act:
            assert term in query_exp

def verify_commands_equal(runner, cli, expected_result_data, command_list):
    """ Verifies that all of the specified commands pass and give the same result """
    for command in command_list:
        result = runner.invoke(cli, command)
        assert result.exit_code == 0
        data = json.loads(result.output)
        compare_dicts(expected_result_data, data)

# From Python 3 docs: https://docs.python.org/3/library/itertools.html
def powerset(iterable):
    """powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
