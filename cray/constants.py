""" Constants """


def _make_envvar(var):
    return '{}_{}'.format(NAME, var).upper()


# Main name of CLI
NAME = 'cray'
# Various global env vars that can be used.
CONFIG_ENVVAR = _make_envvar('CONFIG')
TOKEN_ENVVAR = _make_envvar('CREDENTIALS')
QUIET_ENVVAR = _make_envvar('QUIET')
FORMAT_ENVVAR = _make_envvar('FORMAT')
CONFIG_DIR_ENVVAR = _make_envvar('CONFIG_DIR')

# Generator constants
TAG_SPLIT = "$"
IGNORE_TAG = "cli_ignore"
HIDDEN_TAG = "cli_hidden"
DANGER_TAG = "cli_danger"
FROM_FILE_TAG = "cli_from_file"
CONVERSTION_FLAG = "cray_converted"


# Config constants
DEFAULT_CONFIG = 'default'
ACTIVE_CONFIG = 'active_config'
EMPTY_CONFIG = ''
CONFIG_DIR_NAME = 'configurations'
LOG_DIR_NAME = 'logs'
AUTH_DIR_NAME = 'tokens'
