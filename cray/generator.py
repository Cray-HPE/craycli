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
""" Generates CLI commands from parsed Swagger file """
import json
import os
import re
import click
from requests_toolbelt.multipart.encoder import MultipartEncoder
from six import string_types
from six.moves import urllib

from cray import core
from cray import hostlist
from cray import rest
from cray import swagger
from cray.constants import CONVERSION_FLAG
from cray.constants import DANGER_TAG
from cray.constants import FROM_FILE_TAG
from cray.constants import HIDDEN_TAG
from cray.constants import IGNORE_TAG
from cray.constants import TAG_SPLIT
from cray.nesteddict import NestedDict

PATH_ORIGIN = 'path'
QUERY_ORIGIN = 'query'
HEADER_ORIGIN = 'header'
PARAM_ORIGIN = 'params'
FILE_ORIGIN = 'filepath'

# What we'll search for to filter out non-prod servers
PREFERRED_HOST_PREFIX = 'api-gw'
PREFERRED_URL_PREFIX = "/apis"


def api(data, callback, base=''):
    """ Decorator that will send endpoint data into commands """

    def tags_decorator(func):  # pylint: disable=missing-docstring
        def func_wrapper(
                *args,
                data_handler=None,
                **kwargs,
        ):  # pylint: disable=missing-docstring
            kwargs['base'] = base
            args = _parse_data(data, **kwargs)
            if data_handler:
                args = data_handler(args)
            opts = args[-1]
            opts['callback'] = callback
            return func(*args[:-1], **opts)

        return func_wrapper

    return tags_decorator


def _raise_missing_param(parent_name, param_name):
    param = f'--{parent_name}-{param_name}'
    raise click.BadParameter(f'Missing parameter: {_make_name(param)}')


def _make_object_array(values, parent_name):
    # This isn't ideal but it works and isn't ran often.
    generated_array = []
    max_val = sorted([len(v) for v in values.values()], reverse=True)[0]
    for i in range(max_val):
        obj = {}
        for k, v in values.items():
            if len(v) != max_val:
                _raise_missing_param(parent_name, k)
            obj[k] = v[i]
        generated_array.append(obj)
    return generated_array


def _generate_body(body, params):
    resp = NestedDict({})
    nestings = NestedDict({})
    for param in params:
        param_name = param['name']
        item = body.get(param_name)
        if item is not None:
            nesting = param.get('nesting')
            if not nesting:
                resp[param_name] = item
                continue
            key = '.'.join(param_name.split('-'))
            if nesting == 'nested_array':
                if param['array_item_type'] == 'object':
                    nestings.set_deep(f'array_objs.{key}', item)
                else:
                    resp[key.split('.', maxsplit=1)[0]] = item
            else:
                resp.set_deep(key, item)
    if nestings.get('array_objs'):
        for arr, value in nestings['array_objs'].items():
            resp[arr] = _make_object_array(value, arr)
    return dict(resp)


def _get_endpoint(url):
    _, _, path, _, _ = urllib.parse.urlsplit(url)
    return path


def _split_origins(data):
    opts = {}
    opts[FILE_ORIGIN] = {}
    for origin in [PATH_ORIGIN, QUERY_ORIGIN, HEADER_ORIGIN, PARAM_ORIGIN]:
        opts.setdefault(origin, {})
        for i in data.get(origin, []):
            name = i['name']
            if i.get('type') == FILE_ORIGIN:
                opts[FILE_ORIGIN].setdefault(name, None)
            else:
                opts[origin].setdefault(name, None)
    return opts


def _parse_data(data, base=None, **kwargs):
    method = data['method']
    opts = _split_origins(data)
    from_file_data = None
    for i in kwargs.values():
        if i['name'] == FROM_FILE_TAG:
            from_file_data = i['value']
            continue
        for origin, params in opts.items():
            if i['name'] in params:
                # Not sure why lint wants me to "use 'params' instead
                # pylint: disable=unnecessary-dict-index-lookup
                opts[origin][i['name']] = i['value']

    route = data['route'].format(**opts[PATH_ORIGIN])
    if base is not None:
        route = _get_endpoint(base) + route

    body = from_file_data if from_file_data \
        else _generate_body(opts[PARAM_ORIGIN], data.get('params', []))

    if not body and method.lower() in ['get', 'delete']:
        body = None

    # Pack args into kwargs requests expects
    args = {}
    if body:
        args['json'] = body
    if opts[QUERY_ORIGIN]:
        args['params'] = opts[QUERY_ORIGIN]
    if opts[HEADER_ORIGIN]:
        args['headers'] = opts[HEADER_ORIGIN]
    if opts[FILE_ORIGIN]:
        fields = {}
        for k, v in opts[FILE_ORIGIN].items():
            # This explicitly returns an open file object, can't use 'with' here
            # pylint: disable=consider-using-with
            fields[k] = (os.path.basename(v), open(v, 'rb'))
        args['data'] = MultipartEncoder(fields=fields)
        args.setdefault('headers', {})['Content-Type'] = args[
            'data'].content_type
    return (method, route, args)


