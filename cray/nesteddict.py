""" Nested Dict class """


class NestedDict(dict):
    """dict object that allows for period separated gets:
    a_config.get('some.key', default) ==
        a_config.get('some', {}).get('key', default)
    given:
        a_config == {"some": {"key": "some value"}}"""

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)

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
        found = {}
        for k in self.keys():
            found[k] = self[k]
        for k in keys:
            if not isinstance(found, dict):
                return default
            found = found.get(k)
            if found is None:
                return default
        return found
