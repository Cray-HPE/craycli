""" Cray User Access Manager """
# pylint: disable=invalid-name
import click

from cray.generator import generate


cli = generate(__file__)


def _check_for_private_key(existing_callback):
    """Returns a function that ensures a private key will not hit the wire."""

    def _callback(ctx, param, value):
        cb_data = existing_callback(ctx, param, value)

        # NOTE: This unfortunately means the file is opened twice, once here
        #       and again in cray.generate._parse_data.
        with open(cb_data["value"], "rb") as f:
            pubkey = f.read()

        if b"PRIVATE KEY" in pubkey:
            raise click.UsageError(
                "Please specify a properly formatted public key. It "
                "appears that you are trying to use your private key."
            )

        return cb_data

    return _callback


cmd = cli.commands["create"]
for p in cmd.params:
    if p.name == "publickey":
        p.callback = _check_for_private_key(p.callback)
        break
