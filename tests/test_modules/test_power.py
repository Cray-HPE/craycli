""" Test the main CLI command hostlist expansion .

MIT License

(C) Copyright [2022] Hewlett Packard Enterprise Development LP

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
# pylint: disable=too-many-arguments, unused-argument
# pylint: disable=too-many-lines

import json
# import click

import requests_mock as req_mock
import pytest

# from cray.core import pass_context

# from cray.modules.power.cli import component_valid
from cray.modules.power.cli import xname_array
from cray.modules.power.cli import is_Node, is_Module, is_Chassis
from cray.modules.power.cli import get_module, get_chassis
# from cray.modules.power.cli import add_parents

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import

##############################################################################
# MOCKS
##############################################################################

def _x1000c0s0_request_cb(request, context):
    return '''{ "Components": [ { "ID": "x1000c0s0b1n0" },
        { "ID": "x1000c0s0b0n1" }, { "ID": "x1000c0s0b1n1" },
        { "ID": "x1000c0s0" }, { "ID": "x1000c0s0b0n0" } ] }'''

def _x1000c0_request_cb(request, context):
    return '''{ "Components": [
        { "ID": "x1000c0s7" }, { "ID": "x1000c0s3b1n1" }, { "ID": "x1000c0s2" },
        { "ID": "x1000c0s0" }, { "ID": "x1000c0s4" }, { "ID": "x1000c0s6" },
        { "ID": "x1000c0s3" }, { "ID": "x1000c0s1" }, { "ID": "x1000c0s0b0n0" },
        { "ID": "x1000c0s5b0n1" }, { "ID": "x1000c0s2b0n0" }, { "ID": "x1000c0s5" },
        { "ID": "x1000c0s7b1n1" }, { "ID": "x1000c0s7b1n0" }, { "ID": "x1000c0" },
        { "ID": "x1000c0r6" }, { "ID": "x1000c0r7" }, { "ID": "x1000c0r0" },
        { "ID": "x1000c0r1" }, { "ID": "x1000c0r5" }, { "ID": "x1000c0r2" },
        { "ID": "x1000c0r3" }, { "ID": "x1000c0r4" }, { "ID": "x1000c0s4b1n1" },
        { "ID": "x1000c0s4b1n0" }, { "ID": "x1000c0s6b0n0" }, { "ID": "x1000c0s2b0n1" },
        { "ID": "x1000c0s1b1n0" }, { "ID": "x1000c0s1b1n1" }, { "ID": "x1000c0s3b0n1" },
        { "ID": "x1000c0s2b1n1" }, { "ID": "x1000c0s3b0n0" }, { "ID": "x1000c0s2b1n0" },
        { "ID": "x1000c0s1b0n1" }, { "ID": "x1000c0s5b1n1" }, { "ID": "x1000c0s5b1n0" },
        { "ID": "x1000c0s4b0n1" }, { "ID": "x1000c0s4b0n0" }, { "ID": "x1000c0s7b0n1" },
        { "ID": "x1000c0s7b0n0" }, { "ID": "x1000c0s0b0n1" }, { "ID": "x1000c0s6b0n1" },
        { "ID": "x1000c0s0b1n0" }, { "ID": "x1000c0s1b0n0" }, { "ID": "x1000c0s6b1n0" },
        { "ID": "x1000c0s3b1n0" }, { "ID": "x1000c0s5b0n0" }, { "ID": "x1000c0s6b1n1" },
        { "ID": "x1000c0s0b1n1" }
        ] }'''


@pytest.fixture()
def pcs_rest_mock(requests_mock):
    """ Catch any rest callouts and return the request info instead """
    # pylint: disable=protected-access
    requests_mock._adapter.register_uri(req_mock.GET,
        '/apis/smd/hsm/v2/State/Components/Query/x1000c0s0?type=computemodule'+
            '&type=routermodule&type=node',
        text=_x1000c0s0_request_cb)
    requests_mock._adapter.register_uri(req_mock.GET,
        '/apis/smd/hsm/v2/State/Components/Query/x1000c0?type=chassis'+
            '&type=computemodule&type=routermodule&type=node',
        text=_x1000c0_request_cb)
    requests_mock._adapter.register_uri(req_mock.GET,
        '/apis/smd/hsm/v2/State/Components',
        text=_x1000c0_request_cb)

##############################################################################
# SUPPORT FUNCTIONS
##############################################################################

# pylint: disable=redefined-outer-name
def test_xname_array():
    """ Test array expansion of xnames """

    expected = ['x1000c0s0b0n0','x1000c0s0b0n1','x1000c1s0b0n0','x1000c1s0b0n1']
    xnames = ('x1000c[0-1]s0b0n[0-1]',)
    output = xname_array(xnames)
    assert expected == output

    expected = ['x1c0','x1c1','x5c0','x5c1']
    xnames = ('x1c[0-1]', 'x5c[0-1]')
    output = xname_array(xnames)
    assert expected == output

    expected = ['x1000c0','x1000c1','x1000c5']
    xnames = ('x1000c[0-1,5]',)
    output = xname_array(xnames)
    assert expected == output

cabinet_str = 'x1000'
chassis_str = 'x1000c0'
cc = 'x1000c0b0'
rmodule = 'x1000c0r0'
sc = 'x1000c0r0b0'
cmodule = 'x1000c0s0'
nc = 'x1000c0s0b0'
n = 'x1000c0s0b0n0'

def test_is_Node():
    """ Test node identification """

    output = is_Node(chassis_str)
    assert not output

    output = is_Node(cc)
    assert not output

    output = is_Node(rmodule)
    assert not output

    output = is_Node(sc)
    assert not output

    output = is_Node(cmodule)
    assert not output

    output = is_Node(nc)
    assert not output

    output = is_Node(n)
    assert output

def test_is_Module():
    """ Test is_Module identification """

    output = is_Module(chassis_str)
    assert not output

    output = is_Module(cc)
    assert not output

    output = is_Module(rmodule)
    assert output

    output = is_Module(sc)
    assert not output

    output = is_Module(cmodule)
    assert output

    output = is_Module(nc)
    assert not output

    output = is_Module(n)
    assert not output

def test_is_Chassis():
    """ Test is_Chassis identification """

    output = is_Chassis(chassis_str)
    assert output

    output = is_Chassis(cc)
    assert not output

    output = is_Chassis(rmodule)
    assert not output

    output = is_Chassis(sc)
    assert not output

    output = is_Chassis(cmodule)
    assert not output

    output = is_Chassis(nc)
    assert not output

    output = is_Chassis(n)
    assert not output

def test_get_module():
    """ Test pulling module out of xname """

    output = get_module(n)
    assert output == cmodule

    output = get_module(nc)
    assert output == cmodule

    output = get_module(cmodule)
    assert output == cmodule

    output = get_module(sc)
    assert output == rmodule

    output = get_module(rmodule)
    assert output == rmodule

    output = get_module(cc)
    assert output == ''

    output = get_module(chassis_str)
    assert output == ''

def test_get_chassis():
    """ Test pulling chassis out of xname """

    output = get_chassis(n)
    assert output == chassis_str

    output = get_chassis(nc)
    assert output == chassis_str

    output = get_chassis(cmodule)
    assert output == chassis_str

    output = get_chassis(sc)
    assert output == chassis_str

    output = get_chassis(rmodule)
    assert output == chassis_str

    output = get_chassis(cc)
    assert output == chassis_str

    output = get_chassis(chassis_str)
    assert output == chassis_str

    output = get_chassis(cabinet_str)
    assert output == ""

#####
# Following tests fail because there is no click context. Figure out how to
# get a click context and re-enable them.
#####
# def test_component_valid(rest_mock):
#     """ Test to make sure we have a valid xname """
#     xname = 'x1000c0'
#     output = component_valid(xname)
#     assert output

# def test_add_parents():
#     """ Test generating parent xnames """
#
#     output = add_parents([n])
#     assert output == [n, cmodule, chassis_str]
#
#     output = add_parents([cmodule])
#     assert output == [cmodule, chassis_str]
#
#     output = add_parents([chassis_str])
#     assert output == [chassis_str]

power_url_base = '/power-control/v1'

##############################################################################
# CRAY POWER TRANSITION
##############################################################################

def test_transition_missing_xname(cli_runner, rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list>` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, _ = cli_runner
        result = runner.invoke(cli, ['power', 'transition', op])
        print(result.output)
        assert result.exit_code == 2
        outputs = [
            "Error: Missing option '--xnames'.",
        ]

    for out in outputs:
        assert out in result.output

def test_transition_single(cli_runner, rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list>` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c0'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        assert data['body']['location'] == [{'xname':'x1000c0'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_hostlist(cli_runner, rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list>` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c[0-1,5]'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        assert data['body']['location'] == [{'xname':'x1000c0'},
                                            {'xname':'x1000c1'},
                                            {'xname':'x1000c5'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_multi(cli_runner, rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list> ...` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c0', '--xnames', 'x1000c1'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        assert data['body']['location'] == [{'xname':'x1000c0'},
                                            {'xname':'x1000c1'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_hostlist_multi(cli_runner, rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list> ...` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c[0-1]',
                                    '--xnames','x1000c[5,6]'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        assert data['body']['location'] == [{'xname':'x1000c0'},
                                            {'xname':'x1000c1'},
                                            {'xname':'x1000c5'},
                                            {'xname':'x1000c6'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_parents_node(cli_runner, rest_mock, pcs_rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list> --include parents` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c0s0b0n0',
                                    '--include','parents'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        xarr = data['body']['location']
        assert xarr == [{'xname':'x1000c0'},{'xname':'x1000c0s0'},
                        {'xname':'x1000c0s0b0n0'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_parents_node_none(cli_runner, rest_mock, pcs_rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list> --include parents` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x2000c0s0b0n0',
                                    '--include','parents'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        xarr = data['body']['location']
        assert xarr == [{'xname':'x2000c0s0b0n0'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_parents_slot(cli_runner, rest_mock, pcs_rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list> --include parents` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c0s0',
                                    '--include','parents'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        xarr = data['body']['location']
        assert xarr == [{'xname':'x1000c0'},{'xname':'x1000c0s0'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_parents_chassis(cli_runner, rest_mock, pcs_rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list> --include parents` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c0',
                                    '--include','parents'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        xarr = data['body']['location']
        assert xarr == [{'xname':'x1000c0'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_children_slot(cli_runner, rest_mock, pcs_rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list> --include children` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c0s0',
                                    '--include','children'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        print(data)
        xarr = data['body']['location']
        assert xarr == [{'xname':'x1000c0s0'}, {'xname':'x1000c0s0b0n0'},
                        {'xname':'x1000c0s0b0n1'}, {'xname':'x1000c0s0b1n0'},
                        {'xname':'x1000c0s0b1n1'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_children_chassis(cli_runner, rest_mock, pcs_rest_mock):
    """ Test `cray power transition <operation> --xnames <xname list> --include children` """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c0',
                                    '--include','children'])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        xarr = data['body']['location']
        assert xarr == [{'xname':'x1000c0'}, {'xname':'x1000c0r0'},
                        {'xname':'x1000c0r1'}, {'xname':'x1000c0r2'},
                        {'xname':'x1000c0r3'}, {'xname':'x1000c0r4'},
                        {'xname':'x1000c0r5'}, {'xname':'x1000c0r6'},
                        {'xname':'x1000c0r7'}, {'xname':'x1000c0s0'},
                        {'xname':'x1000c0s0b0n0'}, {'xname':'x1000c0s0b0n1'},
                        {'xname':'x1000c0s0b1n0'}, {'xname':'x1000c0s0b1n1'},
                        {'xname':'x1000c0s1'}, {'xname':'x1000c0s1b0n0'},
                        {'xname':'x1000c0s1b0n1'}, {'xname':'x1000c0s1b1n0'},
                        {'xname':'x1000c0s1b1n1'}, {'xname':'x1000c0s2'},
                        {'xname':'x1000c0s2b0n0'}, {'xname':'x1000c0s2b0n1'},
                        {'xname':'x1000c0s2b1n0'}, {'xname':'x1000c0s2b1n1'},
                        {'xname':'x1000c0s3'}, {'xname':'x1000c0s3b0n0'},
                        {'xname':'x1000c0s3b0n1'}, {'xname':'x1000c0s3b1n0'},
                        {'xname':'x1000c0s3b1n1'}, {'xname':'x1000c0s4'},
                        {'xname':'x1000c0s4b0n0'}, {'xname':'x1000c0s4b0n1'},
                        {'xname':'x1000c0s4b1n0'}, {'xname':'x1000c0s4b1n1'},
                        {'xname':'x1000c0s5'}, {'xname':'x1000c0s5b0n0'},
                        {'xname':'x1000c0s5b0n1'}, {'xname':'x1000c0s5b1n0'},
                        {'xname':'x1000c0s5b1n1'}, {'xname':'x1000c0s6'},
                        {'xname':'x1000c0s6b0n0'}, {'xname':'x1000c0s6b0n1'},
                        {'xname':'x1000c0s6b1n0'}, {'xname':'x1000c0s6b1n1'},
                        {'xname':'x1000c0s7'}, {'xname':'x1000c0s7b0n0'},
                        {'xname':'x1000c0s7b0n1'}, {'xname':'x1000c0s7b1n0'},
                        {'xname':'x1000c0s7b1n1'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_both_slot(cli_runner, rest_mock, pcs_rest_mock):
    """
    Test `cray power transition <operation> --xnames <xname list> \
        --include parents --include children`
    """
    operations = ['on', 'off', 'soft-off', 'soft-restart', 'hard-restart', 'reinit', 'force-off']
    for op in operations:
        runner, cli, opts = cli_runner
        url_template = power_url_base + '/transitions'
        config = opts['default']
        hostname = config['hostname']
        result = runner.invoke(cli, ['power', 'transition', op,
                                    '--xnames', 'x1000c0s0',
                                    '--include', 'parents',
                                    '--include','children'
                                    ])
        print(result.output)
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['method'].lower() == 'post'
        uri = data['url'].split(hostname)[-1]
        assert url_template in uri
        xarr = data['body']['location']
        assert xarr == [{'xname':'x1000c0'},
                        {'xname':'x1000c0s0'},
                        {'xname':'x1000c0s0b0n0'},
                        {'xname':'x1000c0s0b0n1'},
                        {'xname':'x1000c0s0b1n0'},
                        {'xname':'x1000c0s0b1n1'}]
        if op == 'reinit':
            assert data['body']['operation'] == 'init'
        else:
            assert data['body']['operation'] == op

def test_transition_list(cli_runner, rest_mock):
    """ Test `cray power transition list` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/transitions'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'transition', 'list' ])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri

