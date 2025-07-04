#!/bin/bash

# Change to the directory where the script is located
SCRIPT_DIR=$(dirname "$(realpath -s "$0")")
cd "$SCRIPT_DIR" || {
    echo "Error: Could not change directory to $SCRIPT_DIR. Exiting."
    exit 1
}

# Start timer for the entire script execution (though only pipeline time is displayed at the end)
START_TIME=$(date +%s)

# Default compression method and output extension
DEFAULT_COMPRESSOR="pigz"     # Default to pigz for speed
DESIRED_COMPRESSION_METHOD="" # Variable to store the user's chosen method

# Function to display usage information
usage() {
    echo "Usage: $0 <APPNAME> [-c <compression_method>]"
    echo "  <APPNAME>          : The name of the application to archive."
    echo "  -c <compression_method> : Optional. Specify the compression method (xz, pigz, gzip)."
    echo "                         Default: pigz (falls back to gzip if pigz not found)."
    exit 1
}

# Parse command-line arguments
if [ -z "$1" ]; then
    usage
fi

APPNAME=$1
shift # Shift APPNAME so getopts can process the next arguments

# Process optional arguments
while getopts ":c:" opt; do
    case ${opt} in
    c)
        DESIRED_COMPRESSION_METHOD=$OPTARG
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        usage
        ;;
    :)
        echo "Option -$OPTARG requires an argument." >&2
        usage
        ;;
    esac
done
shift $((OPTIND - 1)) # Adjust positional parameters after processing options

SOURCE_DIR="../Waterfox" # Directory containing the Git repository

# Change to the source directory, exit if it fails
cd "$SOURCE_DIR" || {
    echo "Error: Could not change directory to $SOURCE_DIR. Exiting."
    exit 1
}

# Get Git version tag; use 'unknown' if no exact tag is found
VERSION=$(git describe --tags --exact-match 2>/dev/null)
if [ -z "$VERSION" ]; then
    VERSION="unknown"
fi

# --- Determine the best available compressor and set output filename dynamically ---
COMPRESSOR_CMD=""   # The full command for the chosen compressor
COMPRESSOR_NAME=""  # Just the name of the chosen compressor (e.g., 'xz', 'pigz')
OUTPUT_EXTENSION="" # The file extension for the compressed archive

# Function to set compressor based on availability and desired method
set_compressor() {
    local method_preference="$1"
    case "$method_preference" in
    "xz")
        if command -v xz &>/dev/null; then
            COMPRESSOR_CMD="xz -6 -T0"
            COMPRESSOR_NAME="xz"
            OUTPUT_EXTENSION=".tar.xz"
            echo "Using xz for compression (optimal level, multi-threaded) as requested."
            return 0
        else
            echo "Warning: xz not found. Cannot use xz compression."
            return 1
        fi
        ;;
    "pigz")
        if command -v pigz &>/dev/null; then
            COMPRESSOR_CMD="pigz -6"
            COMPRESSOR_NAME="pigz"
            OUTPUT_EXTENSION=".tar.gz"
            echo "Using pigz for parallel compression (optimal level) as requested."
            return 0
        else
            echo "Warning: pigz not found. Cannot use pigz compression."
            return 1
        fi
        ;;
    "gzip")
        if command -v gzip &>/dev/null; then
            COMPRESSOR_CMD="gzip -6"
            COMPRESSOR_NAME="gzip"
            OUTPUT_EXTENSION=".tar.gz"
            echo "Using gzip for compression (optimal level) as requested."
            return 0
        else
            echo "Error: gzip not found. No compression utility available. Exiting."
            exit 1
        fi
        ;;
    *)
        echo "Error: Invalid compression method specified: '$method_preference'."
        return 1
        ;;
    esac
}

# If a specific compression method was requested, try to set it
if [ -n "$DESIRED_COMPRESSION_METHOD" ]; then
    if ! set_compressor "$DESIRED_COMPRESSION_METHOD"; then
        echo "Attempting to fall back to default compression methods..."
        # If the requested method failed, proceed to default fallback logic
        DESIRED_COMPRESSION_METHOD="" # Clear to trigger default logic below
    fi
fi

# If compressor is still not set (either no method requested or requested method failed),
# apply the default fallback logic: pigz -> gzip
if [ -z "$COMPRESSOR_NAME" ]; then
    if command -v pigz &>/dev/null; then
        COMPRESSOR_CMD="pigz -6"
        COMPRESSOR_NAME="pigz"
        OUTPUT_EXTENSION=".tar.gz"
        echo "Using pigz for parallel compression (optimal level) by default."
    elif command -v gzip &>/dev/null; then
        COMPRESSOR_CMD="gzip -6"
        COMPRESSOR_NAME="gzip"
        OUTPUT_EXTENSION=".tar.gz"
        echo "Warning: pigz not found. Falling back to gzip (optimal level) by default."
    else
        echo "Error: Neither pigz nor gzip found. No compression utility available. Exiting."
        exit 1
    fi
