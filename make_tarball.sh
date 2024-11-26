#!/bin/bash

APPNAME=$1
VERSION=$2
cd ../Waterfox
git ls-files --recurse-submodules | tar caf ../$APPNAME-$VERSION.tar.gz --verbatim-files-from -T- --xform s:^:$APPNAME-$VERSION/:
