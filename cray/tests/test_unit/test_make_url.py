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
from cray import rest


def test_make_url_ip():
    """ Make URL with IP address """
    base = '127.0.0.1'
    route = '/test'
    scheme = 'http'
    data = rest.make_url(route, base, default_scheme=scheme)
    assert data == f'{scheme}://{base}{route}'


def test_make_url_no_www():
    """ Make url with no TLD """
    base = 'test.com'
    route = '/test'
    scheme = 'https'
    data = rest.make_url(route, base)
    assert data == f'{scheme}://{base}{route}'


def test_make_url_no_scheme():
    """ Make url with no scheme """
    base = 'test.com'
    route = '/test'
    scheme = 'https'
    data = rest.make_url(route, base + '/123')
    assert data == f'{scheme}://{base}{route}'