fi

# Construct the full output filename and the internal directory name for the archive
OUTPUT_FILENAME="../$APPNAME-$VERSION$OUTPUT_EXTENSION"
ARCHIVE_INTERNAL_DIR=$(basename "$OUTPUT_FILENAME" "$OUTPUT_EXTENSION") # e.g., 'myapp-1.0' from 'myapp-1.0.tar.xz'

echo "Archiving current repository to '$OUTPUT_FILENAME' with internal root '$ARCHIVE_INTERNAL_DIR/'..."

# --- Calculate estimated sizes for progress bar and display ---
# Create a temporary file to store the list of files to be archived
TEMP_FILE_LIST=$(mktemp)
# Populate the temporary file with null-separated list of tracked files, including submodules
git ls-files --recurse-submodules -z >"$TEMP_FILE_LIST"

TOTAL_UNCOMPRESSED_FILE_BYTES=0         # Total bytes of all files before tar overhead
NUMBER_OF_FILES=0                       # Total count of files
TOTAL_SIZE_FOR_PV=0                     # Estimated total bytes for pv (uncompressed stream, including tar overhead)
UNCOMPRESSED_DISPLAY_SIZE="0KB"         # Human-readable uncompressed size
ESTIMATED_COMPRESSED_DISPLAY_SIZE="N/A" # Human-readable estimated compressed size
ESTIMATED_COMPRESSED_BYTES=0            # Raw byte count for estimated compressed size

# Check if git ls-files returned any files
if [ ! -s "$TEMP_FILE_LIST" ]; then
    echo "Info: git ls-files returned no files. Archive will be empty or very small."
else
    # Calculate total uncompressed file bytes using du from the file list
    RAW_DU_OUTPUT=$(cat "$TEMP_FILE_LIST" | xargs -0 du -b 2>/dev/null)
    TOTAL_UNCOMPRESSED_FILE_BYTES=$(echo "$RAW_DU_OUTPUT" | awk '{s+=$1} END {print s}')
    # Get the number of files by counting null-separated entries
    NUMBER_OF_FILES=$(grep -zc . "$TEMP_FILE_LIST")

    # Handle cases where calculations might result in empty or zero values unexpectedly
    if [[ -z "$TOTAL_UNCOMPRESSED_FILE_BYTES" || ! "$TOTAL_UNCOMPRESSED_FILE_BYTES" =~ ^[0-9]+$ ]]; then
        TOTAL_UNCOMPRESSED_FILE_BYTES=0
    fi
    # Ensure a minimum byte count if files exist but du reports 0 (e.g., all empty files)
    if [ "$NUMBER_OF_FILES" -gt 0 ] && [ "$TOTAL_UNCOMPRESSED_FILE_BYTES" -eq 0 ]; then
        TOTAL_UNCOMPRESSED_FILE_BYTES=1
    fi

    if [ "$NUMBER_OF_FILES" -gt 0 ]; then
        # Estimate tar's metadata overhead (512 bytes per file/directory entry is common)
        METADATA_OVERHEAD=$((NUMBER_OF_FILES * 512))
        # Add a buffer for tar's internal streaming overhead (e.g., ~16.6%)
        ADDITIONAL_BUFFER=$((TOTAL_UNCOMPRESSED_FILE_BYTES / 6))
        ADDITIONAL_BUFFER=$((ADDITIONAL_BUFFER + 1))
        # Total size for pv includes file bytes, metadata, and a buffer
        TOTAL_SIZE_FOR_PV=$((TOTAL_UNCOMPRESSED_FILE_BYTES + METADATA_OVERHEAD + ADDITIONAL_BUFFER))

        # Ensure TOTAL_SIZE_FOR_PV is at least 1MB to avoid pv issues with very small targets
        if [ "$NUMBER_OF_FILES" -gt 0 ] && [ "$TOTAL_SIZE_FOR_PV" -lt 1048576 ]; then
            TOTAL_SIZE_FOR_PV=1048576 # Set to minimum 1MB (1024*1024 bytes)
        fi

        # Convert uncompressed bytes to human-readable format (KB, MB, GB)
        if ((TOTAL_UNCOMPRESSED_FILE_BYTES >= 1073741824)); then
            UNCOMPRESSED_DISPLAY_SIZE=$(echo "scale=2; $TOTAL_UNCOMPRESSED_FILE_BYTES / 1073741824" | bc)GB
        elif ((TOTAL_UNCOMPRESSED_FILE_BYTES >= 1048576)); then
            UNCOMPRESSED_DISPLAY_SIZE=$(echo "scale=2; $TOTAL_UNCOMPRESSED_FILE_BYTES / 1048576" | bc)MB
        else
            UNCOMPRESSED_DISPLAY_SIZE=$(echo "scale=2; $TOTAL_UNCOMPRESSED_FILE_BYTES / 1024" | bc)KB
        fi

        # Estimate compressed bytes based on typical ratios for optimal levels
        if [ "$COMPRESSOR_NAME" = "xz" ]; then
            # xz at -6 usually achieves around 5.5:1 compression
            ESTIMATED_COMPRESSED_BYTES=$(echo "scale=0; $TOTAL_UNCOMPRESSED_FILE_BYTES / 5.5" | bc)
        else
            # gzip/pigz at -6 usually achieve around 3.5:1 compression
            ESTIMATED_COMPRESSED_BYTES=$(echo "scale=0; $TOTAL_UNCOMPRESSED_FILE_BYTES * 2 / 7" | bc)
        fi

        # Ensure estimated compressed bytes are positive for display
        if [ "$ESTIMATED_COMPRESSED_BYTES" -le 0 ] && [ "$TOTAL_UNCOMPRESSED_FILE_BYTES" -gt 0 ]; then
            ESTIMATED_COMPRESSED_BYTES=1
        fi
        # Convert estimated compressed bytes to human-readable format (KB, MB, GB)
        if ((ESTIMATED_COMPRESSED_BYTES < 1024 && ESTIMATED_COMPRESSED_BYTES > 0)); then
            ESTIMATED_COMPRESSED_DISPLAY_SIZE="<1KB"
        elif ((ESTIMATED_COMPRESSED_BYTES >= 1073741824)); then
            ESTIMATED_COMPRESSED_DISPLAY_SIZE=$(echo "scale=2; $ESTIMATED_COMPRESSED_BYTES / 1073741824" | bc)GB
        elif ((ESTIMATED_COMPRESSED_BYTES >= 1048576)); then
            ESTIMATED_COMPRESSED_DISPLAY_SIZE=$(echo "scale=2; $ESTIMATED_COMPRESSED_BYTES / 1048576" | bc)MB
        else
            ESTIMATED_COMPRESSED_DISPLAY_SIZE=$(echo "scale=2; $ESTIMATED_COMPRESSED_BYTES / 1024" | bc)KB
        fi
    fi