def test_transition_describe_missing_id(cli_runner, rest_mock):
    """ Test `cray power transition describe` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['power', 'transition', 'describe'])
    print(result.output)
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument 'TRANSITIONID'.",
        ]

    for out in outputs:
        assert out in result.output

def test_transition_describe(cli_runner, rest_mock):
    """ Test `cray power transition describe <transitionID>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/transitions'
    config = opts['default']
    hostname = config['hostname']
    transitionID = '3fa85f64-5717-4562-b3fc-2c963f66afa6'
    result = runner.invoke(cli, ['power', 'transition', 'describe', transitionID])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template+'/'+transitionID in uri

def test_transition_delete_missing_id(cli_runner, rest_mock):
    """ Test `cray power transition delete` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['power', 'transition', 'delete'])
    print(result.output)
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument 'TRANSITIONID'.",
        ]

    for out in outputs:
        assert out in result.output

def test_transition_delete(cli_runner, rest_mock):
    """ Test `cray power transition delete <transitionID>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/transitions'
    config = opts['default']
    hostname = config['hostname']
    transitionID = '3fa85f64-5717-4562-b3fc-2c963f66afa6'
    result = runner.invoke(cli, ['power', 'transition', 'delete', transitionID])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'delete'
    uri = data['url'].split(hostname)[-1]
    assert url_template+'/'+transitionID in uri

