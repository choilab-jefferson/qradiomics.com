#!/usr/bin/env bash
# Convert WordPress XML export to Hugo-compatible Markdown
# Run from migration/ directory after placing wordpress-export.xml here

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INPUT="$SCRIPT_DIR/wordpress-export.xml"
OUTPUT="$SCRIPT_DIR/output"

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: Place WordPress export XML at: $INPUT"
  exit 1
fi

rm -rf "$OUTPUT"
mkdir -p "$OUTPUT"

cd "$SCRIPT_DIR"

# wordpress-export-to-markdown options:
#   --input             : XML file path
#   --output            : output directory
#   --year-folders      : organize posts by year
#   --month-folders     : organize posts by month
#   --post-folders      : each post gets its own folder
#   --prefix-date       : prefix filename with publish date
#   --save-attached-images : download images attached to posts
#   --save-scraped-images  : download images linked in post body
#   --include-other-types  : include pages and custom post types
npx wordpress-export-to-markdown \
  --input="$INPUT" \
  --output="$OUTPUT" \
  --year-folders=false \
  --month-folders=false \
  --post-folders=true \
  --prefix-date=true \
  --save-attached-images=true \
  --save-scraped-images=true \
  --include-other-types=true \
  --timezone=America/New_York

echo ""
echo "==> Conversion complete. Output at: $OUTPUT"
echo "==> Next: review output, then run scripts/import-to-hugo.sh"
