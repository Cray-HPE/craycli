# Tutorial

Recommended Reading to Review First

* [Integration](Integration.md) How to integrate your application with the CLI
* [Demo](demo.md) Demonstration of functionality presented to customers

Integrating your own CLI into this framework is quite easy. All integrations
are located in the cray/modules directory. To create a new integration:

```bash
CLI_NAME='name_of_cli'
mkdir cray/modules/$CLI_NAME
touch cray/modules/${CLI_NAME}/__init__.py
touch cray/modules/${CLI_NAME}/cli.py
```

Within your cli.py, the framework looks for a cli def as an entrypoint:

```python
import cray

@cray.group()
def cli():
    pass

@cli.command()  # Note how we add our command to the CLI group.
@cray.argument('name')
@cray.option('--end', default='.')

def hello(name, end):
    cray.echo('Hello, {}{}'.format(name, end))
```

Now from here when you run `cray` you'll see a new highlevel command named from
your `CLI_NAME` variable. If you run `cray $CLI_NAME` you'll see a `hello`
command.

```bash
cray $CLI_NAME hello World

Hello, World.

cray $CLI_NAME hello World --end !

Hello, World!
```

#### Subgroups

If your CLI is complex, you can split it up into different sub groups.

```python
import cray

@cray.group()
def cli():
    pass

@cli.group()  # Note how we add our group to the main group
def some_group():
    pass

@cli.group(name='group_two')  # Override group name from function name
def another_group():
    pass

@some_group.command(help='Some helpful text')
def command_one():
    cray.echo('Foo')

@another_group.command(name='best_command') # We can override commands too
def command_two():
    cray.echo('Bar')
```

Here we'll have something like this:

```bash
cray $CLI_NAME

...

Commands:
  some_group
  group_two


cray $CLI_NAME some_group

...

Commands:
  command_one   Some helpful text


cray $CLI_NAME group_two

...

Commands:
  best_command
```
