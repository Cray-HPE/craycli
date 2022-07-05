# MIT License
#
# (C) Copyright [2020,2022] Hewlett Packard Enterprise Development LP
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

# pylint: disable=invalid-name

""" sls """

import json
import os
import click

from cray.core import option
from cray.generator import generate, _opt_callback
from cray.constants import FROM_FILE_TAG


def _validate_options(
        is_update, xname_value, class_value, extra_properties_value, payload_file_value):
    if payload_file_value:
        if is_update:
            if class_value or extra_properties_value:
                raise click.BadParameter(
                    "The --payload-file option cannot be combined with other options")
        else:
            if xname_value or class_value or extra_properties_value:
                raise click.BadParameter(
                    "The --payload-file option cannot be combined with other options")
    else:
        if not xname_value:
            raise click.BadParameter("The --xname option is required")
        if not class_value:
            raise click.BadParameter("The --class option is required")
    pass


def _set_hardware_shim(func, is_update=False):
    """ Callback function to create our own payload """

    def _decorator(extra_properties, payload_file, **kwargs):
        xname_value = kwargs.get('xname', {}).get('value')
        class_value = kwargs.get('class', {}).get('value')
        extra_properties_value = extra_properties.get('value')
        payload_file_value = payload_file.get('value')

        _validate_options(
            is_update, xname_value, class_value, extra_properties_value, payload_file_value)

        # build new payload
        payload = {}
        if payload_file_value:
            if not os.path.exists(payload_file_value):
                raise click.BadParameter(
                        f"--payload-file {payload_file_value} file does not exist.")

            with open(payload_file_value, mode='r', encoding='utf-8') as f:
                json_string = f.read()
                try:
                    payload = json.loads(json_string)
                except ValueError as e:
                    raise click.BadParameter(
                            f"The contents of {payload_file_value} is not valid json.") from e
        else:
            if extra_properties_value:
                try:
                    extra_properties_parsed = json.loads(extra_properties_value)
                    payload['ExtraProperties'] = extra_properties_parsed
                except ValueError as e:
                    raise click.BadParameter(f"{extra_properties_value} is not valid json.") from e

            for key, value in kwargs.items():
                name = value.get('name') if value.get('name') else key
                payload[name] = value['value']

        # Inform the CLI that we are passing our own payload and don't generate it
        kwargs[FROM_FILE_TAG] = {"value": payload, "name": FROM_FILE_TAG}
        return func(**kwargs)
    return _decorator


def _setup_hardware_options(cmd, is_update=False):
    option_extra_properties = 'extra-properties'
    option_payload_file = 'payload-file'

    option('--'+option_extra_properties, nargs=1, type=click.STRING, multiple=False,
           payload_name=option_extra_properties,
           callback=_opt_callback,
           help="The extra properties as a json string")(cmd)

    option('--'+option_payload_file, nargs=1, type=click.STRING, multiple=False,
           payload_name=option_payload_file,
           callback=_opt_callback,
           help="A file that contains the json for the hardware")(cmd)

    params = []
    for p in cmd.params:
        i = 4
        if p.payload_name == 'Xname':
            params.append((0, p))
        elif p.payload_name == 'Class':
            params.append((1, p))
        elif p.payload_name == option_extra_properties:
            params.append((2, p))
        elif p.payload_name == option_payload_file:
            params.append((3, p))
        elif p.payload_name == 'ExtraProperties':
            # pylint: disable=fixme
            # todo
            pass
        else:
            params.append((i, p))
            i = i + 1

    sorted_params = sorted(params, key = lambda x: x[0])
    cmd.params = [ p[1] for p in sorted_params ]
    cmd.callback = _set_hardware_shim(cmd.callback, is_update=is_update)


def _clear_required_parameters(cmd, parameter_names):
    for p in cmd.get_params(click.get_current_context()):
        if hasattr(p, 'payload_name'):
            if p.payload_name in parameter_names:
                p.required = False


# Main #

cli = generate(__file__, condense=False)

create_cmd = cli.commands['hardware'].commands['create']
_clear_required_parameters(create_cmd, [ 'Xname', 'Class' ])
_setup_hardware_options(create_cmd)

modify_cmd = cli.commands['hardware'].commands['update']
_clear_required_parameters(modify_cmd, [ 'Class' ])
_setup_hardware_options(modify_cmd, is_update=True)
