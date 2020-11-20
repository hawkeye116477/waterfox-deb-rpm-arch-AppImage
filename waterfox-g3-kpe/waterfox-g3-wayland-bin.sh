#!/bin/bash
#
# Run Waterfox G3 under Wayland
#
export MOZ_ENABLE_WAYLAND=1
exec /usr/lib/waterfox-g3/waterfox-g3 "$@"
