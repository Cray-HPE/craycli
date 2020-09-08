"""ims"""
# pylint: disable=invalid-name
import click

from cray.generator import generate


cli = generate(__file__)


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
