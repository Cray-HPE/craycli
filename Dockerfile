FROM dtr.dev.cray.com/baseos/alpine:3.12.0 as builder

RUN apk add --no-cache python3 py3-pip && \
    pip install --upgrade pip && \
    pip install wheel

RUN mkdir -p /wheels

ADD . /src
WORKDIR /src

RUN pip wheel . -w wheels

FROM dtr.dev.cray.com/baseos/alpine:3.12.0 as cray

RUN apk add --no-cache python3 py3-pip && \
    pip install --upgrade pip && \
    pip install wheel

COPY --from=builder /src/wheels /tmp
RUN pip install --no-index --find-links=/tmp cray

ENTRYPOINT ["/usr/bin/cray"]
