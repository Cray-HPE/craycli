#  MIT License
#
#  (C) Copyright 2023 Hewlett Packard Enterprise Development LP
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.
""" Mocks for craycli modules. """
# pylint: disable=protected-access
import pytest
import requests_mock as req_mock


##############################################################################
# MOCKS
##############################################################################

def _x1000c0s0_request_cb(*_) -> str:
    """ Mock mountain cab. slot."""
    return '''{ "Components": [ { "ID": "x1000c0s0b1n0" },
        { "ID": "x1000c0s0b0n1" }, { "ID": "x1000c0s0b1n1" },
        { "ID": "x1000c0s0" }, { "ID": "x1000c0s0b0n0" } ] }'''


def _x1000c0_request_cb(*_) -> str:
    """ Mock mountain cab."""
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
def pcs_rest_mock(requests_mock) -> str:
    """ Catch any rest callouts and return the request info instead """

    requests_mock._adapter.register_uri(
        req_mock.GET,
        '/apis/smd/hsm/v2/State/Components/Query/x1000c0s0?type=computemodule'
        '&type=routermodule&type=node',
        text=_x1000c0s0_request_cb
    )
    requests_mock._adapter.register_uri(
        req_mock.GET,
        '/apis/smd/hsm/v2/State/Components/Query/x1000c0?type=chassis'
        '&type=computemodule&type=routermodule&type=node',
        text=_x1000c0_request_cb
    )
    requests_mock._adapter.register_uri(
        req_mock.GET,
        '/apis/smd/hsm/v2/State/Components',
        text=_x1000c0_request_cb
    )
