#!/usr/bin/env bash
# Wrapper script for Cray CLI
#
# (C) Copyright 2020 Hewlett Packard Enterprise Development LP.
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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

mount_path() {
    # In podman, files can only be bind-mounted if their paths are
    # relative.  Directories can be mounted either way.  Since we are
    # going out of our way to bind-mount absolute paths, the safe way
    # to do it is to bind-mount the cooked containing directory when
    # the path is a file.  We also need to make sure that there are no
    # embedded spaces in the thing we are mounting because we can't
    # properly quote them.  So, if there are embedded spaces, we mount
    # the parent of the component with the space in its name.
    mp="$(realpath "$1" | sed -E 's:^([^[:space:]]*)(/.*[[:space:]].*)$:\1:')"
    if ! [ -d "${mp}" ]; then
        mp="$(dirname "${mp}")"
    fi
    if [ -z "${mp}" ]; then
        echo "WARNING: if '$1' is supposed to be a file, it's parent is an empty string and can't be mounted, this will probably fail." >&2
        return
    fi
    if [ "${mp}" == '/' ]; then
        echo "WARNING: if '$1' is supposed to be a file, it's parent is '/' which we cannot safely mount, this will probably fail." >&2
        return
    fi
    echo ${mp}
}

# set default container engine to podman (could also run via docker)
: ${ENGINE:="podman"}

# Figure out what cray CLI container image to use when running the
# command.  The RPM is tagged with the same tag as the container image
# so get the tag there (do this in a way that can be overridden in
# case the caller wants to use a different tag).  Then, because the
# available images may be in different registries, find the first
# matching image that the engine knows about.
: ${craycli_tag:=$(rpm -q \
                       --queryformat '%{VERSION}' \
                       craycli-wrapper\
                )-$(rpm -q \
                        --queryformat '%{RELEASE}' \
                        craycli-wrapper | \
                        cut -d '_' -f2\
                )\
    }
craycli_image=$(${ENGINE} images |\
                    grep craycli |\
                    grep "${craycli_tag}" \
                    | awk '{ printf "%s:%s",$1,$2 }' \
                    | head -1\
             )

# set the config dir location if it exists or default to user home
: ${CRAY_CONFIG_DIR:=$HOME}

# If CRAY_CREDENTIALS is set we want to pass it into the container
# so it can be used by 'cray' but only if it is set because it will
# override the configuration credentials if it is present, so check
# for the setting and compose the option here only it if is set.
if [ -n "${CRAY_CREDENTIALS}" ]; then
    cray_cred_env="-e CRAY_CREDENTIALS=${CRAY_CREDENTIALS}"
fi

# runs container while passing all arguments from this script to
# container command FIXME: Until we run a registry off the LiveCD this
# will fail in airgap - or point to k8s-nexus.

# Before running the command in the container, we need to make sure
# that any files referenced by the command have some hope of being
# found in the container.  To this end, we need to go through the
# arguments looking for likely file names.  Then normalize those to
# fully resolved absolute paths.  These can be bind-mounted in the
# container.  If we bind mount the fully resolved absolute current
# working directory too, then absolute and relative paths that are not
# modified by symbolic links will be resolvable in their raw form
# inside the container.  The final check is to make sure that any
# proposed file argument resolves the same regardless of following
# symbolic links.  If any does not, warn about it and identify the
# absolute fully resolved path that might work better, but continue
# and try to use it as is (as a raw argument).
mounts_file=$(mktemp /tmp/cli_mounts.XXXXXXXX)

# To make all of this work with relative paths in the raw form,
# we need the command to be running in the cooked version of the
# current working directory translated into the container, so get the
# path for that and add it to the list of directories to mount.
mount_path . > ${mounts_file}
real_cwd="$(realpath .)"

# To keep the list of volume mounts clean, put the CRAY_CONFIG_DIR in
# there too so it can be considered when we clean up the list.  This
# will also mean that it is volume mounted in its natural place which
# should make error messages easier to interpret.
mount_path "${CRAY_CONFIG_DIR}" >> ${mounts_file}

for arg in "$@"; do
    if echo ${arg} | grep '^[-][^=]*=' > /dev/null; then
        # This looks like an option with an equal sign specifying the
        # argument that has potential to be a file.  Strip off
        # everything up to and including the first '=' in it.
        arg="$(echo ${arg} | sed -e 's/^[^=]*=//')"
    fi
    # Check whether the argument exists as a file or whatever it is.
    # If not, we can, skip this one.
    if [ ! -e "${arg}" ] && [ ! -e "$(dirname "${arg}")" ]; then
        continue
    fi
    # There is something in the filesystem namespace for this
    # argument, so we will try to mount it and use it.  See if it has
    # potential symlink issues in it by normalizing it with and without
    # symlink expansion.  If the results differ, we may have a problem.
    rp_cooked="$(realpath "${arg}")"
    rp_raw="$(realpath -s "${arg}")"
    if [ "${rp_cooked}" != "${rp_raw}" ]; then
        echo "WARNING: if '${arg}' is meant to be a file, it may fail to resolve due to symbolic links in its path.  Try '${rp_cooked}' instead." >&2
    fi

    # Get the actual processed mount path that we are going to use...
    mount_path "${arg}" >> ${mounts_file}
done
# Make sure we only mount each directory once, since there could be
# duplicates
volume_mounts=$(sort -u ${mounts_file} | \
                    sed -e 's/\(^.*$\)/--volume \1:\1:rw/'\
             )
rm -f "${mounts_file}"

# runs container while passing all arguments from this script to
# container command.  For some reason podman or the container itself
# winds up adding carriage returns to the lines in the output, so filter
# those out.
${ENGINE} run \
    --network host \
    -it \
    --rm \
    ${volume_mounts} \
    -e "CRAY_CONFIG_DIR=${CRAY_CONFIG_DIR}" \
    ${cray_cred_env} \
    --workdir "${real_cwd}" \
    $craycli_image "$@" | tr -d '\r'
