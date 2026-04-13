#!/bin/bash
# Cleanup script for AGT Navigation Stack

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE="${SCRIPT_DIR}/../agt_ws"

echo "Cleaning AGT workspace..."

cd "$WORKSPACE"

# Remove build artifacts
rm -rf build/
rm -rf install/
rm -rf log/

echo "✓ Cleanup complete"
echo ""
echo "To rebuild, run:"
echo "  cd $WORKSPACE"
echo "  colcon build --symlink-install"
