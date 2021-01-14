"""
CAPMC - Cray Advanced Platform Monitoring and Control

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
SPC_NODE_ARG = 'node'
SPC_ACCEL_ARG = 'accel'
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

option('--'+SPC_NODE_ARG, nargs=1, type=click.INT,
       payload_name=SPC_NODE_ARG,
       help="Specify the desired node level power cap. The value given must "
            "be within the range returned in the capabilities output. A value "
            "of zero may be supplied to explicitly clear an existing node "
            "level power cap. Nodes with high powered accelerators and high "
            "TDP processors will be automatically power capped at the supply "
            "limit returned per the get_power_cap_capabilities command. If a "
            "node level power cap is specified that is within the node "
            "control range but exceeds the supply limit, the actual power cap "
            "assigned will be clamped at the supply limit.")(CREATE_CMD)

option('--'+SPC_ACCEL_ARG, nargs=1, type=click.INT,
       payload_name=SPC_ACCEL_ARG,
       help="Specify the desired accelerator component power cap. The value "
            "given must be within the range returned in the capabilities "
            "output. A value of zero may be supplied to to explicitly clear "
            "an accelerator power cap.  The accelerator power cap value "
            "represents a subset of the total node level power cap. If a node "
            "level power cap of 400 watts is applied and an accelerator power "
            "cap of 180 watts is applied, then the total node power "
            "consumption is limited to 400 watts. If the accelerator is "
            "actively consuming its entire 180 watt power allocation, then "
            "the host processor, memory subsystem, and support logic for that "
            "node may consume a maximum of 220 watts.")(CREATE_CMD)

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
    elif p.payload_name == SPC_NODE_ARG:
        params.insert(1, p)
    elif p.payload_name == SPC_ACCEL_ARG:
        params.insert(2, p)
    else:
        params.append(p)

# Update the command with the new params
CREATE_CMD.params = params

def set_power_cap_shim(func):
    """ Callback function to create our own payload """
    def _decorator(nids, node, accel, **kwargs):
        if not nids['value']:
            raise click.BadParameter("--nids option required")

        if not node and not accel:
            raise click.BadParameter("--node and/or --accel must be supplied.")

        payload = {'nids':[]}
        for n in nids['value']:
            e = {'nid': n, 'controls':[]}
            if node:
                c = {
                    'name': 'node',
                    'val': node
                }
                e['controls'].append(c)


            if accel:
                c = {
                    'name': 'accel',
                    'val': accel
                }
                e['controls'].append(c)

            payload['nids'].append(e)

        # Inform the CLI that we are passing our own payload and don't generate it
        kwargs[FROM_FILE_TAG] = {"value": payload, "name": FROM_FILE_TAG}
        return func(**kwargs)
    return _decorator

# Update to create command with the callback
CREATE_CMD.callback = set_power_cap_shim(CREATE_CMD.callback)

################################################################################
#####                 cray capmc emergency_power_off create                #####
#####                                  for                                 #####
#####                   /capmc/v1/emergency_power_off API                  #####
################################################################################

CREATE_CMD = cli.commands['emergency_power_off'].commands['create']

EPO_FORCE = 'force'

option('--'+EPO_FORCE, nargs=1, type=click.BOOL, multiple=False,
       payload_name=EPO_FORCE,
       metavar='BOOLEAN',
       help="Immediately issue the emergency power off.")(CREATE_CMD)


# Add the new force command into the proper place.
params = []
for p in CREATE_CMD.params:
    if p.payload_name == EPO_FORCE:
        params.insert(2, p)
    else:
        params.append(p)

# Update the command with the new params
CREATE_CMD.params = params

def emergency_power_off_shim(func):
    """ Callback function to create our own payload """
    def _decorator(force, **kwargs):
        if not force:
            click.confirm('Are you sure you want to perform an EPO?',
                          abort=True)

        return func(**kwargs)
    return _decorator


# Update to create command with the callback
CREATE_CMD.callback = emergency_power_off_shim(CREATE_CMD.callback)
