#!/bin/bash

if [ "$XDG_CURRENT_DESKTOP" == "KDE" ] && dpkg --compare-versions "$(dpkg-query -f='${Version}' --show libgtk-3-0)" ge 3.24.4; then
    export GTK_USE_PORTAL=1
fi

exec /usr/lib/waterfox-beta/waterfox-beta "$@"
