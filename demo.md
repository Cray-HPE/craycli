# Cray CLI Demo script

To demonstrate how [openAPI](https://swagger.io/docs/specification/about/) and [Click](https://palletsprojects.com/p/click/) come together to create a useful CLI we can use for interacting with Shasta, we'll add a fanciful API definition and call it.

First, we need the code and a virtual environment to work with:

``` shell
mkvirtualenv -p /usr/local/bin/python3 clidemo   # Create and activate a python3 virtual environment
pip3 install -r requirements.txt                 # The production requirements are small
pip3 install -r requirements-test.txt            # We also need nox for generating OpenAPI3
pip3 install -e .                                # Install the cray command into the virtual environment
```

Next, we need to create a module directory and add files to it:

``` shell
mkdir cray/modules/petstore/
cp cray/modules/uas/cli.py cray/modules/petstore/
touch cray/modules/petstore/__init__.py
cp tests/files/swagger.json cray/modules/petstore/
```

There are a few minor edits that the files need.  Make sure the `cli.py` file is fixed.

## Time to run the generator

The cray cli framework does some simple linting and conversion to make sure that the swagger file will process before adding the module.  Since it relies on different python modules for the generator, we wrap everything in `nox`.  

``` shell
nox -s swagger
```

## Let's explore the updated CLI that now understands our petstore

``` shell
pip3 install -e .         # Update the install in our virtualenv
cray petstore --help
```