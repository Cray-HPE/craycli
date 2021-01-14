"""
Parses OpenAPI spec files and other related classes
Copyright 2020 Hewlett Packard Enterprise Development LP
"""
import json
from copy import copy

from cray.nesteddict import NestedDict
from cray.constants import IGNORE_TAG, CONVERSTION_FLAG


class Schema(object):
    """ OpenAPI Schema Parser """

    _NESTED_ARRAY = 'nested_array'
    _NESTED_OBJECT = 'nested_object'
    _NESTINGS = [_NESTED_ARRAY, _NESTED_OBJECT]

    def __init__(self, schema, prefix=None, required=None, **kwargs):
        self.schema = schema
        self.prefix = prefix
        schema_req = self.schema.get('required')
        # Remove any children required if the parent is not required
        if required is False and schema_req is not None:
            del self.schema['required']
        self.required = required or schema_req
        self.parsed = self.parse(**kwargs)

    def _make_name(self, name=None, default=None):
        keys = []
        if name is None and self.prefix is None and default is None:
            raise ValueError("Either name or prefix is required")
        if self.prefix is not None:
            keys = keys + self.prefix.split('-')
        if name is not None:
            keys = keys + name.split('-')
        if not keys and default is not None:
            keys.append(default)
        return '-'.join([k for k in keys if k != ''])

    @classmethod
    def _set_nesting(cls, param, default=None):
        nested = len(param['name'].split('-')) > 1
        if param.get('nesting') in cls._NESTINGS:
            # Nothing to change.
            return None
        if not nested:
            return False
        default = default or cls._NESTED_OBJECT
        param['nesting'] = default
        return True

    def get_parser(self):
        """ Get the parsed data """
        return self.parsed

    def parse(self, **kwargs):
        """ Parse schema """
        raise NotImplementedError


class SchemaObject(Schema):
    """ OpenAPI Object Schema Parser """

    def parse(self, **kwargs):
        params = []
        required = [i.lower() for i in self.schema.get('required', [])]
        for name, param in self.schema.get('properties', {}).items():
            fullname = self._make_name(name=name)
            param_type = _find_type(param, 'type', 'object')
            required_param = (name.lower() in required)

            kwargs.update({
                'prefix': fullname,
                'required': required_param
            })


            parsed = parse_schema_type(param_type, param, **kwargs).parsed
            parsed_params = parsed['params']
            for parsed_param in parsed_params:
                parsed_param.update(parsed['options'])
                self._set_nesting(parsed_param)
            params = params + parsed_params
        return {'params': params, 'options': {}}


class SchemaArray(Schema):
    """ OpenAPI Array Schema Parser """

    def _get_opts(self):
        """ Get array options to pass back in kwargs """
        opts = self.schema.copy()
        to_remove = ('items', 'type')
        for key in to_remove:
            opts.pop(key, None)
        return opts

    def parse(self, **kwargs):
        params = []
        kwargs.update(self._get_opts())
        items = self.schema['items']
        item_type = _find_type(items, 'type', 'object')
        item_name = self._make_name(name=self.schema.get('name'), default='')
        kwargs.update({
            'prefix': item_name,
            'required': self.required or kwargs.get('required', False)
        })
        parsed = parse_schema_type(item_type, items, **kwargs).parsed
        params = parsed['params']
        for param in params:
            self._set_nesting(param, default=self._NESTED_ARRAY)
        options = parsed['options']
        options.update({
            'nesting': self._NESTED_ARRAY,
            'array_item_type': item_type
        })
        return {'params': params, 'options': options}


