#!/bin/bash

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
    docker pull dtr.dev.cray.com/rbezdicek/swagger2openapi:latest
    docker run -v $DIRNAME:/converter dtr.dev.cray.com/rbezdicek/swagger2openapi:latest $OPTS -o swagger3.json
fi
