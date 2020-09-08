FROM alpine:node8 as base

RUN mkdir -p /converter

WORKDIR /converter

RUN npm install -g swagger2openapi

USER 1000
ENTRYPOINT ["swagger2openapi"]