def _get_type(param_type, opt):
    types = {
        'string': click.STRING,
        'integer': click.INT,
        'int': click.INT,
        'float': click.FLOAT,
        'boolean': click.BOOL,
        'choice': click.Choice,
        'filepath': click.Path(exists=True)
    }
    # Ignoring param_type = 'string' allows for CLI's with nested arrays of
    # enums to be forced to the 'string' type by _generate_option(). Otherwise,
    # options with 'enum' are param_type 'choice' and are unaffected by
    # "param_type != 'string'"
    if 'enum' in opt and param_type != 'string':
        return types['choice'](opt['enum'])

    return types.get(param_type, click.STRING)


def _arg_file_cb(ctx, param, value):
    try:
        with open(value, encoding='utf-8') as payload_fp:
            data = json.load(payload_fp)
    except:  # pylint: disable=broad-except
        # pylint: disable=raise-missing-from
        raise click.UsageError('Payload file not valid JSON')
    return _arg_cb(ctx, param, data)


def _arg_cb(ctx, param, value):  # pylint: disable=unused-argument
    name = param.var_name
    if param.payload_name is not None:
        name = param.payload_name
    return {
        'value': value,
        'name': name,
    }


def _generate_argument(func, arg, from_file=False):
    name = arg['name']
    opts = {
        'name': name,
        'payload_name': name if not from_file else FROM_FILE_TAG,
        'metavar': name.upper(),
        'type': _get_type(arg.get('type'), arg),
    }
    opts['callback'] = _arg_cb if not from_file else _arg_file_cb
    if 'required' in arg:
        opts['required'] = arg['required']
    return core.argument(name, **opts)(func)


def _find_help(param):
    for key in ['help', 'description', 'summary', 'example']:
        resp = param.get(key)
        if resp:
            return str(resp)
    return ''


def _array_validation_callback(click_type, cb):  # pylint: disable=invalid-name

    def callback(ctx, param, value):
        "Nested array param callback"
        if isinstance(value, string_types):
            items = []
            for i in "".join(hostlist.expand(value).split()).split(','):
                items.append(click_type.convert(i, param, ctx))
            return cb(ctx, param, items)
        return cb(ctx, param, value)

    return callback


def _opt_callback(ctx, param, value):  # pylint: disable=unused-argument
    name = param.name
    if param.payload_name is not None:
        name = param.payload_name
    return {
        'value': value,
        'name': name,
    }


def _make_name(name):
    name = '-'.join(
        re.sub(r'([A-Z][a-z]+|[A-Z]+[s]?(?![a-rt-z]))', r' \1', name).split()
    )
    return name.replace('_', '-').lower()


def _generate_option(func, param):
    if param.get('readOnly') is True:
        return func
    callback = _opt_callback
    opts = {
        'type': _get_type(param.get('type'), param),
        'help': _find_help(param),
        'callback': callback
    }
    if param.get('nesting') == "nested_array":
        metavar = opts['type'].name.upper()
        opts['metavar'] = f"{metavar},...|EXPR"
        opts['callback'] = _array_validation_callback(opts['type'], callback)
        # Force type back to string for arrays so we can do comma separation.
        opts['type'] = _get_type('string', param)
        if param.get('type') in 'integer':
            opts['help'] = opts['help'] + \
                           " EXPR is a hostlist of the form [1-10,12]"
        if param.get('type') in 'string':
            opts['help'] = opts['help'] + \
                           " EXPR is a hostlist of the form x[0-1]c[2,4]"
    if param.get('default'):
        opts['default'] = param['default']
    if 'required' in param and param.get('array_item_type') != 'object':
        opts['required'] = param['required']
    opts['payload_name'] = param['name']
    return core.option(f'--{_make_name(param["name"])}', **opts)(func)


def _set_params(func, command, from_file=False):
    if command.get(PATH_ORIGIN):
        for arg in command[PATH_ORIGIN]:
            func = _generate_argument(func, arg)
    if command.get(QUERY_ORIGIN):
        for arg in command[QUERY_ORIGIN]:
            func = _generate_option(func, arg)
    if command.get(HEADER_ORIGIN):
        for arg in command[HEADER_ORIGIN]:
            func = _generate_option(func, arg)
    if command.get(PARAM_ORIGIN):
        if from_file:
            from_file_data = {
                'name': 'payload_file',
                'required': True,
                'type': FILE_ORIGIN,
            }
            func = _generate_argument(func, from_file_data, from_file)
        else:
            for param in command[PARAM_ORIGIN]:
                func = _generate_option(func, param)
    return func


def _base_group(*args, **kwargs):
    """ Stubbed out group to be used when generating new groups """
    # pylint: disable=unused-argument
    pass


