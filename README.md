# Cray CLI

## Company Internal


> __This is a work in progress. Feedback is greatly encouraged and appreciated.__
> For internal use at Cray Inc Only

## Detailed Documentation

1. [Developing the CLI](Developing.md)
1. [Integrating a New Module](Integration.md)
1. [Customer Demo Script](demo.md)
1. [Tutorial](Tutorial.md)

## Table of Contents

1. [Overview](#Overview)
1. [Install](#Install)
1. [Usage](#Usage)
1. [Environment variables](#Environment-variables)
1. [Configuration files](#Configuration-files)
1. [Installing Podman wrapper script](#installing-podman-wrapper-script)
1. [Running Podman wrapper script](#running-podman-wrapper-script)
1. [TODO](#TODO)

## Overview

The Cray CLI is a framework created to integrate all of the system management
REST APIs into one, easily usable, CLI for customers to interact with.

The framework itself is relatively lightweight and implements the basic
needs of a CLI with the ability for each team to integrate their own endpoints.

The CLI provides built in configurations (stored in ~/.config/cray), built-in
authentication token stores (similar to AWS/GCP), and a built-in parser
that can take a swagger file and generate CLI commands.

## Install

The CLI is built as an RPM and included with the "blob" and customers can install via yum:

    yum install craycli

## Usage

    terminal: cray

    Usage: cray [OPTIONS] COMMAND [ARGS]...

    Cray management and workflow tool

    Options:
      --help  Show this message and exit.

    Commands:
      auth    Manage OAuth2 credentials for the Cray CLI
      config  View and edit Cray configuration properties
      init    Initialize/reinitialize the Cray CLI

To get started run `cray init`. This will initialize the CLI on your machine and
authenticate you with the system.

## Environment variables

By default the cli looks for files in `~/.config/cray` (OS agnostic).
If a user would like to override this, it can be configured using a `CRAY_CONFIG_DIR`
environment variable. Users can also pass command options using variables like
`CRAY_[{module name}_, {group name}_, ...]{command name}_{option name}=value`

For example, `CRAY_AUTH_LOGIN_USERNAME=ryan` can be used instead of
`cray auth login --username=ryan`. These are command specific, and the above
environment variable will not be used for any commands other than `cray auth login`.

## Configuration files

As mentioned above, users can create configuration files that set default values.
Configuration files use the TOML format for ease of readability. When you run
`cray init` we automatically create the default configuration with a few values.

For example:

    [core]
    hostname='https://api.gw.url'

    [auth.login]
    username='admin'

    [module.command]
    option1='foo'
    option2='bar'

These configuration files are abstracted away from users with the `cray config`
commands. `--configuration` is a global variable that allows users to set the
configuration name to use for each command.

### Creating alternate configurations

If you have more than one system that you intend to work with, the cli can store multiple configuration files.  To create a second, third, or more, use `cray init --configuration mynewconfig`

## Installing Podman wrapper script

The Podman wrapper script, which runs the CLI in a container, is installed using a separate RPM. To install, run the following command:

    zypper -n install --auto-agree-with-licenses craycli-wrapper

## Running Podman wrapper script

To run the CLI using the the Podman container wrapper, use the following command:

    /usr/sbin/craycli-podman.sh [craycli arguments]

The arguments given to the shell script will be passed to the CLI command running in the container.

## TODO

The following are not yet implemented:

- Self updating feature.
- Ask the api gateway what modules should be installed.
- Advanced filters to ignore endpoints, etc.
- Run the parsers at build time, allowing to link external swagger files (git).
- Create a functional test generator
- Create dockerfile with cli installed
