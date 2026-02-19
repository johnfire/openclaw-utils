#!/bin/bash
# Simple ClawSec advisory check script

echo "🔒 ClawSec Security Advisory Check"
echo "=================================="
echo ""

INSTALL_ROOT="$HOME/.openclaw/workspace/skills"
SUITE_DIR="$INSTALL_ROOT/clawsec-suite"
STATE_FILE="$HOME/.openclaw/clawsec-suite-feed-state.json"

echo "📁 Suite directory: $SUITE_DIR"
echo "📄 State file: $STATE_FILE"
echo ""

# Check if suite is installed
if [ ! -d "$SUITE_DIR" ]; then
    echo "❌ ERROR: clawsec-suite not found at $SUITE_DIR"
    exit 1
fi

# Check for curl and jq
command -v curl >/dev/null 2>&1 || { echo "❌ ERROR: curl not found"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "❌ ERROR: jq not found"; exit 1; }

echo "✅ Dependencies: curl, jq available"
echo ""

# Check advisory feed
FEED_URL="https://raw.githubusercontent.com/prompt-security/clawsec/main/advisories/feed.json"
echo "📡 Checking advisory feed: $FEED_URL"

FEED_TMP=$(mktemp)
if curl -fsSL "$FEED_URL" -o "$FEED_TMP"; then
    FEED_VERSION=$(jq -r '.version // "unknown"' "$FEED_TMP")
    FEED_UPDATED=$(jq -r '.updated // "unknown"' "$FEED_TMP")
    ADVISORY_COUNT=$(jq -r '.advisories | length' "$FEED_TMP")
    
    echo "✅ Feed version: $FEED_VERSION"
    echo "📅 Last updated: $FEED_UPDATED"
    echo "📊 Total advisories: $ADVISORY_COUNT"
    echo ""
    
    # Check for critical/high advisories
    echo "🔍 Checking for critical/high severity advisories:"
    jq -r '.advisories[] | select(.severity == "critical" or .severity == "high") | "- [\(.severity)] \(.id): \(.title)"' "$FEED_TMP"
    
    # Check installed skills against advisories
    echo ""
    echo "🔧 Checking installed skills against advisories:"
    for skill_path in "$INSTALL_ROOT"/*; do
        [ -d "$skill_path" ] || continue
        skill_name=$(basename "$skill_path")
        
        # Skip clawsec-suite itself
        [ "$skill_name" = "clawsec-suite" ] && continue
        
        skill_hits=$(jq -r --arg skill_prefix "${skill_name}@" \
            '[.advisories[]
            | select(any(.affected[]?; startswith($skill_prefix)))
            | "  - [\(.severity)] \(.id): \(.title)"
            ] | .[]?' "$FEED_TMP")
        
        if [ -n "$skill_hits" ]; then
            echo "⚠️  $skill_name is referenced in advisories:"
            echo "$skill_hits"
        fi
    done
    
    rm "$FEED_TMP"
else
    echo "❌ ERROR: Failed to fetch advisory feed"
    exit 1
fi

echo ""
echo "✅ Advisory check complete"
echo ""
echo "📋 Next steps:"
echo "   - Review any advisories affecting installed skills"
echo "   - Check HEARTBEAT.md for automated monitoring"
echo "   - Run soul-guardian check for file integrity"