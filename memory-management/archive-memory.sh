#!/bin/bash
# Memory Archiving Script
# Use: ./archive-memory.sh [comment]

echo "📚 Memory Archiving Tool"
echo "========================"
echo ""

DATE=$(date '+%Y-%m-%d %H:%M CET')
COMMENT="${1:-routine archive}"

echo "📅 Archive date: $DATE"
echo "📝 Comment: $COMMENT"
echo ""

# Check if MEMORY.md exists
if [ ! -f "MEMORY.md" ]; then
    echo "❌ Error: MEMORY.md not found!"
    exit 1
fi

# Count lines in MEMORY.md
LINES=$(wc -l < MEMORY.md)
echo "📊 MEMORY.md has $LINES lines"

# Archive threshold warning
if [ $LINES -gt 500 ]; then
    echo "⚠️  Warning: MEMORY.md is getting large (>500 lines)"
    echo "   Consider clearing/trimming after archiving"
fi

echo ""
echo "📋 Archiving process:"
echo "1. Reading current MEMORY.md..."
echo "2. Appending to MEMORY_ARCHIVE.md..."
echo "3. Adding timestamp and comment..."
echo ""

# Create archive entry
ARCHIVE_ENTRY="\n\n---\n\n## Archive Entry: $DATE\n**Comment:** $COMMENT\n\n$(cat MEMORY.md)"

# Append to archive
echo -e "$ARCHIVE_ENTRY" >> MEMORY_ARCHIVE.md

# Count archive lines
ARCHIVE_LINES=$(wc -l < MEMORY_ARCHIVE.md)

echo "✅ Archive complete!"
echo "📁 MEMORY_ARCHIVE.md now has $ARCHIVE_LINES lines"
echo ""
echo "📋 Next steps:"
echo "   - Review MEMORY.md and consider clearing/trimming"
echo "   - Use 'grep' to search the archive when needed"
echo "   - Archive again when MEMORY.md gets large"
echo ""
echo "🔍 Quick search examples:"
echo "   grep -i 'email' MEMORY_ARCHIVE.md"
echo "   grep -i 'gpu' MEMORY_ARCHIVE.md"
echo "   grep '2026-02' MEMORY_ARCHIVE.md"