class SchemaString(Schema):
    """ OpenAPI String/Catchall Schema Parser """

    @staticmethod
    def _get_type(param):
        ptype = param.get('type')
        pformat = param.get('format')
        pname = param.get('name')
        if param.get('enum'):
            return 'choice'
        if pformat == 'binary':
            return 'filepath'
        if 'password' in pname:
            return 'password'
        return ptype

    @classmethod
    def _format_body_param(cls, name, param):
        param['required'] = param.get('required', False)
        remove = ['xml', 'properties']
        to_remove = [r for r in param.keys() if r in remove]
        for remove in to_remove:
            del param[remove]
        param.update({
            'name': name,
        })
        param['type'] = cls._get_type(param)
        return param

    def parse(self, **kwargs):
        name = self.schema.get('name')
        kwargs['required'] = self.required or kwargs.get('required', False)
        name_opts = {}
        # required = self.required or kwargs.get('required', False)
        if self.schema.get('format') == 'binary':
            if name is None:
                name_opts['default'] = 'file'
            kwargs['required'] = True
        self.schema.update(**kwargs)
        fullname = self._make_name(name=name, **name_opts)
        params = [self._format_body_param(fullname, self.schema)]
        return {'params': params, 'options': {}}


def parse_schema_type(stype, schema, **kwargs):
    """ Return the proper schema class based on schema type """
    schemas = {
        'object': SchemaObject,
        'array': SchemaArray,
        'string': SchemaString,
        'allOf': handle_complex,
        'oneOf': handle_complex,
        'anyOf': handle_complex
    }

    return schemas.get(stype, SchemaString)(schema, **kwargs)


def _find_type(param, default_type, default_value=None):
    if 'allOf' in param:
        param_type = 'allOf'
    elif 'oneOf' in param:
        param_type = 'oneOf'
    elif 'anyOf' in param:
        param_type = 'anyOf'
    else:
        param_type = param.get(default_type, default_value)

    return param_type


def handle_complex(schema, **kwargs):
    """ Return the nested *Of: schemas """
    out = _merge_complex(schema)
    return parse_schema_type(out['type'], out, **kwargs)


def _merge_complex(schema):
    schemas = []
    for k in schema.keys():
        if isinstance(schema[k], dict):
            schemas.extend(schema[k])
    out = {
        "type": "object",
        "required": [],
        "properties": {}
    }
    for schema_entry in schemas:
        if bool(set(schema_entry.keys()) & set(['allOf', 'anyOf', 'oneOf'])):
            schema_entry = _merge_complex(schema_entry)
        out['properties'].update(schema_entry['properties'])
    return out


