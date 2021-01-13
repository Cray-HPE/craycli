# Instructions for CrayCLI Developers

## Development Process

Using the [Cray Service Generator](https://stash.us.cray.com/projects/CLOUD/repos/cray-generators/browse)
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
$ cray config set core hostname=http://localhost:8080

```

if your server is running on port 8080. Since this localhost server is not
running with https, you need to set `OAUTHLIB_INSECURE_TRANSPORT=1` in your
shell.

```bash
$ export OAUTHLIB_INSECURE_TRANSPORT=1
$ cray config get core.hostname
http://localhost:8080
$ cray mymodule things list
[]
```

Your CLI commands are now routed to the local server.

### Testing against a hardware system

To test against a real hardware system, build the source as a wheel and install
in a virtual environment on the target system.

```bash
pip install wheel
python setup.py bdist_wheel
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

For development, we recommend the container below or a virtualenv with python3:

```bash
virtualenv -p python3 cli
cd cli
source bin/activate
git clone https://stash.us.cray.com/scm/cloud/craycli.git
cd craycli
pip install -e .
```

### Dev Container

We created a container that includes all dependencies required to run nox and
develop for the cli:

```bash
git clone https://stash.us.cray.com/scm/cloud/craycli.git
cd craycli
utils/devenv.sh
```

## Building

We are using pyinstaller to generate a binary and wrapping into an RPM.
This is integrated into the DST jenkins pipeline.

## Bugs

If you find a bug in the craycli framework, feel free to open a bug in the
casmcloud project.  We'll triage it within a day or two.
[File Bug](https://connect.us.cray.com/jira/CreateIssue!default.jspa?selectedProjectKey=CASMCLOUD&issuetype=1)

## How to update your swagger

Assuming you're using the .remote option for your module: (from the root of the forked project)


__Generate the swagger__

```
$> ./utils/devenv.sh
bash-4.4$ nox -s swagger -- my_service_name
nox > Running session swagger
nox > Creating virtualenv using python3.6 in /work/.nox/swagger
... 
nox > Session swagger was successful.
```

__Run normal tests__

```
bash-4.4$ nox -s tests
nox > Running session tests-2.7
nox > Creating virtualenv using python2.7 in /work/.nox/tests-2-7
nox > pip install --upgrade -r requirements-test.txt
nox > pip install --upgrade -e .
nox > py.test --quiet --cov=cray --cov=tests --cov-append --cov-config=.coveragerc --cov-report= --cov-fail-under=95 tests
... [100%]
Required test coverage of 95% reached. Total coverage: 95.60%
460 passed in 110.78 seconds
nox > Session tests-2.7 was successful.
bash-4.4$ exit
$>
```

If they pass open the PR and we’ll merge it asap.