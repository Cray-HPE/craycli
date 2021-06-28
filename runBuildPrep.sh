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
    sudo yum install -y python-devel
    sudo yum install -y python36
    sudo yum install -y python36-setuptools
    sudoyum install -y python3-devel
elif command -v zypper > /dev/null; then
    sudo zypper install -y -f -l python-pip
    sudo zypper install -y -f -l python-devel
    sudo zypper install -y -f -l python3
    sudo zypper install -y -f -l python3-setuptools
    sudo zypper install -y -f -l python3-devel
else
    echo "Unsupported package manager or package manager not found -- installing nothing"
    exit 1
fi

if ! command -v pip3 > /dev/null; then
    sudo easy_install-3.4 pip || easy_install-3.6 pip || easy_install pip
fi
sudo pip3 install --upgrade pip
sudo pip3 install --upgrade --no-use-pep517 nox
hash -r   # invalidate hash tables since we may have moved things around
sudo pip3 install --ignore-installed pyinstaller
sudo pip3 install --ignore-installed -r requirements.txt

sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

set -e

# Remove before just to ensure a clean nox env.
sudo rm -rf .nox

# Note we are running this all here as we want to break the build BEFORE an rpm is built.
sudo nox -s lint -- prod
sudo nox -s lint_modules tests cover
# Remove these files again to speed up source tar for build step.
sudo rm -rf .nox