class Swagger(object):
    """ Parses a swagger file and schemas as generates a dict consumbale by the
    Cray CLI
    """

    _MIME_JSON = 'application/json'
    _MIME_FORM = 'application/x-www-form-urlencoded'
    _MIME_OCTET = 'application/octet-stream'
    _MIME_MULTIPART = 'multipart/form-data'
    _MIME_CATCHALL = '*/*'
    # _SUPPORTED_MIMES should be preferred order or choice.
    # Make sure _CATCHALL is always last in the list.
    _SUPPORTED_MIMES = [_MIME_JSON, _MIME_FORM, _MIME_MULTIPART, _MIME_OCTET]
    _SUPPORTED_MIMES.append(_MIME_CATCHALL)

    _VOCABULARY = {
        'getall': 'list',
        'get': 'describe',
        'post': 'create',
        'put': 'update',
        'patch': 'update',
        'delete': 'delete',
        'deleteall': 'delete'
    }

    def __init__(self, data, ignore_endpoints=None, **kwargs):
        ignore_endpoints = ignore_endpoints or []
        # Make sure to copy the class vocab to prevent changes affecting
        # other class instances.
        vocab = copy(self._VOCABULARY)
        vocab.update(kwargs.get('vocabulary', {}))

        self.data = data
        self.ignore_endpoints = ignore_endpoints or []
        self.vocab = dict((k.lower(), v.lower())
                          for k, v in vocab.items())
        self.ignore = ignore_endpoints
        self.parsed = NestedDict()
        self.mime = None
        self.parse()

    def _parse_body(self, body):
        data = NestedDict(**body['content'])

        mime = self._get_prefered_mime(data.keys())
        self.mime = mime
        schema = data[mime]['schema']
        # Assume top level schemas are object type if not provided.
        schema_type = _find_type(schema, 'type', 'object')
        results = parse_schema_type(schema_type, schema).parsed
        optional = results['options']
        if optional.get('nesting') is not None:
            del optional['nesting']
        params = results['params']
        optional.update({'params': params, 'payload_type': schema_type})
        return optional

    @classmethod
    def _get_prefered_mime(cls, mimes):
        supported = [m for m in mimes if m in cls._SUPPORTED_MIMES]
        msg = 'Provided mime(s) not supported: {}'.format(mimes)
        if not supported:
            raise NotImplementedError(msg)
        found = supported[0]
        for mime in cls._SUPPORTED_MIMES:
            if mime in supported:
                found = mime
                break
        return found

    @staticmethod
    def _parse_route(route):
        end_in_arg = False
        keys = [i for i in route.split('/') if i != '']
        commands = []
        args = []
        for k in keys:
            # Ignore parameters since we'll get those later in the spec.
            if (lambda c: (c and c.find('{') == -1 and c.find('}') == -1))(k):
                commands.append(k)
            else:
                args.append(k)
        if args and keys and keys[-1] == args[-1]:
            end_in_arg = True

        return (commands, args, end_in_arg)

    @staticmethod
    def _format_param(param):
        schema = param
        schema.update(**param['schema'])
        del param['schema']
        parsed = parse_schema_type(schema['type'], schema).parsed
        return parsed['params']

    @classmethod
    def _parse_params(cls, params):
        resp = {}
        for param in params:
            resp.setdefault(param['in'], [])
            resp[param['in']] = resp[param['in']] + cls._format_param(param)
        return resp

    def _get_command(self, key, route, method):
        existing = self.parsed.get(key)
        if existing is not None:  # pragma: NO COVER
            conflict = existing
            template = '{m}:{r} conflicts with {cm}:{cr}'
            msg = template.format(m=method, r=route,
                                  cm=conflict['method'],
                                  cr=conflict['route'])
            raise ValueError(msg)
        return key

    def _get_key(self, commands, verb):
        return '.'.join(commands + [self.vocab[verb.lower()]])

    def get_parsed(self):
        """ Get parsed data """
        return self.parsed

    @staticmethod
    def _parse_servers(current_servers):
        servers = []
        for server in current_servers:
            url = server.get('url')
            if url:
                if url[-1] == '/':
                    url = url[:-1]
                server['url'] = url
                servers.append(server)
        return servers

    def parse(self):
        """ Parse data and return groups, commands, and parameters """
        # pylint: disable=too-many-locals
        endpoint_key = 'endpoints'
        # Remove any trailing / from servers to prevent urllib errors
        self.data['servers'] = self._parse_servers(self.data['servers'])

        for key in ['info', 'servers']:
            if key in self.data:
                self.parsed[key] = self.data[key]
        self.parsed.setdefault(endpoint_key, NestedDict())
        for route, data in self.data['paths'].items():
            if route not in self.ignore_endpoints:
                commands, _, end_in_arg = self._parse_route(route)
                parameters = self._parse_params(data.get('parameters', []))
                if 'parameters' in data:
                    del data['parameters']
                if 'servers' in data:
                    del data['servers']
                for verb, details in data.items():
                    if IGNORE_TAG in details.get('tags', []):
                        continue
                    method = verb.upper()
                    if verb.lower() == 'get' and not end_in_arg:
                        verb = 'getall'
                    if verb.lower() == 'delete' and not end_in_arg:
                        verb = 'deleteall'
                    keep_keys = ['tags']
                    command_data = {
                        key: value for key, value in details.items()
                        if key in keep_keys}
                    command_data.update({
                        'route': route,
                        'method': method,
                    })
                    command_data.update(parameters)
                    command_data.update(self._parse_params(details.get(
                        'parameters', [])))
                    if details.get('requestBody') is not None:
                        body = self._parse_body(details['requestBody'])
                        body['mime'] = self.mime
                        command_data.update(body)
                    command = self._get_command(self._get_key(commands, verb),
                                                route, method)
                    self.parsed[endpoint_key].set_deep(command, command_data)
        self.parsed[CONVERSTION_FLAG] = True


def parse(path, **kwargs):
    """ Parse a Swagger/OpenAPI file and return an object that can be consumed
    by the Cray CLI Framework """
    # pylint: disable=invalid-name
    with open(path) as filep:
        data = json.load(filep)
    s = Swagger(data, **kwargs)

    return s
