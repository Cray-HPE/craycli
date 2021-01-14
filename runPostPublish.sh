#!/bin/bash

VERSION="$(cat ./version)"
TAG="v$VERSION"

if [[ "$GIT_BRANCH" == 'origin/master' ]]; then
    echo "TODO"
    #git tag $TAG && git push origin --tags
fi
