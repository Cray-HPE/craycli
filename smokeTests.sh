# Run some sanity tests to make sure the built binary works.
#
# MIT License
# 
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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
