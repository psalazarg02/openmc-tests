#!/bin/bash

# move.sh - Flexible file moving script for OpenMC simulation results

# Default values
START_NUM=0
END_NUM=6
FOLDER_NUM=01

# Function to show usage
show_usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -s NUM    Starting simulation number (default: 0)"
    echo "  -e NUM    Ending simulation number (default: 6)" 
    echo "  -f NUM    Folder number (default: 01)"
    echo "  -h        Show this help message"
    echo ""
    echo "Example: $0 -s 0 -e 10 -f 02"
}

# Parse command line arguments
while getopts "s:e:f:h" opt; do
    case $opt in
        s)
            START_NUM=$OPTARG
            ;;
        e)
            END_NUM=$OPTARG
            ;;
        f)
            FOLDER_NUM=$OPTARG
            ;;
        h)
            show_usage
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            show_usage
            exit 1
            ;;
    esac
done

# Create target folder
TARGET_FOLDER="simulation_results${FOLDER_NUM}"
echo "Creating folder: $TARGET_FOLDER"
mkdir -p "$TARGET_FOLDER"

# Move simulation files (n0.h5 to n6.h5, or custom range)
echo "Moving simulation files from n${START_NUM}.h5 to n${END_NUM}.h5"
for ((i=START_NUM; i<=END_NUM; i++)); do
    FILENAME="openmc_simulation_n${i}.h5"
    if [ -f "$FILENAME" ]; then
        mv "$FILENAME" "$TARGET_FOLDER/"
        echo "Moved: $FILENAME"
    else
        echo "Warning: $FILENAME not found"
    fi
done

# Move other required files
OTHER_FILES=("summary.h5" "tallies.out" "settings.xml" "materials.xml" "geometry.xml")

echo "Moving other simulation files..."
for file in "${OTHER_FILES[@]}"; do
    if [ -f "$file" ]; then
        mv "$file" "$TARGET_FOLDER/"
        echo "Moved: $file"
    else
        echo "Warning: $file not found"
    fi
done

# Also check for statepoint file (common in OpenMC)
STATEPOINT_FILE="statepoint.50.h5"
if [ -f "$STATEPOINT_FILE" ]; then
    mv "$STATEPOINT_FILE" "$TARGET_FOLDER/"
    echo "Moved: $STATEPOINT_FILE"
fi

echo ""
echo "All files moved to $TARGET_FOLDER/"
echo "Files in $TARGET_FOLDER/:"
ls -la "$TARGET_FOLDER/"