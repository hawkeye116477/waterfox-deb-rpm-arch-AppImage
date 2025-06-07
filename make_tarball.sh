#!/bin/bash
set -eo pipefail
APPNAME="$1"; [ -z "$APPNAME" ] && { echo "Usage: $0 <APP_NAME>" >&2; exit 1; }
VERSION=$(git describe --tags --exact-match 2>/dev/null || git rev-parse --short HEAD)
REPO_ROOT="../Waterfox"; cd "$REPO_ROOT" || { echo "Error: Could not change to Git repository directory: $REPO_ROOT" >&2; exit 1; }

FILE_LIST_TEMP=$(mktemp); PIGZ_STDERR_TEMP=$(mktemp)
# Ensure temporary files are cleaned up upon script exit
trap 'rm -f "$FILE_LIST_TEMP" "$PIGZ_STDERR_TEMP"' EXIT

# Get file list to calculate total size
git ls-files --recurse-submodules -z > "$FILE_LIST_TEMP"

TOTAL_SIZE=0
if [ -s "$FILE_LIST_TEMP" ]; then
    echo "Calculating total uncompressed size for the progress bar. This may be a moment..."
    read -r TOTAL_CONTENT_AND_PADDING_SIZE NUM_FILES <<< "$(xargs -0 stat -c '%s' < "$FILE_LIST_TEMP" 2>/dev/null | awk '{total_bytes += int(($0 + 511) / 512) * 512; file_count++} END { print total_bytes, file_count }')"
    TOTAL_CONTENT_AND_PADDING_SIZE=${TOTAL_CONTENT_AND_PADDING_SIZE:-0}; NUM_FILES=${NUM_FILES:-0}

    # AWK script for unique subdirectory counting (condensed)
    # Note: 'EOF' must be at the beginning of its line.
    AWK_SCRIPT_DIRS=$(cat <<'EOF'
{dir_part=$0;sub(/[^/]*$/,"",dir_part);if(dir_part!=""){if(substr(dir_part,length(dir_part),1)=="/"){dir_part=substr(dir_part,1,length(dir_part)-1)}if(dir_part!="."){unique_dirs[dir_part]=1}}}END{cleaned_dirs_count=0;for(dir in unique_dirs){cleaned_dirs_count++}print cleaned_dirs_count}
EOF
)
    read -r CLEANED_DIRS_COUNT <<< "$(awk -v RS='\0' "$AWK_SCRIPT_DIRS" < "$FILE_LIST_TEMP")"; CLEANED_DIRS_COUNT=${CLEANED_DIRS_COUNT:-0}
    TAR_HEADER_OVERHEAD_BYTES=$(((NUM_FILES * 512)+(CLEANED_DIRS_COUNT * 512)+512))
    # Add a 5% buffer to estimate for pv to prevent overshooting
    TOTAL_SIZE=$(((TOTAL_CONTENT_AND_PADDING_SIZE + TAR_HEADER_OVERHEAD_BYTES + 1024) * 105 / 100))
fi

# Ensure TOTAL_SIZE is positive for pv if there are files
[ "$TOTAL_SIZE" -eq 0 ] && [ "$NUM_FILES" -gt 0 ] && TOTAL_SIZE=1
APPROX_COMPRESSED_SIZE=$((TOTAL_SIZE / 4)); [ "$APPROX_COMPRESSED_SIZE" -eq 0 ] && [ "$TOTAL_SIZE" -ne 0 ] && APPROX_COMPRESSED_SIZE=1

DISPLAY_SIZE_MIB=$(awk "BEGIN {printf \"%.2f\", $TOTAL_SIZE / (1024 * 1024)}")
APPROX_COMPRESSED_SIZE_MIB=$(awk "BEGIN {printf \"%.2f\", $APPROX_COMPRESSED_SIZE / (1024 * 1024)}")
echo "Estimated uncompressed archive size: ${DISPLAY_SIZE_MIB} MiB"
echo "Approximate compressed archive size: ${APPROX_COMPRESSED_SIZE_MIB} MiB"
echo "Creating archive: ../$APPNAME-$VERSION.tar.gz"

COMPRESSOR_BIN="gzip"; COMPRESSOR_ARGS=("-9")
if command -v pigz &>/dev/null; then
    COMPRESSOR_BIN="pigz"; NUM_PROCS=$(nproc 2>/dev/null || echo 4); COMPRESSOR_ARGS=("-9" "-p" "$NUM_PROCS")
    echo "Using pigz for parallel compression (estimated cores: $NUM_PROCS)."
else echo "pigz not found, falling back to gzip (single-threaded compression)."; fi

# Archiving pipeline: PV monitors the UNCOMPRESSED stream
# Commands are run in a subshell to reliably capture their exit statuses in PIPESTATUS
( < "$FILE_LIST_TEMP" xargs -0 tar -c --files-from=- --dereference --verbatim-files-from --xform "s:^:$APPNAME-$VERSION/:" -f - 2>/dev/null | pv -pterb -s "$TOTAL_SIZE" | "$COMPRESSOR_BIN" "${COMPRESSOR_ARGS[@]}" 2> "$PIGZ_STDERR_TEMP" > "../$APPNAME-$VERSION.gz.tmp" )
TAR_EXIT_STATUS=${PIPESTATUS[0]:-1}; PV_EXIT_STATUS=${PIPESTATUS[1]:-1}; COMPRESSOR_EXIT_STATUS=${PIPESTATUS[2]:-1}

FINAL_ARCHIVE_PATH="../$APPNAME-$VERSION.tar.gz"
mv "../$APPNAME-$VERSION.gz.tmp" "$FINAL_ARCHIVE_PATH" || { echo "Error: Failed to move temporary archive to final destination: '$FINAL_ARCHIVE_PATH'." >&2; exit 1; }

# --- Error Handling ---
# Check tar/xargs command status
[ "$TAR_EXIT_STATUS" -ne 0 ] && { echo "Error: tar/xargs command failed with exit status $TAR_EXIT_STATUS. Archive might be incomplete or empty." >&2; exit 1; }

# Check pv command status
if [ "$PV_EXIT_STATUS" -eq 2 ]; then echo "Error: pv command was interrupted (exit status 2). Archive might be incomplete." >&2; exit 1; fi

# Check compressor (pigz/gzip) command status
# Handle exit status 0 (success) and 1 (non-critical warning) silently
if [ "$COMPRESSOR_EXIT_STATUS" -eq 0 ] || [ "$COMPRESSOR_EXIT_STATUS" -eq 1 ]; then
    : # Success or non-critical warning, continue silently
elif [ "$COMPRESSOR_EXIT_STATUS" -eq 2 ]; then
    echo "Error: $COMPRESSOR_BIN command was interrupted (exit status 2). Archive might be corrupted." >&2; exit 1
else # Any other unexpected, non-zero status
    echo "Error: $COMPRESSOR_BIN command failed with unexpected exit status $COMPRESSOR_EXIT_STATUS. Archive might be corrupted." >&2; exit 1
fi

echo "Archiving complete: $FINAL_ARCHIVE_PATH"
echo "Final archive size: $(du -h "$FINAL_ARCHIVE_PATH" 2>/dev/null || echo "N/A")"

obs_folder="waterfox-kde"
if [[ "APPNAME" == "waterfox-g" ]]; then
    obs_folder="waterfox-g-appimage"
fi

rm -rf  ~/obs/home:hawkeye116477:waterfox/${obs_folder}/tar_stamps

cat << EOF >> ~/obs/home:hawkeye116477:waterfox/${obs_folder}/tar_stamps
version: $VERSION
commit: $(git rev-parse HEAD)
EOF
