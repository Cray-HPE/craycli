#!/bin/bash

set -ex

SANS_TIME_TAG="$(cat .version)-$(git rev-parse --short HEAD)"
docker pull "$IMAGE_VERSIONED"
docker tag "$IMAGE_VERSIONED" "${IMAGE_VERSIONED%:*}:$SANS_TIME_TAG"
docker push "${IMAGE_VERSIONED%:*}:$SANS_TIME_TAG" || echo 'Tag already exists'
