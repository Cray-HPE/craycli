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
""" hsm """

# pylint: disable=invalid-name

from cray.constants import FROM_FILE_TAG
from cray.core import option
from cray.generator import _opt_callback
from cray.generator import generate

SWAGGER_OPTS = {
    'vocabulary': {
        'put': 'replace',
        'deleteall': 'clear'
    }
}


# Keeping for future API versions
# HSM_API_VERSION = os.environ.get("CRAY_HSM_API_VERSION", "v2")

def setup(hsm_cli):
    """ Sets up all HSM overrides """
    setup_groups_partitions_create(hsm_cli, 'groups')
    setup_groups_partitions_create(hsm_cli, 'partitions')
    setup_redfish_endpoints_update(hsm_cli)
    setup_redfish_endpoints_create(hsm_cli)


# Groups and Partitions #

def create_groups_partitions_create_shim(func):
    """ Callback function to custom create our own payload """

    def _decorator(members_file, members_ids, **kwargs):
        payload = {v['name']: v['value'] for _, v in kwargs.items() if
                   v['value'] is not None}
        file_name = members_file['value']
        if file_name:
            with open(members_file['value'], 'r', encoding='utf-8') as f:
                data = f.read()
            payload['members'] = {
                'ids': data.strip().split(',')
            }
        elif members_ids['value']:
            payload['members'] = {
                'ids': members_ids['value']
            }
        # Hack to tell the CLI we are passing our own payload; don't generate
        kwargs[FROM_FILE_TAG] = {"value": payload, "name": FROM_FILE_TAG}
        return func(**kwargs)

    return _decorator


def setup_groups_partitions_create(hsm_cli, command):
    """ Adds the --file parameter for groups create """
    create_command = hsm_cli.commands[command].commands['create']

    option(
        '--members-file', callback=_opt_callback, type=str, metavar='TEXT',
        help="A file containing a comma-separated list of xnames to be added as members."
             " This overrides --members-ids."
    )(create_command)
    new_params = create_command.params[-1:]
    for param in create_command.params[:-1]:
        new_params.append(param)
    create_command.params = new_params
    create_command.callback = create_groups_partitions_create_shim(
        create_command.callback
    )

    hsm_cli.commands[command].commands['create'] = create_command


# redfishEndpoints update #
def setup_redfish_endpoints_update(hsm_cli):
    """ Added a fix for the hostname being set to the cray global hostname """
    update_command = hsm_cli.commands["inventory"].commands["redfishEndpoints"].commands['update']
    update_command.callback = create_re_create_and_update_shim(update_command.callback)


# redfishEndpoints create #
def setup_redfish_endpoints_create(hsm_cli):
    """ Added a fix for the hostname being set to the cray global hostname """
    create_command = hsm_cli.commands["inventory"].commands["redfishEndpoints"].commands['create']
    create_command.callback = create_re_create_and_update_shim(create_command.callback)


def create_re_create_and_update_shim(func):
    """ This causes the call to ignore any hostname value that starts with http: or https:
    The top level cray command has a --hostname option which is stored in the config file
    and its value gets passed through here when the user doesn't specify the hsm flavor
    of the --hostname option """

    def _decorator(**kwargs):
        hostname = kwargs.get("hostname")
        if hostname:
            value = hostname.get("value")
            if value and (value.lower().startswith("https:") or value.lower().startswith("http:")):
                hostname["value"] = None
                kwargs["hostname"] = hostname

        return func(**kwargs)

    return _decorator


# Keeping for future API versions
# if HSM_API_VERSION == 'v1':
# cli = generate(__file__, filename='swagger3_v1.json', swagger_opts=SWAGGER_OPTS)
# else:
cli = generate(
    __file__,
    filename='swagger3_v2.json',
    swagger_opts=SWAGGER_OPTS
)
setup(cli)
