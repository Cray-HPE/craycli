"""
ims
Copyright 2020 Hewlett Packard Enterprise Development LP
"""

# pylint: disable=invalid-name
import click

from cray.generator import generate


CURRENT_VERSION = 'v3'
SWAGGER_OPTS = {
    'vocabulary': {
        'deleteall': 'deleteall'
    }
}

cli = generate(__file__,  condense=False, swagger_opts=SWAGGER_OPTS)
version = cli.commands["version"]
cli.commands = cli.commands[CURRENT_VERSION].commands
cli.commands["version"] = version


def _file_cb(cb):

    def _cb(ctx, param, value):
        data = value.read()
        if cb:
            return cb(ctx, param, data)
        return data
    return _cb

for p in cli.commands['public-keys'].commands['create'].params:
    if p.payload_name == 'public_key':
        p.type = click.File(mode='r')
        p.callback = _file_cb(p.callback)
        break
