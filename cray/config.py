""" Classes that interact with configuration files. """
# pylint: disable=invalid-name

import os

import click
import toml

from cray.constants import NAME, ACTIVE_CONFIG
from cray.nesteddict import NestedDict
from cray.utils import open_atomic

_CONFIG_DIR_NAME = 'configurations'
_LOG_DIR_NAME = 'logs'
_AUTH_DIR_NAME = 'tokens'


def _read_file(path, frmt=toml):
    data = None
    if os.path.isfile(path):
        with open(path, 'r') as f:
            data = frmt.load(f)
    return data


def _get_cmd_call(ctx, names=None):
    names = names or []
    if isinstance(ctx, click.Context) and ctx.info_name != NAME:
        names.append(ctx.info_name)
        return _get_cmd_call(ctx.parent, names)
    return '.'.join(names[::-1])


def initialize_dirs(path):
    """ Create initial configuration directory structure. """
    for folder in [_CONFIG_DIR_NAME, _LOG_DIR_NAME, _AUTH_DIR_NAME]:
        mkdir = os.path.join(path, folder)
        try:
            os.makedirs(mkdir)
        except OSError:  # pragma: NO COVER
            if not os.path.isdir(mkdir):
                raise


class Config(NestedDict):
    """Loads configuration from disk and becomes a dict.
    If you think you need this, you probably don't.
    Use ctx.obj.config instead.
    """

    _CORE_KEYS = ['hostname', 'quiet', 'format']

    def __init__(self, path, config, raise_err=False):
        # pylint: disable=super-init-not-called
        self._format = toml
        self._config_dir = path
        self._config_name = config
        self._raise_err = raise_err
        self.update(**self._load())

    def _values(self):
        return {key: self[key] for key in self.keys()}

    def get_config_dir(self):
        """ Get the base config directory """
        return self._config_dir

    def set_active(self):
        """ Set the active config """
        with open_atomic(os.path.join(self._config_dir, ACTIVE_CONFIG)) as fp:
            fp.write(self._config_name)

    def get_configurations_dir(self):
        """ Get the config configurations directory """
        return os.path.join(self._config_dir, _CONFIG_DIR_NAME)

    def _get_config_file_name(self):
        return os.path.join(self._config_dir, _CONFIG_DIR_NAME,
                            self._config_name)

    def _load(self):
        data = _read_file(self._get_config_file_name())
        if not data and self._raise_err:
            raise click.UsageError("Unable to find configuration file.")
        data = data or {}
        return data

    def reload(self):
        """ Reload a config, really only helpful for tests """
        return self._load()

    def show(self, frmt=None):
        """ Get a string dump of the config """
        frmt = frmt or self._format  # pragma: NO COVER
        return frmt.dumps(self._values())

    def save(self):
        """ Get a string dump of the config """
        with open_atomic(self._get_config_file_name()) as f:
            self._format.dump(self._values(), f)

    def get_core(self, value, default=None):
        """ If value is in core section return the key,
        otherwise return default """
        if value in self._CORE_KEYS:
            'core.{}'.format(value)
        return default

    def get_from_ctx(self, ctx, key, default=None):
        """ Get a value based on current context and parameter name. """
        key = self.get_core(key, _get_cmd_call(ctx, [key]))
        return self.get(key, default)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