fi
rm -f "$TEMP_FILE_LIST" # Clean up the temporary file list

echo "Estimated total uncompressed content size (files only): ${UNCOMPRESSED_DISPLAY_SIZE}"
echo "Estimated compressed size (approx. ratio for $COMPRESSOR_NAME at optimal level): ${ESTIMATED_COMPRESSED_DISPLAY_SIZE}"

# Start timer just before the main archiving pipeline begins
PIPELINE_START_TIME=$(date +%s)

# --- Archiving pipeline: git ls-files -> tar -> pv -> compressor -> output file ---
if [[ "$TOTAL_SIZE_FOR_PV" -eq 0 ]]; then
    # If no precise size target was calculated, pv shows throughput only
    echo "Warning: No precise size target for progress. Displaying throughput only."

    git ls-files --recurse-submodules -z |
        tar -c --null --format=pax --verbatim-files-from -T- --xform "s:^:$ARCHIVE_INTERNAL_DIR/:" |
        pv --progress --eta --bytes --rate |
        $COMPRESSOR_CMD >"$OUTPUT_FILENAME"
else
    # pv monitors the uncompressed data stream using the calculated size target
    echo "Progress bar will track the uncompressed data stream (approx. ${UNCOMPRESSED_DISPLAY_SIZE})."
    echo "Note: The final file on disk will be smaller due to compression. ETA here is for data transfer to compressor."

    git ls-files --recurse-submodules -z |
        tar -c --null --format=pax --verbatim-files-from -T- --xform "s:^:$ARCHIVE_INTERNAL_DIR/:" |
        pv --progress --eta --bytes --rate --size "$TOTAL_SIZE_FOR_PV" |
        $COMPRESSOR_CMD >"$OUTPUT_FILENAME"
fi

# --- Post-archiving checks and final output ---
# Check the exit status of the last command in the pipeline
if [ $? -eq 0 ]; then
    echo "Archiving complete!"
    # Get and display the actual compressed size of the output file
    COMPRESSED_SIZE=$(du -h "$OUTPUT_FILENAME" | awk '{print $1}')
    echo "Actual compressed size: $COMPRESSED_SIZE"
else
    echo "Error: Archiving failed. Check for issues with git, tar, pv, or $COMPRESSOR_NAME."
    exit 1
fi

# End timer for the archiving pipeline and display total elapsed time
PIPELINE_END_TIME=$(date +%s)
ELAPSED_PIPELINE_TIME=$((PIPELINE_END_TIME - PIPELINE_START_TIME))
echo "Archiving pipeline time: ${ELAPSED_PIPELINE_TIME} seconds."

obs_folder="waterfox-kde"
if [[ "$APPNAME" == "waterfox-g" ]]; then
    obs_folder="waterfox-g-appimage"
fi

rm -rf ~/obs/home:hawkeye116477:waterfox/${obs_folder}/tar_stamps

cat <<EOF >>~/obs/home:hawkeye116477:waterfox/${obs_folder}/tar_stamps
version: $VERSION
commit: $(git rev-parse HEAD)
EOF
