# Instructions for CrayCLI Developers

## Development Process

Using the [Cray Service Generator](https://github.com/Cray-HPE/cray-generators)
is the preferred method of integrating with the CLI. This will automatically
take your swagger file and bootstrap a new CLI module from it, creating a pull
request into the CLI along the way. The only thing you need to do after this
process is create functional tests and add them to your pull request.

If you choose to manually integrate and not use the generator, our development
process is based on git flow. Do the following:

- Create a feature branch off of master
- Integrate your CLI, note that integrations will not be approved without functional tests.
- Run `nox -s tests` locally to ensure the CLI tests pass
- Create a pull request to have your changes merged into master.

### Testing against a local API server

If you would like to point the CLI at a local server that is running an API so
that you don't have to develop with an entire Cray system up and running, you
can configure the CLI like this:

```bash
cray config set core hostname=http://localhost:8080
```

if your server is running on port 8080. Since this localhost server is not
running with https, you need to set `OAUTHLIB_INSECURE_TRANSPORT=1` in your
shell.

Command:

```bash
export OAUTHLIB_INSECURE_TRANSPORT=1
cray config get core.hostname
```

Output:

```text
http://localhost:8080
```

Command:

```bash
cray mymodule things list
```

Output:

```text
[]
```

Your CLI commands are now routed to the local server.

### Testing against a hardware system

To test against a real hardware system, build the source as a wheel and install
in a virtual environment on the target system.

```bash
python -m pip install build
python -m build --wheel
scp ./dist/cray-<version>.whl <target system>
ssh <target system>
python3 -m venv venv
source venv/bin/activate
pip install cray-<version>.whl
```

Now running the `cray` command will test your source against the target system.

### Unit/Functional Testing

The CLI Framework is using [nox](https://nox.thea.codes/en/stable/) to run
tests, linting, and building documentation. This means you only need to worry
about writing unit/functional tests and we take care of testing on each python
version, auto-doc new CLI commands, etc. Test cases should be added for each new
module. Pull requests cannot be merged until a 95% code coverage is achieved.

To run tests:

```bash
nox -s tests cover
```

## Installation for Development

For development, we recommend a virtualenv with python3:

> ***NOTE*** It is recommended to install the highest version of Python supported by the application \(e.g. Python 3.10\)
> For MacOS users we recommend using [`pyenv`](https://github.com/pyenv/pyenv#homebrew-in-macos), which can be installed via
> [Homebrew (`brew`)](https://brew.sh/). Using `pyenv` enables installing every version of Python there is, and avoids 
> interactions with the system Python. For help using `pyenv`, see [setting up python](#setting-up-python).

### Setting up Python

These steps are specific to MacOS. For other distros, please ask in the CrayCLI Slack channel.

[`pyenv`](https://github.com/pyenv/pyenv) is a Python version manager for MacOS, it allows users to
install multiple versions of Python. It is not recommended to use the system's Python, since it often requires root
privileges and is a fragile dependency of the OS itself. `pyenv` installs Python versions into the user directory on
the system, keeping the Python versions local to the user session.

1. Install bew using the steps outlined on [Homebrew (`brew`)](https://brew.sh/)'s homepage.    

1. Install `pyenv`, using the directions on their MacOS page [here](https://github.com/pyenv/pyenv#homebrew-in-macos).

    > ***NOTE*** There are automatic installers mention on the linked page above.

1. Open a new shell, and invoke `pyenv` to make sure it works.
1. Install Python 3.10

    ```bash
    # Find latest Python 3.10
    pyenv install -l | grep 3.10

    pyenv install 3.10.10 # or w/e the latest one was
    ```

1. Install `virtualenv`

    > ***NOTE*** Optionally you can run `pyenv global 3.10.10` and then `python -m pip install virtualenv`. The step below
    > uses the installed path instead because not all users wnat to change their global Python version for their user account. 

    ```bash
    ~/.pyenv/versions/3.10.10/bin/python -m pip install virtualenv
    ```

1. Create a `virtualenv` for `craycli`

    ```bash
    mkdir -p ~/.virtualenvs
    ~/.pyenv/versions/3.10.10/bin/python -m virtualenv ~/.virtualenvs/craycli
    ```

### Installing craycli

1. Load the `virtualenv` (the example below uses the virtualenv created in [setting up python](#setting-up-python)).

    ```bash
    source ~/.virtualenvs/craycli/bin/activate
    ```

1. Clone `craycli` (if it isn't already cloned somewhere)

    ```bash
    git clone https://github.com/Cray-HPE/craycli.git
    cd craycli
    ```

1. Install `craycli`

    ```bash
    python -m pip install .
    cray --version
    ```

## Building

We are using `pyinstaller` to generate a binary, and then installing it on systems using an RPM.

## Bugs

If you find a bug in the `craycli` framework, feel free to open a bug in the
CASMCLOUD project.  We'll triage it within a day or two.
[File Bug](https://github.com/Cray-HPE/craycli/issues/new)

## How to update your swagger

Assuming you're using the .remote option for your module: (from the root of the forked project)

#### Convert to Swagger

> ***NOTE*** Remember to activate your `virtualenv`, or create one following
> [installation for development](#installation-for-development).

- Install CI tools.

    ```bash
    python -m pip install .[ci]
    ```

- Generate swagger.

    ```bash
    nox -s swagger -- my_service_name path/to/api/file
    ```
  
    Potential output:

    ```text
    nox > Running session swagger
    nox > Creating virtual environment (virtualenv) using python3 in .nox/swagger
    nox > /bin/bash utils/convert.sh cray/modules/ims swagger3.json
    ... 
    Wrote /Users/rusty/gitstuffs/cray-shasta/craycli/cray/modules/my_service_name/swagger3.json
    nox > Session swagger was successful.
    ```

#### Running `nox` (unit tests)

- Install CI tools.

    ```bash
    python -m pip install .[ci]
    ```

- Run unit tests.

    ```bash
    nox -s tests
    ```

    Potential output:

    ```text
    nox > Running session tests
    nox > Creating virtual environment (virtualenv) using python3 in .nox/tests
    nox > python -m pip install '.[test]'
    nox > python -m pip install .
    nox > pytest --quiet --cov=cray --cov-append --cov-config=.coveragerc --cov-report= --cov-fail-under=85 cray
    ... [100%]
    Required test coverage of 85% reached. Total coverage: 91.83%
    523 passed in 211.76s (0:03:31)
    nox > Session tests was successful.
    ```
