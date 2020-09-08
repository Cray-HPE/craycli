""" Test utilities that make testing easier."""
# pylint: disable=missing-docstring, invalid-name, import-error
import os
import uuid
import toml

import names


def _uuid():
    return str(uuid.uuid4())


def new_username():
    return names.get_full_name().replace(' ', '')


def new_hostname():
    return "https://{}".format(_uuid().replace('-', ''))


def new_configname():
    return _uuid().replace('-', '')


def new_random_string():
    return _uuid().replace('-', '')


def create_config_file(filename, hostname, username):
    data = {
        'core': {'hostname': hostname},
        'auth': {'login': {'username': username}}
    }
    path = '.config/cray/configurations'
    full_path = os.path.join(path, filename)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(full_path, 'w') as f:
        toml.dump(data, f)

def strip_confirmation(output):
    return "\n".join(output.splitlines()[1:])
