"""
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
from setuptools import setup


with open('LICENSE') as license_file:
    LICENSE = license_file.read()

with open('requirements.txt') as reqs_file:
    REQUIRMENTS = reqs_file.read()

with open('version') as vers_file:
    VERSION = vers_file.read()

setup(
    name='cray',
    author="Hewlett Packard Enterprise LP",
    author_email="eric.lund@hpe.com",
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
