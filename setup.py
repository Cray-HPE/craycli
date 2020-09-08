from setuptools import setup


with open('LICENSE.txt') as license_file:
    LICENSE = license_file.read()

with open('requirements.txt') as reqs_file:
    REQUIRMENTS = reqs_file.read()

with open('version') as vers_file:
    VERSION = vers_file.read()

setup(
    name='cray',
    author="Cray Inc.",
    author_email="rbezdicek@cray.com",
    url="http://cray.com",
    description="Cray management and workflow tool",
    long_description="A tool to help you manage and interact with a cray",
    version=VERSION,
    packages=['cray'],
    license=LICENSE,
    include_package_data=True,
    install_requires=REQUIRMENTS,
    entry_points='''
        [console_scripts]
        cray=cray.cli:cli
    '''
)
