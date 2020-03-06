#!/bin/bash
#
# Run Waterfox Current under Wayland
#
export MOZ_ENABLE_WAYLAND=1
exec /usr/lib/waterfox-current/waterfox-current "$@"
