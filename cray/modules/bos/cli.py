"""bos

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
    def _decorator(file, name, **kwargs):
        if not file.get('value'):
            return func(name=name, **kwargs)
        with open(file["value"], 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        payload = data
        if name:
            payload['name'] = name['value']
        # Hack to tell the CLI we are passing our own payload; don't generate
        kwargs[FROM_FILE_TAG] = {"value": payload, "name": FROM_FILE_TAG}
        return func(**kwargs)
    return _decorator


def setup_template_from_file(bos_cli):
    """ Adds a --file parameter for session template creation """
    command = bos_cli.commands['sessiontemplate'].commands['create']
    option('--file', callback=_opt_callback, type=str, default='', metavar='TEXT',
           help="A file containing the json for a template")(command)
    params = [command.params[-1]]
    for param in command.params[:-1]:
        if not param.help or 'DEPRECATED' not in param.help:
            params.append(param)
    command.params = params
    command.callback = create_templates_shim(command.callback)


setup_template_from_file(cli)