def test_status_list_no_xname(cli_runner, rest_mock):
    """ Test `cray power status list` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-status'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'status', 'list'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri

def test_status_list_single(cli_runner, rest_mock):
    """ Test `cray power status list --xnames <xname>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-status'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'status', 'list',
                                '--xnames', 'x1000c0'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    params = uri.split('?')[-1]
    assert params == 'xname=x1000c0'

def test_status_list_single_powerfilter(cli_runner, rest_mock):
    """ Test `cray power status list --xnames <xname> --powerfilter <opt>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-status'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'status', 'list',
                                '--xnames', 'x1000c0',
                                '--powerfilter', 'on'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    params = uri.split('?')[-1]
    assert params == 'powerStateFilter=on&xname=x1000c0'

def test_status_list_single_mgmtfilter(cli_runner, rest_mock):
    """ Test `cray power status list --xnames <xname> --mgmtfilter <opt>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-status'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'status', 'list',
                                '--xnames', 'x1000c0b0',
                                '--mgmtfilter', 'available'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    params = uri.split('?')[-1]
    assert params == 'managementStateFilter=available&xname=x1000c0b0'

def test_status_list_single_bothfilter(cli_runner, rest_mock):
    """ Test `cray power status list --xnames <xname> --mgmtfilter <opt> --powerfilter <opt>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-status'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'status', 'list',
                                '--xnames', 'x1000c0b0',
                                '--mgmtfilter', 'available',
                                '--powerfilter', 'off'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    params = uri.split('?')[-1]
    assert params == 'powerStateFilter=off&managementStateFilter=available&xname=x1000c0b0'

def test_status_list_multi(cli_runner, rest_mock):
    """ Test `cray power status list --xnames <xname> --xnames <xname>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-status'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'status', 'list',
                                '--xnames', 'x1000c0', '--xnames', 'x1000c1'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    params = uri.split('?')[-1]
    assert params == 'xname=x1000c0&xname=x1000c1'

