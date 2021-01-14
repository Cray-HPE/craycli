""" REST Utils for testing """
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument, import-error
# pylint: disable=wrong-import-order
import json

import requests_mock as req_mock
import pytest


def _request_cb(request, context):
    resp = {
        'method': request.method,
        'url': request.url,
    }
    if request.body is not None:
        try:
            resp['body'] = json.loads(request.body)
        except Exception:  # pylint: disable=broad-except
            resp['body'] = request.body
    return json.dumps(resp)


@pytest.fixture()
def rest_mock(requests_mock):
    """ Catch any rest callouts and return the request info instead """
    # pylint: disable=protected-access
    requests_mock._adapter.register_uri(req_mock.ANY, req_mock.ANY,
                                        text=_request_cb)
