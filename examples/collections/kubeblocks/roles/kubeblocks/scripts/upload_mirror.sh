#!/bin/bash

# Recursive upload script for Helm chart mirror created by download_charts.py
# Usage: ./upload_mirror.sh <local_directory>

set -e  # Exit on error

# Get credentials from ansible-vault
eval "$(ansible-vault view ~/.filerepo)"

# Configuration
LOCAL_DIR="${1:-helm-charts}"
BASE_URL="${BASE_URL}"  # From ansible-vault

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL=0
SUCCESS=0
FAILED=0

echo "=========================================="
echo "Helm Chart Mirror Upload"
echo "=========================================="
echo "Local directory: $LOCAL_DIR"
echo "Base URL: $BASE_URL"
echo ""

# Check if directory exists
if [ ! -d "$LOCAL_DIR" ]; then
    echo -e "${RED}Error: Directory $LOCAL_DIR does not exist${NC}"
    exit 1
fi

# Find all .tgz files recursively
echo "Finding chart files..."
FILES=$(find "$LOCAL_DIR" -type f -name "*.tgz")
TOTAL=$(echo "$FILES" | wc -l)

echo -e "Found ${YELLOW}${TOTAL}${NC} chart file(s) to upload"
echo ""

# Upload each file
CURRENT=0
while IFS= read -r filepath; do
    CURRENT=$((CURRENT + 1))

    # Extract relative path from local directory
    RELATIVE_PATH="${filepath#$LOCAL_DIR/}"

    # Extract directory and filename
    DIR_NAME=$(dirname "$RELATIVE_PATH")
    FILE_NAME=$(basename "$RELATIVE_PATH")

    # If file is in root, DIR_NAME will be ".", handle this
    if [ "$DIR_NAME" = "." ]; then
        UPLOAD_URL="$BASE_URL/$FILE_NAME"
    else
        UPLOAD_URL="$BASE_URL/$DIR_NAME/$FILE_NAME"
    fi

    echo -e "[${CURRENT}/${TOTAL}] Uploading: ${YELLOW}${RELATIVE_PATH}${NC}"
    echo "  → $UPLOAD_URL"

    # Upload with curl
    HTTP_CODE=$(curl -u "$USERNAME:$PASSWORD" \
                     -T "$filepath" \
                     "$UPLOAD_URL" \
                     -w "%{http_code}" \
                     -o /dev/null \
                     -s \
                     --create-dirs)

    # Check HTTP response code
    if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
        echo -e "  ${GREEN}✓ Success (HTTP $HTTP_CODE)${NC}"
        SUCCESS=$((SUCCESS + 1))
    else
        echo -e "  ${RED}✗ Failed (HTTP $HTTP_CODE)${NC}"
        FAILED=$((FAILED + 1))
    fi
    echo ""

done <<< "$FILES"

# Summary
echo "=========================================="
echo "Upload Summary"
echo "=========================================="
echo -e "Total files:    ${TOTAL}"
echo -e "Successful:     ${GREEN}${SUCCESS}${NC}"
echo -e "Failed:         ${RED}${FAILED}${NC}"
echo "=========================================="

# Exit with error if any uploads failed
if [ "$FAILED" -gt 0 ]; then
    exit 1
fi
