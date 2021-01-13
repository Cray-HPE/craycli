""" Handles logging for the CLI """
import click

# Logging levels
# Note, there is purposely no ERROR level, if an actual error occurs an
# exception should be raise from the exceptions library provided. If you
# do not think it merits an exception than it is not an error.
LOG_FORCE = 0  # Generally avoided, used by the config module
LOG_WARN = 0
LOG_INFO = 1
LOG_DEBUG = 2
LOG_RAW = 3  # Ultra verbose


# Custom utils
def echo(*args, **kwargs):
    """ Logging to console and files """
    default_verbose = 0
    default_is_quiet = False
    try:
        ctx = kwargs.get('ctx', click.get_current_context())
        verbosity = ctx.obj['globals'].get('verbose', default_verbose)
        is_quiet = ctx.obj['globals'].get('quiet', default_is_quiet)
    except RuntimeError:
        # This is mostly a workaround for unit tests.
        verbosity = default_verbose
        is_quiet = default_is_quiet

    if 'ctx' in kwargs:
        del kwargs['ctx']
    level = kwargs.get('level', 2)
    if 'level' in kwargs:
        del kwargs['level']
    to_log = (level <= verbosity)

    if not is_quiet and to_log:
        click.echo(*args, **kwargs)
