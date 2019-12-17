#!/bin/bash

set -e -x

_scriptdir="$(readlink -f $(dirname "$0"))"

# Install build dependencies
_build_deps=$(grep ^BuildRequires webthings-gateway.spec | cut -d: -f2-)
_extra_deps="rpm-build rpm-devel rpmlint patch rpmdevtools patch git-lfs"

if [[ $EUID -eq 0 ]]; then
    dnf install -y ${_extra_deps} ${_build_deps}
else
    sudo -p 'Enter sudo password to install build dependencies: ' \
        su -c "dnf install -y ${_extra_deps} ${_build_deps}"
fi

rpmdev-setuptree

# Clean up
git clean -Xdf

# Pull all sources
git lfs install
git lfs pull

# Copy in the build scripts
cp *.spec ~/rpmbuild/SPECS/
cp src/* ~/rpmbuild/SOURCES/

# Build it
rpmbuild -bb ~/rpmbuild/SPECS/webthings-gateway.spec

# Done building, let's just rename things
_rpm=$(find ~/rpmbuild/RPMS/ -type f)
ln -s "${_rpm}" "webthings-gateway.rpm"

echo ""
echo "Done building: ${_rpm}"
