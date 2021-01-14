"""bos"""
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
        with open(file["value"], 'r') as f:
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
