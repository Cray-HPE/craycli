"""bos

MIT License

(C) Copyright [2020, 2022-2023] Hewlett Packard Enterprise Development LP

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
# pylint: disable=invalid-name
import json

from cray.core import option
from cray.generator import generate, _opt_callback
from cray.constants import FROM_FILE_TAG

SWAGGER_OPTS = {
    # 'ignore_endpoints': [
    #     '/v1/session/{session_id}/status/{boot_set_name}'
    # ]
}

cli = generate(__file__, swagger_opts=SWAGGER_OPTS)

# Place the v1 commands at the 'cray bos' level of the cli
CURRENT_VERSION = 'v1'
PRESERVE_VERSIONS = True

if PRESERVE_VERSIONS:
    cli.commands.update(cli.commands[CURRENT_VERSION].commands)
else:
    cli.commands = cli.commands[CURRENT_VERSION].commands


# Add --file parameter for specifying session template data
def create_templates_shim(func):
    """ Callback function to custom create our own payload """
    def _decorator(file, **kwargs):
        if not file.get('value'):
            return func(**kwargs)
        with open(file["value"], 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        payload = data
        if 'name' in kwargs:
            payload['name'] = kwargs['name']['value']
            del kwargs['name']
        # Hack to tell the CLI we are passing our own payload; don't generate
        kwargs[FROM_FILE_TAG] = {"value": payload, "name": FROM_FILE_TAG}
        return func(**kwargs)
    return _decorator


def setup_template_from_file(command):
    """ Adds a --file parameter for session template creation """
    option('--file', callback=_opt_callback, type=str, default='', metavar='TEXT',
           help="A file containing the JSON for a template")(command)
    params = [command.params[-1]]
    for param in command.params[:-1]:
        if not getattr(param, 'help', None) or 'DEPRECATED' not in param.help:
            params.append(param)
    command.params = params
    command.callback = create_templates_shim(command.callback)


def updatemany_data_handler(args):
    """ Handler to override the api action taken for updatemany """
    _, path, data = args
    return "PATCH", path, data


def create_patch_shim(func):
    """ Callback function to custom create our own payload """
    def _decorator(filter_ids, filter_session, patch, enabled, **kwargs):
        filter_ids=filter_ids["value"]
        filter_session=filter_session["value"]
        if not (filter_ids or filter_session):
            raise Exception('Either the IDs or session filter must be provided')
        if filter_ids and filter_session:
            raise Exception('Only one of the two filter options can be provided')
        payload = {}
        if filter_ids:
            payload["filters"] = {"ids": filter_ids}
        if filter_session:
            payload["filters"] = {"session": filter_session}
        if patch["value"]:
            payload["patch"] = json.loads(patch["value"])
        else:
            payload["patch"] = {}
        if enabled["value"] is not None:
            payload["patch"]["enabled"] = enabled["value"]
        # Hack to tell the CLI we are passing our own payload; don't generate
        kwargs[FROM_FILE_TAG] = {"value": payload, "name": FROM_FILE_TAG}
        return func(data_handler=updatemany_data_handler, **kwargs)
    return _decorator


def setup_components_patch():
    """ Sets up an updatemany command for components """
    source_command = cli.commands['v2'].commands['components'].commands['list']
    command_type = type(source_command)
    new_command = command_type("updatemany")
    for key, value in source_command.__dict__.items():
        setattr(new_command, key, value)
    cli.commands['v2'].commands['components'].commands['updatemany'] = new_command
    new_command.params = []
    default_params = [param for param in source_command.params if not param.expose_value]
    option('--filter-ids', callback=_opt_callback, type=str, default='', metavar='TEXT',
           help="A comma-separated list of nodes to patch")(new_command)
    option('--filter-session', callback=_opt_callback, type=str, default='', metavar='TEXT',
           help="Patch all components owned by this session")(new_command)
    option('--patch', callback=_opt_callback, type=str, default='', metavar='TEXT',
           help="Json component data applied to all filtered components")(new_command)
    option('--enabled', callback=_opt_callback, type=bool, default=None, metavar='BOOLEAN',
           help="Shortcut for --patch '{\"enabled\":True/False}'")(new_command)
    new_command.params += default_params
    new_command.callback = create_patch_shim(new_command.callback)


def setup_v2_template_create():
    """ Sets up a sessiontemplate create operation in addition to the update operation """
    TEMP_SWAGGER_OPTS = {
        'vocabulary': {
            'put': 'create'
        }
    }
    temp_cli = generate(__file__, swagger_opts=TEMP_SWAGGER_OPTS)
    cli.commands['v2'].commands['sessiontemplates'].commands['create'] = \
        temp_cli.commands['v2'].commands['sessiontemplates'].commands['create']



setup_v2_template_create()

setup_template_from_file(cli.commands['v1'].commands['sessiontemplate'].commands['create'])
setup_template_from_file(cli.commands['v2'].commands['sessiontemplates'].commands['create'])
setup_template_from_file(cli.commands['v2'].commands['sessiontemplates'].commands['update'])

setup_components_patch()
