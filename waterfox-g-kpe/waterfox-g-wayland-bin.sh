#!/bin/bash
#
# Run Waterfox G under Wayland
#
export MOZ_ENABLE_WAYLAND=1
exec /usr/lib/waterfox-g/waterfox-g "$@"
