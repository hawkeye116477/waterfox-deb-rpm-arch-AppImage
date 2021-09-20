#!/bin/bash

SCRIPT_PATH=$(dirname "$0")

TSTAMP=$(date --rfc-2822)

cat /dev/stdin "$SCRIPT_PATH"/"$1"/changelog <<EOI | tee "$SCRIPT_PATH"/"$1"/changelog >/dev/null
$1 ($2-0) obs; urgency=medium

    * https://www.waterfox.net/blog/waterfox-$2-release

 -- hawkeye116477 <hawkeye116477@gmail.com>  $TSTAMP

EOI

mkdir -p "$SCRIPT_PATH"/tmp
wget https://raw.githubusercontent.com/openSUSE/obs-build/20210902/changelog2spec -O "$SCRIPT_PATH"/tmp/changelog2spec

perl "$SCRIPT_PATH"/tmp/changelog2spec "$SCRIPT_PATH"/"$1"/changelog > ~/obs/home:hawkeye116477:waterfox/"$1"/"$1".changes

rm -rf "$SCRIPT_PATH"/tmp/
