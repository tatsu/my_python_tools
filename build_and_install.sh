#!/bin/bash

# Exit on error
set -e

# Define output directory
BIN_DIR="$HOME/bin"

# Ensure bin directory exists
mkdir -p "$BIN_DIR"

# Clean up previous build artifacts
rm -rf build/ dist/ *.spec

# Loop through all .py files in the current directory
for pyfile in ./*.py; do
    # Skip if no .py files found
    [ -e "$pyfile" ] || continue

    # Extract base name without extension
    name=$(basename "$pyfile" .py)

    echo "🔧 Building $name from $pyfile..."

    # Create binary with PyInstaller
    pyinstaller --onefile --clean --name "$name" "$pyfile"

    # Move binary to ~/bin
    cp "dist/$name" "$BIN_DIR/"
    chmod +x "$BIN_DIR/$name"

    echo "✅ Installed $name to $BIN_DIR"
done

# Clean up build directories
rm -rf build/ dist/ *.spec

echo "🎉 All binaries built and installed to $BIN_DIR"
