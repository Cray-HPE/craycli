# Integrating modules

Integrating an API with the CLI is a fairly easy process once you have a valid swagger file.

1. Fork this repository to make changes (Do not attempt to branch.  You do not have write permissions)
1. Add your module and swagger file to the `cray/modules/` directory
1. Run the swagger parser to convert from a swagger.yaml file to a json file and validate

See the [demo](demo.md) for what we showed the Compass group in Jan '19.

We've provided a generator that will create a CLI from the stash URL of your swagger file:

    pip3 install nox
    nox -s generate -- [module name] [stash swagger url]

I.e.

    nox -s generate -- uas https://github.com/Cray-HPE/uan-mgr/blob/main/api/swagger.yaml

*NOTE: The generator appends `?raw&at=refs%2Fheads%2Fmaster` to the passed in URL.
You are required to use the master branch. For local development, you can pass a local
file to the generate command. However, using remote files is highly encouraged when you open your pull request.*

*NOTE: Support for anyOf/allOf/oneOf keywords in OpenAPI 3 has been added. All
options under these keywords are added to the option list for the individual
command that uses them. Any validation of required options must be done on the
server side.

This will create everything required to create a CLI from your swagger file. You can now making any customizations required. The above command is idempotent and will not overwrite any customizations you've made. Make sure you write a few functional tests for your CLI to ensure it is working as you expect.

### Why the manual parse to generate yet another file?

Multiple reasons, the first being we are mostly on Swagger 2.0 with plans to migrate.
This would add a lot of unneeded dependencies into the CLI to do the conversion.
Also, since we will have many modules, having to do the conversion and parsing on
the fly for each module will be a big performance hit. The CLI needs to parse
each module to get a list of commands when it runs. We want to optimize this
as much as possible.


### Notes on user experience

We encourage all integrators to use our swagger file parser to automatically
generate your CLI module. This will automatically create CLI commands based on
your REST endpoints and add options/arguments based on the payload.

This will ensure we use the same vocabulary and user experience across modules.
If you believe your REST API is too complex to be automatically generated we encourage
you to consider simplifying your API. Your API is just as much a UI as the CLI is.

That said, we understand there are scenarios where complex APIs are required or
manually creating CLI commands is needed. If this is the case for you please carefully
read the documentation below.


## Basic Example

An example of your cli.py will look like this:

    from cray.generator import generate
    from cray.core import echo


    def cb(response):
        """ Optional callback to do post-processing on REST responses.
        Passes in a requests lib response object. It's best to omit this
        unless you have specific tasks to do. The formatter will handle
        formatting the result in JSON, TOML, text, or any of the other supported
        formats."""
        echo("Status code: {}".format(response.status_code))
        return response


    # Pass in the CLI group you want the commands to be added to, the directory
    # where you module lives, the name of your parsed swagger file, and an
    # optional callback.
    cli = generate(__file__, callback=cb)

## Advanced Example

    from cray.generator import generate
    from cray.core import argument, option, echo


    cli = generate(__file__)


    @cli.command(name="demo")
    @argument("name")
    @option('--shout', is_flag=True)
    def demo(name, shout):
        echo("This is a verbose statement")
        resp = 'Hello, {}'.format(name)
        if shout:
            resp = '{}!!'.format(resp.upper())
        return resp

## Guidelines

The CLI is an internal standard that controls how users interact with a cray system.  It makes a few assumptions about the services it is calling.  Because it is just one client and not the only possible client, services may choose to implement more sophisticated strctures than are currently supported by the CLI.  The CLI will adhere to these guidelines when making calls to services.

### Supported CLI MIME types

```
   'application/json'
   'application/x-www-form-urlencoded'
   'application/octet-stream'
   'multipart/form-data'
```

### Parameters

For all intents and purposes, `cray.argument` and `cray.option` acts just like
[`click.argument`](https://click.palletsprojects.com/en/7.x/arguments/) and [`click.option`](https://click.palletsprojects.com/en/7.x/options/), with one caveat. All options within
the cray cli can have a default value defined within a configuration file. When you add an
option to a command, the framework will first attempt to find a default value from
the configuration file before using the options `default` variable. This is why
it is so important to only use parameters on `cray.commands`, as configuration files
are not loaded until just before the command is called. Note: default values are only
used if the option is not provided in the command.

If your parameter expects a nonstring value, click provides a few nice
predefined types that it will automatically handle for you. See the [click documentation](https://click.palletsprojects.com/en/7.x/parameters/#parameter-types) for more information.

#### Thoughts on short names

Although providing short names are nice for options (`-c` for `--configuration`)
they can quickly get out of hand. We recommend only using short names for options if:

1) The option has an exceptionally long name
2) The option is used very frequently but is rarely static (and therefore can't easily be set in a configuration file). Evaluate if using arguments instead of options makes sense in this case.

#### Parameter best practices

1) Offer as few options as possible.
2) Every option is required to have a help
3) Map REST verbs as follows:
    - GET single: `describe`
    - GET multiple: `list`
    - POST: `create`
    - PUT/PATCH: `update`
    - DELETE: `delete`

### API Tags

craycli has the ability to parse API tags to add additional functionality 
that is only for CLI interactions. The following tags are available:

* **cli\_hidden** - API interfaces tagged with this will be hidden from the
CLI when --help is run
* **cli\_ignore** - API interfaces tagger with this will be ignored and not
shown in the help or available for use.
* **cli\_danger** - Prompts the user before completing the operation. This is
used for potentially dangerous operations like "delete all the things".
cli_danger offers an additional feature that allows APIs to specify their own
confirmation message. A string passed along with this tag separated by a $ will
be the confirmation message. For example, "cli\_danger$This will delete
everything, continue?"

Note: Tags that craycli does not recognize are ignored by the CLI.

#### Usage Example

The tags need to be placed on the API calls themselves, not at the top level. 

Example of **cli_danger** with the optional message:

	/uais:
      delete:
        tags:
        - "cli_danger$This will delete all running UAIs, Are you sure?"
        summary: "Delete all UAIs on the system"
      
Example of **cli_ignore**:
	
	/:
	  get:
	    tags:
		 - "cli_ignore"


## Non-REST functionality

The CLI is based on python click framework. However, in order to provide some
nice features like configuration files and global options, we've had to extend
some of their capabilities. This adds some caveats you need to know when
developing.

1. Always use cray provided decorators and classes, try to avoid using click directly
2. Only add arguments and options to commands, never groups[\*](#Note)
3. Be very careful when doing anything within a group function[\*](#Note)
4. Assume argument/options/globals can change up until the point your command function is called[\*](#Note)
5. Use `cray.echo` for any information that can be omitted with a `--quiet`, your command should `return` your final data, whether it is text or a dict. The CLI will automatically format a returned `dict` based on the `--format` option. The returned `dict` needs to be json serializable.

### Note

\* We had to make some concessions in order to have a configuration file with
automatic defaults as well as global options. Since a `--configuration` option
is automatically added to each command, we don't load configuration files
until right before the command is called. It's the first parameter to be handled
for a command. Users can add default values for ANY parameter. This means
that the loading goes:

    - Group level parameters loaded and group function called
    - Load configuration file (based on envvar, configuration option, or default)
    - All other parameters are loaded, default value goes in this order:
            - Check global variables
            - Check configuration file
            - Check if parameter provided a default value
            - Return None

As you can see, putting anything in a group level function can be called
BEFORE the configuration file is loaded and global variables are set.
