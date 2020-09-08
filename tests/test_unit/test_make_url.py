""" Test the main CLI command (`cray`) and options."""
# pylint: disable=redefined-outer-name, invalid-name
# pylint: disable=too-many-arguments, unused-variable, import-error
# pylint: disable=protected-access

from cray import rest


def test_make_url_ip():
    """ Make url with ip """
    base = '127.0.0.1'
    route = '/test'
    scheme = 'http'
    data = rest.make_url(route, base, default_scheme=scheme)
    assert data == '{}://{}{}'.format(scheme, base, route)


def test_make_url_no_www():
    """ Make url with no TLD """
    base = 'test.com'
    route = '/test'
    scheme = 'https'
    data = rest.make_url(route, base)
    assert data == '{}://{}{}'.format(scheme, base, route)


def test_make_url_no_scheme():
    """ Make url with no scheme """
    base = 'test.com'
    route = '/test'
    scheme = 'https'
    data = rest.make_url(route, base + '/123')
    assert data == '{}://{}{}'.format(scheme, base, route)
