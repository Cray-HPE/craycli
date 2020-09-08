
DIR=${1:-$PWD}
CUR=$PWD
IMAGE="dtr.dev.cray.com/rbezdicek/craycli-devenv:v2"

cd $DIR
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
docker pull $IMAGE
docker run -u ${UID}:${GID} -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/work -it $IMAGE /bin/bash
cd $CUR

