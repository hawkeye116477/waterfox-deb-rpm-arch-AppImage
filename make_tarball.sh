#!/bin/bash

APPNAME=$1
VERSION=$(git describe --tags --exact-match)
cd ../Waterfox
git ls-files --recurse-submodules | tar caf ../$APPNAME-$VERSION.tar.gz --verbatim-files-from -T- --xform s:^:$APPNAME-$VERSION/:

obs_folder="waterfox-kde"
if [[ "APPNAME" == "waterfox-g" ]]; then
    obs_folder="waterfox-g-appimage"
fi

rm -rf  ~/obs/home:hawkeye116477:waterfox/${obs_folder}/tar_stamps

cat << EOF >> ~/obs/home:hawkeye116477:waterfox/${obs_folder}/tar_stamps
version: $VERSION
commit: $(git rev-parse HEAD)
EOF