def _add_confirmation_opt(func, msg=None):
    msg = msg or "Are you sure?"

    def _cb(ctx, param, value):  # pylint: disable=unused-argument
        if not value:
            click.confirm(msg, abort=True)
        return value

    opts = {
        "expose_value": False,
        "is_flag": True,
        "help": "Respond yes to any confirmations."
    }
    # Note we have to use a '-y' instead of a preferred '--force' as other apis
    # already implement a force field within their JSON.
    return core.option("-y", callback=_cb, **opts)(func)


def create_commands(cli, commands, base=None, callback=None, **kwargs):
    """ Generate CLI commands/groups from a parsed Swagger file """
    # pylint: disable=too-many-locals
    parent_name = cli.name.lower()
    for command, data in commands.items():
        command_name = command[0].lower() + command[1:]
        # filter out possible cli tags
        tags = [i for i in data.get('tags', []) if 'cli_' in i.lower()]
        if IGNORE_TAG in tags:
            continue
        opts = kwargs.copy()
        if 'route' in data:
            if HIDDEN_TAG in tags:
                opts.update({"hidden": True})
            from_file = (FROM_FILE_TAG in tags)
            decorator = api(data, callback, base)(rest.request)
            func = _set_params(
                decorator,
                data,
                from_file
            )
            for tag in tags:
                temp = tag.split(TAG_SPLIT)
                if DANGER_TAG in temp:
                    msg = None
                    if len(temp) > 1:
                        msg = temp[1]
                    func = _add_confirmation_opt(func, msg=msg)
            cli.command(name=command_name, help=data.get('help', ''), **opts)(
                func
            )
        else:
            if command.lower() == parent_name:
                # Hack to prevent duplicate groups, i.e. cray uas uas create
                create_commands(
                    cli,
                    data,
                    base=base,
                    callback=callback,
                    **opts
                )
            else:
                func = cli.group(command_name, help=_find_help(data), **opts)(
                    _base_group
                )
                create_commands(
                    func,
                    data,
                    base=base,
                    callback=callback,
                    **opts
                )
                # If all sub commands/groups are hidden, hide parent.
                _hide_parent = True
                for v in func.commands.values():
                    if not v.hidden:
                        _hide_parent = False
                        break
                func.hidden = _hide_parent
                cli.add_command(func)

                # Create hidden versions of any uppercase commands for backwards compat
                if command != command_name:
                    opts['deprecated'] = True
                    opts['hidden'] = True
                    old_func = cli.group(
                        command,
                        help=_find_help(data),
                        **opts
                    )(_base_group)
                    create_commands(
                        old_func,
                        data,
                        base=base,
                        callback=callback,
                        **opts
                    )
                    cli.add_command(old_func)


def _get_path(dirpath, filename):
    return os.path.realpath(
        os.path.join(
            os.path.dirname(
                os.path.realpath(dirpath)
            ), filename
        )
    )


def _get_data(path, opts=None):
    opts = opts or {}
    with open(path, encoding='utf-8') as parsed_file:
        data = NestedDict(json.load(parsed_file))
    parsed = swagger.Swagger(data, **opts).parsed
    if not parsed.get(CONVERSION_FLAG):
        raise ValueError("Please convert your Swagger file")
    return parsed


def find_newest(versions):
    """ Find newest API version """
    return max(versions)


def filter_servers(servers):
    """ filter out non-prod servers if we can """
    # pylint: disable=invalid-name
    s = [i for i in servers if PREFERRED_HOST_PREFIX in i['url'] or
         PREFERRED_URL_PREFIX in i['url']]

    if s:
        return s
    # servers list is out of conformance so we default back to all
    return servers


def find_name(info, default=''):
    """ Find the name of module group based on Swagger info """
    for i in ['name', 'title', 'description']:
        if i in info:
            return info[i]
    return default


def generate(
        dirpath, filename=None, description=None, cli=None, name=None,
        callback=None, swagger_opts=None, condense=True
):
    """ Create a CLI from a Swagger file and path """
    # pylint: disable=too-many-locals
    filename = filename or 'swagger3.json'
    swagger_path = _get_path(dirpath, filename)
    name = name or os.path.dirname(swagger_path).split('/')[-1]
    parsed = _get_data(swagger_path, opts=swagger_opts)
    description = description or find_name(parsed.get('info', {}))

    @core.group(name, help=description)
    def base():  # pylint: disable=missing-docstring
        pass

    cli = cli or base
    base_url = ''

    servers = filter_servers(parsed.get('servers', []))
    endpoints = parsed['endpoints']
    # pylint: disable=unnecessary-comprehension
    number_endpoints = [endpoint for endpoint in endpoints.keys()]
    if len(number_endpoints) == 1 and condense:
        endpoints = endpoints[number_endpoints[0]]
    # Grab the newest API version available
    if servers:
        urls = [server['url'] for server in servers if 'url' in server]
        versions = {url.split('/')[-1]: url for url in urls if
                    url.split('/')[-1]}
        base_url = versions[find_newest(versions.keys())]

    create_commands(cli, endpoints, base=base_url, callback=callback)

    return cli
