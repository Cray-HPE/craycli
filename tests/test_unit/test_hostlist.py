""" Test the main CLI command hostlist expansion .

MIT License

(C) Copyright [2020] Hewlett Packard Enterprise Development LP

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

from cray import hostlist


def test_expand_integer_noexpand():
    """ Test expanding a simple nid list """
    expected = '1,2,3,4,7,8,9'
    output = hostlist.expand('1,2,3,4,7,8,9')
    assert expected in output


def test_expand_integer_simple():
    """ Test expanding a simple ranged nidlist """
    expected = '1,2,3,4,5,6,7,8,9,10'
    output = hostlist.expand('[1-10]')
    assert expected in output


def test_expand_integer_complex():
    """ Test expanding a complex ranged nidlist """
    expected = '7,3,4,5,1,9,10'
    output = hostlist.expand('7,[3-5],1,[9,10]')
    assert expected in output


def test_expand_xname_noexpand():
    """ Test expanding a simple xname string """
    expected = 'x0c0s0b0n0'
    output = hostlist.expand('x0c0s0b0n0')
    assert expected in output


def test_expand_xname_simple():
    """ Test expanding a simple ranged xname list """
    expected = 'x0c0,x0c1,x1c0,x1c1'
    output = hostlist.expand('x[0-1]c[0-1]')
    assert expected in output


def test_expand_xname_complex():
    """ Test expanding a complex ranged xname list """
    expected = 'x0c1,x0c3,x0c5,x0c7,x1c0,x1c1,x2c0,x2c1'
    output = hostlist.expand('x0c[1,3,5,7],x[1-2]c[0-1]')
    assert expected in output
