"""
CAPMC - Cray Advanced Platform Monitoring and Control

MIT License

(C) Copyright [2020-2021] Hewlett Packard Enterprise Development LP

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
import click

from cray.core import option
from cray.generator import generate, _opt_callback
from cray.constants import FROM_FILE_TAG

cli = generate(__file__, condense=False)

################################################################################
#####                    cray capmc set_power_cap create                   #####
#####                                  for                                 #####
#####                      /capmc/v1/set_power_cap API                     #####
################################################################################

SPC_NIDS_ARG = 'nids'
SPC_CTL_ARG = 'control'
SPC_OLD_NCV = 'nids-controls-val'
SPC_OLD_NCN = 'nids-controls-name'
SPC_OLD_NIDS = 'nids-nid'

CREATE_CMD = cli.commands['set_power_cap'].commands['create']

def _set_power_cap_callback(cb):
    """ Manage the command line options """
    def _cb(ctx, param, value):
        nids = []
        for x in value:
            # Handle nid ranges here
            nids = [int(m.strip()) for m in x.split(',')]
        if cb:
            return cb(ctx, param, nids)
        return nids
    return _cb

option('--'+SPC_NIDS_ARG, nargs=1, type=click.STRING, multiple=True,
       payload_name=SPC_NIDS_ARG,
       callback=_set_power_cap_callback(_opt_callback),
       metavar='INTEGER,...',
       help="Specify the NIDs to apply the specified power caps. The syntax "
            "allows a comma-separated list of nids (e.g. 1,4,5). This option "
            "may not be omitted. Ths specified NIDs must be in the ready "
            "state per the node_status command.")(CREATE_CMD)

option('--'+SPC_CTL_ARG, type=(click.STRING, click.INT),
       payload_name=SPC_CTL_ARG, multiple=True,
       help="Specify the desired power cap for the specified control. The "
            "value given must be within the range returned in the "
            "capabilities output. A value of zero may be supplied to "
            "explicitly clear an existing power cap. Nodes with high powered "
            "accelerators and high TDP processors will be automatically power "
            "capped at the supply limit returned per the "
            "get_power_cap_capabilities command. If a power cap is specified "
            "that is within the control range but exceeds the supply limit, "
            "the actual power cap assigned will be clamped at the supply "
            "limit.")(CREATE_CMD)

# Remove the generated params for the group names and group member lists.
# Add the new target-groups option.
params = []
for p in CREATE_CMD.params:
    if p.payload_name in (SPC_OLD_NCV, SPC_OLD_NCN, SPC_OLD_NIDS):
        continue
    # Hack to force order in list in front of globals
    # only for making the UX better
    if p.payload_name == SPC_NIDS_ARG:
        params.insert(0, p)
    elif p.payload_name == SPC_CTL_ARG:
        params.insert(1, p)
    else:
        params.append(p)

# Update the command with the new params
CREATE_CMD.params = params

def set_power_cap_shim(func):
    """ Callback function to create our own payload """
    def _decorator(nids, control, **kwargs):
        if not nids['value']:
            raise click.BadParameter("--nids option required")

        if not control:
            raise click.BadParameter("--control must be supplied.")

        payload = {'nids':[]}
        for n in nids['value']:
            e = {'nid': n, 'controls':[]}
            for ctl in control:
                c = {
                    'name': ctl[0],
                    'val': ctl[1]
                }
                e['controls'].append(c)

            payload['nids'].append(e)

        # Inform the CLI that we are passing our own payload and don't generate it
        kwargs[FROM_FILE_TAG] = {"value": payload, "name": FROM_FILE_TAG}
        return func(**kwargs)
    return _decorator

# Update to create command with the callback
CREATE_CMD.callback = set_power_cap_shim(CREATE_CMD.callback)

