#!/bin/bash
#
# Run Waterfox G.x under Wayland
#
export MOZ_ENABLE_WAYLAND=1
exec /usr/lib/waterfox/waterfox "$@"