def test_status_list_hostlist(cli_runner, rest_mock):
    """ Test `cray power status list --xnames <hostlist>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-status'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'status', 'list',
                                '--xnames', 'x1000c[0-2]'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    params = uri.split('?')[-1]
    assert params == 'xname=x1000c0&xname=x1000c1&xname=x1000c2'

def test_status_list_hostlist_multi(cli_runner, rest_mock):
    """ Test `cray power status list --xnames <hostlist> --xnames <hostlist>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-status'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'status', 'list',
                                '--xnames', 'x1000c[0-1]',
                                '--xnames', 'x1000c[6,7]'])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    params = uri.split('?')[-1]
    assert params == 'xname=x1000c0&xname=x1000c1&xname=x1000c6&xname=x1000c7'

def test_status_describe_missing_xname(cli_runner, rest_mock):
    """ Test `cray power status describe` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['power', 'status', 'describe'])
    print(result.output)
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument 'XNAME'."
    ]

    for out in outputs:
        assert out in result.output

def test_status_describe_good(cli_runner, rest_mock):
    """ Test `cray power status describe XNAME` """
    xname="x1000c0s0b0n0"

    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-status'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'status', 'describe', xname])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    params = uri.split('?')[-1]
    assert params == 'xname=x1000c0s0b0n0'

def test_cap_snapshot_single(cli_runner, rest_mock):
    """ Test `cray power cap snapshot --xnames <xname list>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-cap/snapshot'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'cap', 'snapshot',
                                '--xnames', 'x1000c0s0b0n0'
                                ])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    xarr = data['body']['xnames']
    assert xarr == ['x1000c0s0b0n0']

