#!/bin/bash

# Define paths
SRC_DIR="./src/fw_fanctrl/hardwareController/ectool"
LIB_NAME="libectool.so"
SOURCE_FILE="$SRC_DIR/ectool.c"
BUILD_OUTPUT="$SRC_DIR/$LIB_NAME"
SYSTEM_LIB_PATH="/usr/local/lib/$LIB_NAME"

# Ensure the source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Source file $SOURCE_FILE not found!"
    exit 1
fi

# Compile the shared library
echo "Compiling $SOURCE_FILE into $BUILD_OUTPUT..."
gcc -shared -o "$BUILD_OUTPUT" -fPIC "$SOURCE_FILE"

# Check if compilation succeeded
if [ $? -ne 0 ]; then
    echo "Error: Compilation failed!"
    exit 1
fi

echo "Compilation successful!"

# Copy to system-wide library directory
echo "Copying $BUILD_OUTPUT to $SYSTEM_LIB_PATH..."
sudo cp "$BUILD_OUTPUT" "$SYSTEM_LIB_PATH"

# Update the shared library cache
echo "Running ldconfig..."
sudo ldconfig

echo "Library successfully installed to $SYSTEM_LIB_PATH!"
