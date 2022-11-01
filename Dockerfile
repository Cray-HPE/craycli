#
# MIT License
#
# (C) Copyright 2018-2022 Hewlett Packard Enterprise Development LP
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
#
# Dockerfile for building HMS bss.

### build-base stage ###
# Build base just has the packages installed we need.
FROM python:3.8.2-alpine AS build-base

RUN set -ex \
    && apk -U upgrade \
    && apk add build-base

### base stage ###
# Base copies in the files we need to test/build.
FROM build-base AS base

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip install --upgrade pip && pip install pyinstaller

# Copy all the necessary files to the image.
COPY . .

### Build Stage ###
FROM base AS builder

RUN pyinstaller --clean -y \
    --hidden-import toml \
    --hidden-import configparser \
    --hidden-import boto3 \
    --hidden-import websocket \
    --hidden-import argparse \
    --add-data .version:cray \
    --add-data cray/modules:cray/modules \
    -p cray --onefile cray/cli.py -n cray

RUN pip install cray
