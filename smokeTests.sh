# Run some sanity tests to make sure the built binary works.
CRAYCLI="cray"


export LC_ALL=C.UTF-8
export LANG=C.UTF-8
cli_help=$($CRAYCLI --help)
if [[ $? == 0 ]]; then
    echo "PASS: cray returns help"
else
    echo "FAIL: cray returns an error."
    exit 1
fi


cli_version=$($CRAYCLI --version)
if [[ $? == 0 ]]; then
    echo "PASS: cray --version returns $cli_version on a system"
else
    echo "FAIL: cray --version returns an error."
    exit 1
fi
