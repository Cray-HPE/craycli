# Cray CLI Demo script

To demonstrate how [openAPI](https://swagger.io/docs/specification/about/) and [Click](https://palletsprojects.com/p/click/) come together to create a useful CLI we can use for interacting with Shasta, we'll add a fanciful API definition and call it.

First, we need the code and a virtual environment to work with:

``` shell
mkvirtualenv -p /usr/local/bin/python3 clidemo   # Create and activate a python3 virtual environment
python -m pip install .                          # Install the cray command into the virtual environment
python -m pip install .[ci]                      # We also need nox for generating OpenAPI3
```

Next, we need to create a module directory and add files to it:

``` shell
mkdir cray/modules/petstore/
cp cray/modules/uas/cli.py cray/modules/petstore/
touch cray/modules/petstore/__init__.py
cp cray/tests/files/swagger.json cray/modules/petstore/
```

There are a few minor edits that the files need.  Make sure the `cli.py` file is fixed.

## Time to run the generator

The Cray CLI framework does some simple linting and conversion to make sure that the Swagger file will process before adding the module.  Since it relies on different python modules for the generator, we wrap everything in `nox`.  

``` shell
nox -s swagger
```

## Let's explore the updated CLI that now understands our petstore

``` shell
python -m pip install -U .         # Update the install in our virtualenv
cray petstore --help
```