def test_cap_snapshot_multi(cli_runner, rest_mock):
    """ Test `cray power cap snapshot --xnames <xname list>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-cap/snapshot'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'cap', 'snapshot',
                                '--xnames', 'x1000c0s0b[0-1]n[0-1]'
                                ])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'post'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    xarr = data['body']['xnames']
    assert xarr == ['x1000c0s0b0n0',
                    'x1000c0s0b0n1',
                    'x1000c0s0b1n0',
                    'x1000c0s0b1n1']

def test_cap_set_single_single(cli_runner, rest_mock):
    """ Test `cray power cap set --xnames <xname> --control <name> <val>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'cap', 'set', '--xnames',
                                'x1000c0s0b0n0', '--control',
                                'Node Power Control', 2500])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'patch'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    print(data['body'])
    assert data['body'] == {
        'components': [
                {
                    'xname': 'x1000c0s0b0n0',
                    'controls': [
                        {
                            'name': 'Node Power Control',
                                    'value': 2500
                        }
                    ]
                }
        ]
        }

def test_cap_set_multi_single(cli_runner, rest_mock):
    """ Test `cray power cap set --xnames <xname> --control <name> <val>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'cap', 'set', '--xnames',
                                'x1000c0s0b0n[0-1]', '--control',
                                'Node Power Control', 2500])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'patch'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    print(data['body'])
    assert data['body'] == {
        'components': [
                {
                    'xname': 'x1000c0s0b0n0',
                    'controls': [
                        {
                            'name': 'Node Power Control',
                                    'value': 2500
                        }
                    ]
                },
                {
                    'xname': 'x1000c0s0b0n1',
                    'controls': [
                        {
                            'name': 'Node Power Control',
                                    'value': 2500
                        }
                    ]
                }
        ]
        }

