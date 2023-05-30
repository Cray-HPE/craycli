# Cray-HPE Shasta CSM CLI

## Greetings

The Shasta CSM CLI is intended to provide you with an industry standard approach to managing the Shasta HPC environment via it's API plane. The CLI is a work in progress, and feedback as well as PR's are always welcom and sincerely appreciated. Please see the To-Do section at the bottom of this file for open items that offer opportunities for contribution and input.

## Detailed Documentation

1. [Developing the CLI](Developing.md)
1. [Integrating a New Module](Integration.md)
1. [Customer Demo Script](demo.md)
1. [Tutorial](Tutorial.md)

## Table of Contents

1. [Overview](#Overview)
1. [Versioning](#versioning)
1. [Usage](#usage)
1. [Environment variabtles](#Environment-variables)
1. [Configuration files](#Configuration-files)
1. [TODO](#TODO)

## Overview

The Cray CLI is a framework created to integrate all of the system management
REST APIs into one, easily usable, CLI for customers to interact with.

The framework itself is relatively lightweight and implements the basic
needs of a CLI with the ability for each team to integrate their own endpoints.

The CLI provides built in configurations (stored in ~/.config/cray), built-in
authentication token stores (similar to AWS/GCP), and a built-in parser
that can take a Swagger file and generate CLI commands.

## Versioning

The version is derived from Git by the `setuptools_scm` Python module.

- ***(stable) release***: A git-tag following the `X.Y.Z` semver format is considered a stable, release version.
  
    ```text
    # Format:
    # {tag}
    # X.Y.Z
    # X - Major
    # Y - Minor
    # Z - Micro (a.k.a. patch)
    0.1.2
    ```
- ***(stable) post-release***: A git-tag following the `X.Y.Z.postN` \(where `N` is an integer\), indicates a post-release.
  These are seldom used, and are strictly for handling documentation, packaging, or other meta
  updates after a release tag was already created where it isn't warranted to publish an
  entirely new release.
  
    ```text
    # Format:
    # {tag}
    # X.Y.Z.postN
    # X - Major
    # Y - Minor
    # Z - Micro (a.k.a. patch)
    # Z - Post release [1-9]+
    0.1.2.post1
    ```

- **(unstable)** Distance and clean; the build came from a commit that is after a git-tag, and the repository folder had no modified files.

    ```bash
    # Format       {tag}.post1.dev{distance}+{scm letter}{revision hash}
    cray, version 1.6.28.post1.dev14+g818da8a
    ```

- **(unstable/dev)** No distance and not clean; the build came from a commit that has a git-tag, and the repository had uncommitted changes.

    ```bash
    # Format       {tag}.dYYYYMMDD
    cray, version 1.6.28.d20230123
    ```

- **(unstable/dev)** Distance and not clean; the build came from one or more commits after a git-tag, and the repository had uncommitted changes.

    ```bash
    # Format       {tag}.post1.dev{distance}+{scm letter}{revision hash}.dYYYYMMDD
    cray, version 1.6.28.post1.dev3+g3071655.d20230123
    ```

The `setuptools_scm` module is configured by `pyproject.toml`.

More information about versioning, see [version number construction][3].

## Usage

- To run `craycli` in a Python Virtualenv:

    - Prerequisites:
        - python3
        - pip3
        - Python Virtualenv

          ```bash
          python3 -m venv .venv
          source ./.venv/bin/activate
          python3 -m pip install 'setuptools_scm[toml]'
          python3 -m pip install .
          ```

    - When you are done working in the Python Virtualenv.
      Use the following command to exit out of the Python Virtualenv:

      ```bash
      deactivate
      ```

- To install the development build of `craycli` type:

  ```bash
  python3 -m pip install --editable .
  ```

- To install SLES RPM versions

    - Find the unstable and stable RPMs at the following locations.

        - [Unstable RPMs][1] (e.g. main/develop/feature/bugfix branches, anything that is not a git-tag)
        - [Stable RPMs][2] (e.g. git-tags)

    - To install the latest RPM, use the following `zypper` command:

        ```bash
        ARTIFACTORY_USER=
        ARTIFACTORY_TOKEN=
        ```

        ```bash
        STREAM=stable
        HTTP_PROXY=http://hpeproxy.its.hpecorp.net:443 zypper --plus-repo=https://${ARTIFACTORY_USER}:${ARTIFACTORY_TOKEN}@artifactory.algol60.net/artifactory/csm-rpms/hpe/${STREAM}/sle-15sp4 --no-gpg-checks -n in -y craycli
        ```

## Environment variables

By default the CLI looks for files in `~/.config/cray` (OS agnostic).
If a user would like to override this, it can be configured using a `CRAY_CONFIG_DIR`
environment variable. Users can also pass command options using variables like
`CRAY_[{module name}_, {group name}_, ...]{command name}_{option name}=value`

For example, `CRAY_AUTH_LOGIN_USERNAME=ryan` can be used instead of
`cray auth login --username=ryan`. These are command-specific, and the above
environment variable will not be used for any commands other than `cray auth login`.

## Configuration files

As mentioned above, users can create configuration files that set default values.
Configuration files use the TOML format for ease of readability. When you run
`cray init` we automatically create the default configuration with a few values.

For example:

```ini
[core]
hostname='https://api.gw.url'

[auth.login]
username='admin'

[module.command]
option1='foo'
option2='bar'
```

These configuration files are abstracted away from users with the `cray config`
commands. `--configuration` is a global variable that allows users to set the
configuration name to use for each command.

### Creating alternate configurations

If you have more than one system that you intend to work with, the CLI can store multiple configuration files.  To create a second, third, or more, use `cray init --configuration mynewconfig`

## Roadmap Items

THe Shasta CSM CLI has many opportunities for enhancements. Over the course of Phase 1 of the Open Sourcing of the CSM tooling we will be refining the roadmap and priorities for the tool. Please be sure to review this document on a periodic basis for new roadmap items, and the appropriate working group in the Cray/HPE OSS community for discussions of the future of the CLI and all other CSM components.

High Priority Items:

- Self updating feature.
- OS specific packaging.

Medium Priority Items:

- Ask the api gateway what modules should be installed.
- Advanced filters to ignore endpoints, etc.
- Run the parsers at build time, allowing to link external Swagger files (git).
- Create a functional test generator

[1]: https://artifactory.algol60.net/artifactory/csm-rpms/hpe/unstable/sle-15sp4/craycli/
[2]: https://artifactory.algol60.net/artifactory/csm-rpms/hpe/stable/sle-15sp4/craycli/
[3]: https://github.com/pypa/setuptools_scm#version-number-construction
