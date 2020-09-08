""" Test the main CLI command (`cray`) and options."""
# pylint: disable=redefined-outer-name, unused-import, invalid-name
# pylint: disable=too-many-arguments, unused-variable, import-error
# pylint: disable=protected-access
import os
import json

import click
import toml
import requests
import pytest

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

    resp = requests.get('https://httpbin.org/status/400')
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
    resp = requests.post('https://httpbin.org/anything', data={})
    resp._content = json.dumps(data).encode('utf-8')
    x = resp.json()
    err = errors.BadResponseError(resp)
    assertions = [
        "{}: {}".format(title, detail)
        ]
    for assertion in assertions:
        assert assertion in err.message


def test_bad_response_capmc_error():
    """ Test CAPMC formatted bad response error """

    e = 400
    err_msg = "CAPMC fake error"
    data = {"e": e, "err_msg": err_msg}
    resp = requests.post('https://httpbin.org/status/400', data={})
    resp._content = json.dumps(data).encode('utf-8')
    x = resp.json()
    err = errors.BadResponseError(resp)
    print(err)
    assertions = [
        "{}: {}".format("400 BAD REQUEST", err_msg)
        ]
    for assertion in assertions:
        assert assertion in err.message
