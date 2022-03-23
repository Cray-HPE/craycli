FROM alpine:3.14.4 as base

RUN apk add --update npm

RUN mkdir -p /converter

WORKDIR /converter

RUN npm install -g swagger2openapi

USER 1000
ENTRYPOINT ["swagger2openapi"]
