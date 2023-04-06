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
""" Nested Dict class. """


class NestedDict(dict):
    """dict object that allows for period separated gets:
    a_config.get('some.key', default) ==
        a_config.get('some', {}).get('key', default)
    given:
        a_config == {"some": {"key": "some value"}}"""

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return f'{type(self).__name__}({dictrepr})'

    def set_deep(self, key, value):
        """ Deep set a value. \n
        Ex: `d.set_deep('a.b.c', 'foo')` is the same as: \n
        `d.setdefault('a', {}).setdefault('b', {})['c'] = 'foo'`
        """
        setter = self
        keys = key.split('.')
        last = keys.pop()
        for k in keys:
            setter = setter.setdefault(k, {})
        setter[last] = value

    def get(self, key, default=None):
        """ Deep get a value. \n
        E: `d.get('a.b.c', 'bar')` is the same as: \n
        `d.get('a', {}).get('b', {}).get('c', 'bar')`
        """
        keys = key.split('.')
        found = dict(self.items())
        for k in keys:
            if not isinstance(found, dict):
                return default
            found = found.get(k)
            if found is None:
                return default
        return found
