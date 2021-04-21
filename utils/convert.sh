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

MODULE_PATH=$1
FILENAME=$2

DIRNAME=$PWD/$MODULE_PATH

if [ $FILENAME == '.remote' ]; then
    FILENAME=$(cat $DIRNAME/$FILENAME)
    if [[ $FILENAME == 'http'* ]]; then
        echo "Support for using remote files has been deprecated. Please use a local file"
        exit 1
    fi
fi
APP=$(which swagger2openapi)
OPTS="--targetVersion 3 --patch --resolve --resolveInternal $FILENAME"

if [ ! -z $APP ]; then
    CUR=$PWD
    cd $DIRNAME
    $APP $OPTS -o $DIRNAME/swagger3.json
    cd $CUR
else
    docker pull arti.dev.cray.com/csm-internal-docker-stable-local/craycli/swagger2openapi:latest
    docker run -v $DIRNAME:/converter arti.dev.cray.com/csm-internal-docker-stable-local/craycli/swagger2openapi:latest $OPTS -o swagger3.json
fi
