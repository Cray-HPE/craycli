""" Helpful utility functions """
import os
import tempfile

from contextlib import contextmanager

import click
from six.moves import urllib


def delete_keys_from_dict(dict_del, lst_keys):
    """Delete key within nested dicts. The original dict is altered in place.
    WARNING: This is recursive, use it wisely. """
    # pylint: disable=invalid-name
    if len(lst_keys) == 1:
        try:
            del dict_del[lst_keys.pop(0)]
        except KeyError:  # pragma: NO COVER
            raise click.UsageError('Specified value does not exist. Use ' +
                                   '`cray config list` to view your config.')
    else:
        delete_keys_from_dict(dict_del[lst_keys.pop(0)], lst_keys)


def merge_dict(d1, d2):
    """Merge two dictionaries maintaining values in nested dicts
    WARNING: This is recursive, use it wisely. """
    # pylint: disable=invalid-name
    if isinstance(d2, dict):  # pragma: NO COVER
        for k in d2.keys():
            if d1.get(k, None) and isinstance(d1[k], dict):
                if not isinstance(d2[k], dict):
                    # Assume default dict is correct here.
                    e = 'Expected {0} to be {1}'.format(type(d2[k]), dict)
                    raise ValueError(e)
                merge_dict(d1[k], d2[k])
            else:
                d1[k] = d2[k]
        return d1
    return d1.update(d2)


def get_hostname(ctx=None):
    """ Get the current API Gateway Hostname or error if not found """
    ctx = ctx or click.get_current_context()
    config = ctx.obj['config']
    hostname = config.get('core.hostname', None)
    if hostname is None:
        msg = "No hostname configured. Run `cray config set core " + \
              "hostname={Cray API URL}`"
        raise click.UsageError(msg)
    return hostname


def hostname_to_name(hostname=None, ctx=None):
    """ Convert hostname to name value for saving as filename"""
    hostname = hostname or get_hostname(ctx=ctx)
    _, netloc, path, _, _ = urllib.parse.urlsplit(hostname)
    host = netloc or path
    name = host.replace('-', '_').replace('.', '_')
    return name


@contextmanager
def open_atomic(path, perms=0o600):
    """ Open a file to be written atomically """
    # Create a temporary file in the same directory, since we can't rename
    # across filesystems
    tmpfd, tmpfname = tempfile.mkstemp(dir=os.path.dirname(path))
    os.close(tmpfd)

    with open(tmpfname, 'w') as tmpfp:
        try:
            yield tmpfp
        finally:
            tmpfp.flush()
            os.fsync(tmpfp.fileno())

    os.chmod(tmpfname, perms)
    os.rename(tmpfname, path)
