#
#  MIT License
#
#  (C) Copyright 2020-2023 Hewlett Packard Enterprise Development LP
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
#
""" Test the main CLI command (`cray`) and options. """
# pylint: disable=invalid-name
# pylint: disable=protected-access
import json
import requests

from cray import errors


def test_unauthorized_normal():
    """ Test `cray init` for creating the default configuration """
    err = errors.UnauthorizedError()
    print(err)
    assertions = [
        '`cray auth login`',
        'Your session has expired, please run:'
    ]
    for assertion in assertions:
        assert assertion in err.message


def test_insecure_error():
    """ Test `cray init` for creating the default configuration """

    err = errors.InsecureError()
    assertions = [
        "You've configured your cray hostname with http. " +
        "Please reconfigure for https."
    ]
    for assertion in assertions:
        assert assertion in err.message


def test_bad_response_error_default():
    """ Test generic bad response error """

    resp = requests.get('https://httpbin.org/status/400', timeout=5)
    err = errors.BadResponseError(resp)
    print(err)
    assertions = [
        "Error received from server: 400 BAD REQUEST"
    ]
    for assertion in assertions:
        assert assertion in err.message


def test_bad_response_error():
    """ Test RFC 7807 formatted bad response error """

    title = "FOO"
    detail = "BAR"
    data = {"title": title, "detail": detail}
    resp = requests.post('https://httpbin.org/anything', data={}, timeout=5)
    resp._content = json.dumps(data).encode('utf-8')
    _ = resp.json()
    err = errors.BadResponseError(resp)
    assertions = [
        f"{title}: {detail}"
    ]
    for assertion in assertions:
        assert assertion in err.message


def test_bad_response_capmc_error():
    """ Test CAPMC formatted bad response error """

    e = 400
    err_msg = "CAPMC fake error"
    data = {"e": e, "err_msg": err_msg}
    resp = requests.post('https://httpbin.org/status/400', data={}, timeout=5)
    resp._content = json.dumps(data).encode('utf-8')
    _ = resp.json()
    err = errors.BadResponseError(resp)
    print(err)
    assertions = [
        f"{'400 BAD REQUEST'}: {err_msg}"
    ]
    for assertion in assertions:
        assert assertion in err.message
