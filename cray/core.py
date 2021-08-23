""" Click specific subclassing and utilities

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
# pylint: disable=invalid-name
import os

import click

# Custom class decorators


def pass_context(f, *args, **kwargs):
    """ pass context wrapper """
    return click.pass_context(f, *args, **kwargs)


def argument(*param_decls, **attrs):
    """ Add arguments to commands/groups """
    def decorator(f):  # pylint: disable=missing-docstring
        attrs.setdefault('cls', Argument)
        return click.argument(*param_decls, **attrs)(f)
    return decorator


def option(*param_decls, **attrs):
    """ Use our Option class instead of clicks. """
    def decorator(f):  # pylint: disable=missing-docstring
        attrs.setdefault('cls', Option)
        return click.option(*param_decls, **attrs)(f)
    return decorator


def command(name=None, cls=None, **kwargs):
    """ Force using our Command class """
    if cls is None:
        cls = click.Command

    needs_globals = kwargs.get('needs_globals')
    if needs_globals is not None:
        del kwargs['needs_globals']

    def decorator(f):  # pylint: disable=missing-docstring
        f = click.command(name, cls, **kwargs)(f)
        if needs_globals:
            # pylint: disable=import-outside-toplevel
            from .options import global_options
            f = global_options(f)
        return f
    return decorator


def group(name=None, **kwargs):
    """ Force using our Group class """
    kwargs.setdefault('cls', Group)
    return command(name, **kwargs)


# Custom classes

class Option(click.Option):
    """ Overrides click's defaults so we can get it from the global context """

    def __init__(self, *args, **kwargs):
        self.payload_name = None
        self.no_global = None
        if 'no_global' in kwargs:
            self.no_global = kwargs['no_global']
            del kwargs['no_global']
        if 'payload_name' in kwargs:
            self.payload_name = kwargs['payload_name']
            del kwargs['payload_name']

        click.Option.__init__(self, *args, **kwargs)

    def get_default(self, ctx):
        found_default = click.Option.get_default(self, ctx)
        if self.no_global:
            return found_default
        obj = ctx.obj
        name = self.name
        found = obj['globals'].get(name, obj['config'].get_from_ctx(ctx, name))
        # Note: we have to call click.Option last in case the above commands
        # alter the state of globals/configs
        if found is None:
            found = click.Option.get_default(self, ctx)
        return found


class Argument(click.Argument):
    """ Argument class that allows names """
    # This class is needed to allow us to maintain an unaltered version
    # Click will convert names to lowercase, we need to do a .format
    # with URIs to add the path arguments, so we need the original
    # name, instead of having to do a lot of extra parsing to determine
    # the template variables.

    def __init__(self, param_decls, **kwargs):
        self.payload_name = None
        self.var_name = param_decls[0]
        if 'name' in kwargs:
            self.var_name = kwargs['name']
            del kwargs['name']
        if 'payload_name' in kwargs:
            self.payload_name = kwargs['payload_name']
            del kwargs['payload_name']
        click.Argument.__init__(self, param_decls, **kwargs)


class Group(click.Group):
    """ Group class that adds global options to each command
        as well as uses our custom classes within decorators """

    def command(self, *args, **kwargs):
        """Adapted from click.Group class to use our command decorator instead.
        As well as add global options to all commands.
        """
        def decorator(f):  # pylint: disable=missing-docstring
            if 'needs_globals' not in kwargs:
                kwargs['needs_globals'] = True
            cmd = command(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd
        return decorator

    def format_commands(self, ctx, formatter):  # pragma: NO COVER
        """Based off the click format but split up groups and commands."""
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:  # pragma: NO COVER
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if commands:
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            cmds = []
            groups = []
            for subcommand, cmd in commands:
                hlp = cmd.get_short_help_str(limit)
                if isinstance(cmd, click.Group):
                    groups.append((subcommand, hlp))
                else:
                    cmds.append((subcommand, hlp))

            if groups:
                with formatter.section('Groups'):
                    formatter.write_dl(groups)
            if cmds:
                with formatter.section('Commands'):
                    formatter.write_dl(cmds)

    def group(self, *args, **kwargs):
        """Adapted from click.Group class to use our group decorator instead.
        """
        def decorator(f):  # pylint: disable=missing-docstring
            cmd = group(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd
        return decorator


class GeneratedCommands(Group):
    """ Subclass the click.Group in order to have segregated plugins within
        the modules directory """
    DIR_NAME = 'modules'
    FILE_NAME = 'cli.py'
    FUNC_NAME = 'cli'

    def __init__(self, base_path, params, name=None, **attrs):
        Group.__init__(self, name, params=params, **attrs)
        self._module_dir = os.path.join(base_path, self.DIR_NAME)

    def list_commands(self, ctx):
        cmds = set(self.commands.keys())
        for module in os.listdir(self._module_dir):
            if os.path.isdir(os.path.join(self._module_dir, module)) and \
               not module.startswith('_'):
                cmds.add(module)
        cmds = list(cmds)
        cmds.sort()
        return cmds

    def get_command(self, ctx, cmd_name):
        if cmd_name not in self.commands:
            module_path = os.path.join(self._module_dir, cmd_name)
            filename = os.path.join(module_path, self.FILE_NAME)

            # If cli.py DNE it's not a valid module return None
            if not os.path.isfile(filename):  # pragma: NO COVER
                return None

            ns = {
                '__file__': filename
            }

            with open(filename, encoding='utf-8') as f:
                code = compile(f.read(), filename, 'exec')
                # Note: We are trusting the modules to not do bad things
                # Since these are cray created we can consider them safe.
                # Using eval will improve performance and allow modules to be
                # completely segregated.
                eval(code, ns, ns)  # pylint: disable=eval-used
            return ns[self.FUNC_NAME]
        return self.commands[cmd_name]
