""" Test the main CLI command hostlist expansion ."""

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
