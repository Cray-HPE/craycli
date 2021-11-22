FROM alpine:3.14 as app

RUN apk add --no-cache bash
RUN apk add --no-cache python3
RUN apk add --no-cache python3-dev
RUN apk add --no-cache py3-pip
RUN apk add --no-cache build-base
RUN apk add --no-cache docker
RUN apk add --no-cache --repository http://nl.alpinelinux.org/alpine/edge/main libuv
RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/community nodejs-current-npm

RUN pip3 install --upgrade pip
RUN pip3 install nox

RUN npm install -g swagger2openapi

RUN mkdir -p /work
VOLUME /work
WORKDIR /work
