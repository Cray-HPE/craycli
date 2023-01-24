"""Content Projection Service

MIT License

(C) Copyright [2022-2023] Hewlett Packard Enterprise Development LP

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
import re
import json
from http import HTTPStatus
import click

from cray import hostlist
from cray.core import option, argument, pass_context
from cray.errors import BadResponseError
from cray.generator import generate
from cray.rest import request

PCS = 'apis/power-control/v1'
SMD = 'apis/smd/hsm/v2'

CONTROL_NAME = 0
CONTROL_VALUE = 1

###########################################################################
# cray power
###########################################################################
cli = generate(__file__, name="power", condense=True)

def xname_array(xnames):
    """
    Take the xnames tuple and pass each element through the hostlist expansion.
    Take the resulting string and split it into an array of xnames then add
    those to the xname array. Return the new xname array.
    """
    xarr = []
    for x in xnames:
        xarr += hostlist.expand(x).split(',')
    return xarr

def is_Node(xname):
    """ Check to see if the xname passed in matches the format of a node. """
    if re.match("^x([0-9]{1,4})c([0-7])s([0-9]+)b([0-9]+)n([0-9]+)$", xname):
        return True
    return False

def is_Module(xname):
    """ Check to see if the xname passed in matches the format of a module. """
    if re.match("^x([0-9]{1,4})c([0-7])[sr]([0-9]+)$", xname):
        return True
    return False

def is_Chassis(xname):
    """ Check to see if the xname passed in matches the format of a chassis. """
    if re.match("^x([0-9]{1,4})c([0-7])$", xname):
        return True
    return False

def get_module(xname):
    """ Return the module portion of an xname. """
    mod = re.match("^x([0-9]{1,4})c([0-7])[sr]([0-9]+)", xname)
    if mod:
        return mod.group(0)
    return ""

def get_chassis(xname):
    """ Return the chassis portion of an xname. """
    chas =  re.match("^x([0-9]{1,4})c([0-7])", xname)
    if chas:
        return chas.group(0)
    return ""

def component_valid(xname, globalComponents):
    """
    Check with the state manager to determine if the xname is valid. Checks for
    enable/disabled or empty state will be done by PCS. This is used to weed out
    hardware that doesn't exist such as chassis and compute/router modules in
    River racks.
    """
    if len(globalComponents) == 0:
        url = SMD+"/State/Components"
        resp = request('GET', url)

        if resp.status_code >= HTTPStatus.BAD_REQUEST:
            raise BadResponseError(resp)

        globalComponents = json.loads(resp.content)

    for c in globalComponents['Components']:
        if xname == c['ID']:
            return True

    return False

def add_parents(xarr):
    """
    Take an array of xnames and return a new array that has been expanded to
    include all parents of the original xnames, along with the original xames.
    """
    globalComponents = []
    narr = xarr.copy()
    for x in xarr:
        slot = ''
        chassis = ''
        if is_Node(x) is True:
            slot = get_module(x)
            chassis = get_chassis(x)
        if is_Module(x) is True:
            chassis = get_chassis(x)
        if slot != '':
            if component_valid(slot, globalComponents) is True:
                narr.append(slot)
        if chassis != '':
            if component_valid(chassis, globalComponents) is True:
                narr.append(chassis)

    return narr

def add_children(xarr):
    """
    Take an array of xnames and return a new array that has been expanded to
    include all children of the original xnames, along with the original xnames.
    """
    url = SMD+"/State/Components/Query/"
    query = ''
    narr = xarr.copy()
    for x in xarr:
        if is_Node(x) is True:
            continue
        if is_Module(x) is True:
            query="?type=computemodule&type=routermodule&type=node"
        elif is_Chassis(x) is True:
            query="?type=chassis&type=computemodule&type=routermodule&type=node"

        exclude = "&state!=empty&enabled=true"

        resp = request('GET', url+x+query+exclude)

        if resp.status_code >= HTTPStatus.BAD_REQUEST:
            raise BadResponseError(resp)

        body = json.loads(resp.content)
        for c in body['Components']:
            narr.append(c['ID'])

    return narr

def execute_transition(ctx, xnames, include, op):
    """ Initiates a transition to the xnames based on the 'op' """
    #pylint: disable=unused-argument
    xarr = xname_array(xnames)
    # Always gather the children first, otherwise we will get everything
    # in the cabinet.
    for inc in sorted(include):
        if inc == "children":
            xarr = add_children(xarr)
        elif inc == "parents":
            xarr = add_parents(xarr)

    # Generate a uniq list then sort it
    xarr = list(set(xarr))
    xarr.sort()

    tReq = {}
    tReq['location'] = []
    # CrayCLI doesn't allow the use of 'init' as a subcommand. Reinit is used
    # for the PCS CLI but needs conversion to the PCS API's 'init'.
    if op == 'reinit':
        tReq['operation'] = 'init'
    else:
        tReq['operation'] = op

    for x in xarr:
        loc = {}
        loc['xname'] = x
        tReq['location'].append(loc)

    resp = request('POST', PCS+'/transitions', json=tReq)

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()

###########################################################################
# cray power transition
###########################################################################
@cli.group()
def transition():
    """ Power state transitions """
    pass

###########################################################################
# cray power transition on
###########################################################################
@transition.command(name='on')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=True,
        help='Target list of components to turn On.')
@option('--include', multiple=True,
        type=click.Choice(['parents','children']), required=False,
        help='Optionally include all parents or all children of target components.')
@pass_context
def transition_on(ctx, xnames, include):
    """ Transition targets to the On power state """
    return execute_transition(ctx, xnames, include, 'on')

###########################################################################
# cray power transition off
###########################################################################
@transition.command(name='off')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=True,
        help='Target list of components to turn Off.')
@option('--include', multiple=True,
        type=click.Choice(['parents','children']), required=False,
        help='Optionally include all parents or all children of target components.')
@pass_context
def transition_off(ctx, xnames, include):
    """ Transition targets to the Off power state """
    return execute_transition(ctx, xnames, include, 'off')

###########################################################################
# cray power transition soft-off
###########################################################################
@transition.command(name='soft-off')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=True,
        help='Target list of components to soft-off.')
@option('--include', multiple=True,
        type=click.Choice(['parents','children']), required=False,
        help='Optionally include all parents or all children of target components.')
@pass_context
def transition_soft_off(ctx, xnames, include):
    """ Issue a soft-off to the target components """
    return execute_transition(ctx, xnames, include, 'soft-off')

###########################################################################
# cray power transition soft-restart
###########################################################################
@transition.command(name='soft-restart')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=True,
        help='Target list of components to soft-restart.')
@option('--include', multiple=True,
        type=click.Choice(['parents','children']), required=False,
        help='Optionally include all parents or all children of target components.')
@pass_context
def transition_soft_restart(ctx, xnames, include):
    """ Issue a soft-restart to the target components """
    return execute_transition(ctx, xnames, include, 'soft-restart')

###########################################################################
# cray power transition hard-restart
###########################################################################
@transition.command(name='hard-restart')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=True,
        help='Target list of components to hard-restart.')
@option('--include', multiple=True,
        type=click.Choice(['parents','children']), required=False,
        help='Optionally include all parents or all children of target components.')
@pass_context
def transition_hard_restart(ctx, xnames, include):
    """ Power Off target components that are already On, then power them back On """
    return execute_transition(ctx, xnames, include, 'hard-restart')

###########################################################################
# cray power transition reinit
###########################################################################
@transition.command(name='reinit')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=True,
        help='Target list of components to turn On.')
@option('--include', multiple=True,
        type=click.Choice(['parents','children']), required=False,
        help='Optionally include all parents or all children of target components.')
@pass_context
def transition_reinit(ctx, xnames, include):
    """ Power Off target components that are already On, powers On all targets components """
    return execute_transition(ctx, xnames, include, 'reinit')

###########################################################################
# cray power transition force-off
###########################################################################
@transition.command(name='force-off')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=True,
        help='Target list of components to force Off.')
@option('--include', multiple=True,
        type=click.Choice(['parents','children']), required=False,
        help='Optionally include all parents or all children of target components.')
@pass_context
def transition_force_off(ctx, xnames, include):
    """
    Issues a force Off to all target components. This is not a graceful
    shutdown.
    """
    return execute_transition(ctx, xnames, include, 'force-off')

###########################################################################
# cray power transition list
###########################################################################
@transition.command(name='list')
@pass_context
def transition_list(ctx):
    """ List all active transition IDs """
    #pylint: disable=unused-argument
    resp = request('GET', PCS+'/transitions')

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()

###########################################################################
# cray power transition describe
###########################################################################
@transition.command(name='describe')
@argument('transitionid')
@pass_context
def transition_describe(ctx, transitionid):
    """ Describe transition """
    #pylint: disable=unused-argument
    url = PCS+'/transitions/'
    resp = request('GET', url+transitionid)

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()

###########################################################################
# cray power transition delete
###########################################################################
@transition.command(name='delete')
@argument('transitionid')
@pass_context
def transition_delete(ctx, transitionid):
    """ Delete transition """
    #pylint: disable=unused-argument
    url = PCS+'/transitions/'
    resp = request('DELETE', url+transitionid)

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()

###########################################################################
# cray power status
###########################################################################
@cli.group()
def status():
    """ Power state query """
    pass

###########################################################################
# cray power status list
###########################################################################
@status.command(name='list')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=False,
        help='Target list of components to query status for.')
@option('--include', multiple=True,
        type=click.Choice(['parents','children']), required=False,
        help='Optionally include all parents or all children of target components.')
@option('--powerfilter', multiple=False,
        type=click.Choice(['on', 'off', 'undefined']), required=False,
        help='Show only components that are On, Off, or the state is unknown.')
@option('--mgmtfilter', multiple=False,
        type=click.Choice(['available', 'unavailable']), required=False,
        help='Show only management components that are available or unavailable.')
@pass_context
def status_list(ctx, xnames, powerfilter, mgmtfilter, include):
    """ List power status of target components """
    #pylint: disable=unused-argument
    # There is a limit to the length of the URL that can be used due to istio.
    # If there are too many query parameters, they need to be broken up into
    # multiple requests to PCS. CAPMC previous used 2k chunks for the maximum
    # number of xnames it queried HSM with at one time.
    xarr = xname_array(xnames)
    # Always gather the children first, otherwise we will get everything
    # in the cabinet.
    for inc in sorted(include):
        if inc == "children":
            xarr = add_children(xarr)
        elif inc == "parents":
            xarr = add_parents(xarr)

    # Generate a uniq list then sort it
    xarr = list(set(xarr))
    xarr.sort()

    # Add all URL parameters via tuples. This allows for duplicate parameter
    # names so we can query multiple xnames at once.
    aParams = []
    if powerfilter is not None:
        tParam = ('powerStateFilter', powerfilter)
        aParams.append(tParam)

    if mgmtfilter is not None:
        tParam = ('managementStateFilter', mgmtfilter)
        aParams.append(tParam)

    for x in xarr:
        tParam = ('xname',x)
        aParams.append(tParam)

    resp = request('GET', PCS+'/power-status', params=aParams)

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()

###########################################################################
# cray power status describe
###########################################################################
@status.command(name='describe')
@argument('xname', metavar='XNAME')
@pass_context
def status_describe(ctx, xname):
    """ Show power status of target component """
    #pylint: disable=unused-argument

    aParams = [('xname',xname)]
    resp = request('GET', PCS+'/power-status', params=aParams)

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()

###########################################################################
# cray power cap
###########################################################################
@cli.group()
def cap():
    """ Power capping """
    pass

###########################################################################
# cray power cap snapshot
###########################################################################
@cap.command(name='snapshot')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=True,
        help='Target list of components to query power capping on.')
@pass_context
def cap_snapshot(ctx, xnames):
    """ Query power capping setting on target components """
    #pylint: disable=unused-argument
    tReq = {}
    tReq['xnames'] = xname_array(xnames)

    resp = request('POST', PCS+'/power-cap/snapshot', json=tReq)

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()

###########################################################################
# cray power cap set
###########################################################################
@cap.command(name='set')
@option('--xnames', metavar='XNAME,...|EXPR', multiple=True, required=True,
        help='Target list of components to set power capping on.')
@option('--control', metavar='<CONTROL-NAME> <VALUE>', multiple=True,
        required=True, type=(click.STRING, click.INT),
        help='Set power cap on target components.')
@pass_context
def cap_set(ctx, xnames, control):
    """ Set power capping on target components """
    #pylint: disable=unused-argument
    xarr = xname_array(xnames)
    # Generate a uniq list then sort it
    xarr = list(set(xarr))
    xarr.sort()

    controls = []

    for c in control:
        ctl = {}
        ctl['name'] = c[CONTROL_NAME]
        ctl['value'] = c[CONTROL_VALUE]
        controls.append(ctl)

    tReq = {}
    tReq['components'] = []

    for x in xarr:
        comp = {}
        comp['xname'] = x
        comp['controls'] = controls
        tReq['components'].append(comp)

    resp = request('PATCH', PCS+'/power-cap', json=tReq)

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()

###########################################################################
# cray power cap list
###########################################################################
@cap.command(name='list')
@pass_context
def cap_list(ctx):
    """ List power capping tasks """
    #pylint: disable=unused-argument
    resp = request('GET', PCS+'/power-cap')

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()

###########################################################################
# cray power cap describe
###########################################################################
@cap.command(name='describe')
@argument('powercapid', metavar='POWERCAPID')
@pass_context
def cap_describe(ctx, powercapid):
    """ Describe power capping task. """
    #pylint: disable=unused-argument
    url = PCS+'/power-cap/'
    resp = request('GET', url+powercapid)

    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        raise BadResponseError(resp)

    return resp.json()
