#!/bin/bash
#
# MIT License
# 
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

VERSION="$(cat ./version)"

echo $VERSION > build_version

if command -v yum > /dev/null; then
    yum install -y python-devel
    yum install -y python36
    yum install -y python36-setuptools
    yum install -y python3-devel
elif command -v zypper > /dev/null; then
    zypper install -y -f -l python-pip
    zypper install -y -f -l python-devel
    zypper install -y -f -l python3
    zypper install -y -f -l python3-setuptools
    zypper install -y -f -l python3-devel
else
    echo "Unsupported package manager or package manager not found -- installing nothing"
    exit 1
fi

if ! command -v pip3 > /dev/null; then
    easy_install-3.4 pip || easy_install-3.6 pip || easy_install pip
fi
pip3 install --upgrade pip
pip3 install --upgrade --no-use-pep517 nox
hash -r   # invalidate hash tables since we may have moved things around
pip3 install --ignore-installed pyinstaller
pip3 install --ignore-installed -r requirements.txt

find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

set -e

# Remove before just to ensure a clean nox env.
rm -rf .nox

# Note we are running this all here as we want to break the build BEFORE an rpm is built.
nox -s lint -- prod
nox -s lint_modules cover

# These tests have false failures intermittently, so add retries to try and avoid this
attempt=1
while [ true ]; do
    if [ $attempt -gt 6 ]; then
        nox -s tests && break
    elif nox -s tests ; then
        break
    else
        let attempt+=1
        sleep 5
    fi
done

# Remove these files again to speed up source tar for build step.
rm -rf .nox