def test_cap_set_single_multi(cli_runner, rest_mock):
    """ Test `cray power cap set --xnames <xname> --control <name> <val> --control <name> <val>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'cap', 'set', '--xnames',
                                'x1000c0s0b0n0',
                                '--control', 'Node Power Control', 500,
                                '--control', 'GPU0 Power Control', 650,
                                '--control', 'GPU1 Power Control', 650,
                                '--control', 'GPU2 Power Control', 650,
                                '--control', 'GPU3 Power Control', 650])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'patch'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    print(data['body'])
    assert data['body'] == {
        'components': [
                {
                    'xname': 'x1000c0s0b0n0',
                    'controls': [
                        {
                            'name': 'Node Power Control',
                                    'value': 500
                        },
                        {
                            'name': 'GPU0 Power Control',
                                    'value': 650
                        },
                        {
                            'name': 'GPU1 Power Control',
                                    'value': 650
                        },
                        {
                            'name': 'GPU2 Power Control',
                                    'value': 650
                        },
                        {
                            'name': 'GPU3 Power Control',
                                    'value': 650
                        }
                    ]
                }
            ]
        }

def test_cap_set_multi_multi(cli_runner, rest_mock):
    """ Test `cray power cap set --xnames <xname> --control <name> <val> --control <name> <val>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'cap', 'set',
                                '--xnames', 'x1000c0s0b0n[0-1]',
                                '--control', 'Node Power Control', 500,
                                '--control', 'GPU0 Power Control', 650,
                                '--control', 'GPU1 Power Control', 650,
                                '--control', 'GPU2 Power Control', 650,
                                '--control', 'GPU3 Power Control', 650])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'patch'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri
    print(data['body'])
    assert data['body'] == {
        'components': [
                {
                    'xname': 'x1000c0s0b0n0',
                    'controls': [
                        {
                            'name': 'Node Power Control',
                                    'value': 500
                        },
                        {
                            'name': 'GPU0 Power Control',
                                    'value': 650
                        },
                        {
                            'name': 'GPU1 Power Control',
                                    'value': 650
                        },
                        {
                            'name': 'GPU2 Power Control',
                                    'value': 650
                        },
                        {
                            'name': 'GPU3 Power Control',
                                    'value': 650
                        }
                    ]
                },
                {
                    'xname': 'x1000c0s0b0n1',
                    'controls': [
                        {
                            'name': 'Node Power Control',
                                    'value': 500
                        },
                        {
                            'name': 'GPU0 Power Control',
                                    'value': 650
                        },
                        {
                            'name': 'GPU1 Power Control',
                                    'value': 650
                        },
                        {
                            'name': 'GPU2 Power Control',
                                    'value': 650
                        },
                        {
                            'name': 'GPU3 Power Control',
                                    'value': 650
                        }
                    ]
                }
            ]
        }

def test_cap_list(cli_runner, rest_mock):
    """ Test `cray power cap list` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-cap'
    config = opts['default']
    hostname = config['hostname']
    result = runner.invoke(cli, ['power', 'cap', 'list' ])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template in uri

def test_cap_describe_missing_id(cli_runner, rest_mock):
    """ Test `cray power cap describe` """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['power', 'cap', 'describe'])
    print(result.output)
    assert result.exit_code == 2
    outputs = [
        "Error: Missing argument 'POWERCAPID'.",
        ]

    for out in outputs:
        assert out in result.output

def test_cap_describe(cli_runner, rest_mock):
    """ Test `cray power cap describe <powerCapID>` """
    runner, cli, opts = cli_runner
    url_template = power_url_base + '/power-cap'
    config = opts['default']
    hostname = config['hostname']
    powerCapID = '3fa85f64-5717-4562-b3fc-2c963f66afa6'
    result = runner.invoke(cli, ['power', 'cap', 'describe', powerCapID])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    assert url_template+'/'+powerCapID in uri
