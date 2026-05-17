#!/usr/bin/env bash
# Convert WordPress XML export to Hugo-compatible Markdown
# Run from migration/ directory after placing wordpress-export.xml here

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT="$SCRIPT_DIR/wordpress-export.xml"
OUTPUT="$SCRIPT_DIR/output"

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: Place WordPress export XML at: $INPUT"
  exit 1
fi

rm -rf "$OUTPUT"
mkdir -p "$OUTPUT"

cd "$SCRIPT_DIR"

npx wordpress-export-to-markdown \
  --wizard=false \
  --input="$INPUT" \
  --output="$OUTPUT" \
  --post-folders=true \
  --prefix-date=true \
  --date-folders=none \
  --save-images=all \
  --timezone=America/New_York \
  --include-time=true \
  --quote-date=true \
  --request-delay=300

echo ""
echo "==> Conversion complete. Output at: $OUTPUT"
