# Memory Management

Tools for managing OpenClaw's memory system and preventing context bloat.

## archive-memory.sh

### Overview
Archives OpenClaw's MEMORY.md file to a permanent archive, allowing you to clear active memory while preserving important information. Essential for maintaining performance and managing long-term knowledge.

### Features
- **Safe archiving**: Appends current memory to permanent archive with timestamps
- **Automatic size checking**: Warns when MEMORY.md gets too large (>500 lines)
- **Searchable history**: Creates structured archive with clear section markers
- **Non-destructive**: Only archives, never deletes (unless you choose to clear MEMORY.md)
- **Easy search**: Provides grep examples for finding archived information

### Why Archive Memory?
OpenClaw uses three memory tiers:
1. **Daily notes**: `memory/YYYY-MM-DD.md` - Raw session logs
2. **Active memory**: `MEMORY.md` - Curated memories (loaded each session)
3. **Historical archive**: `MEMORY_ARCHIVE.md` - Permanent backup

When MEMORY.md gets large:
- Session context becomes bloated
- Responses slow down
- Token usage increases
- Time to archive and start fresh!

### Dependencies
```bash
# Basic bash tools (available on most systems)
bash --version
```

### Setup
1. **Make script executable**:
   ```bash
   chmod +x archive-memory.sh
   ```

2. **Navigate to your OpenClaw workspace**:
   ```bash
   cd ~/.openclaw/workspace
   ```

3. **Ensure MEMORY.md exists**:
   ```bash
   touch MEMORY.md
   ```

### Usage
```bash
# Basic archive (uses default "routine archive" comment)
./archive-memory.sh

# Archive with custom comment
./archive-memory.sh "Before starting new project"

# Archive before clearing memory
./archive-memory.sh "Pre-clearing archive" && echo "" > MEMORY.md
```

### Examples
```bash
# Archive weekly on Mondays
0 9 * * 1 cd ~/.openclaw/workspace && ./archive-memory.sh "Weekly Monday archive"

# Archive when MEMORY.md gets large
cd ~/.openclaw/workspace
if [ $(wc -l < MEMORY.md) -gt 300 ]; then
    ./archive-memory.sh "Large memory cleanup"
fi

# Archive as part of "new session" workflow
./archive-memory.sh "Before new session" && echo "new session"
```

### Archive Format
```
---

## Archive Entry: 2026-02-19 11:30 CET
**Comment:** Routine archive

[Previous MEMORY.md contents here]
```

### Searching Archives
```bash
# Search for specific terms
grep -i "email" MEMORY_ARCHIVE.md
grep -i "gpu" MEMORY_ARCHIVE.md
grep "2026-02" MEMORY_ARCHIVE.md

# Case-insensitive search with context
grep -i -B2 -A2 "security" MEMORY_ARCHIVE.md

# Count occurrences
grep -c "TODO" MEMORY_ARCHIVE.md
```

### Integration with OpenClaw Workflow

#### Heartbeat Integration
Add to your `HEARTBEAT.md`:
```markdown
## Memory Maintenance
- Check MEMORY.md size: if >500 lines, suggest archiving
- Run archive-memory.sh if user approves
- Clear MEMORY.md after successful archive
```

#### "New Session" Command
When user says "new session":
1. Archive current memory
2. Clear MEMORY.md  
3. Start fresh session

#### Cron Automation
```bash
# Archive every Sunday at midnight
0 0 * * 0 cd ~/.openclaw/workspace && ./archive-memory.sh "Weekly automated archive"

# Archive on the 1st of every month
0 0 1 * * cd ~/.openclaw/workspace && ./archive-memory.sh "Monthly archive"
```

### Best Practices
1. **Archive regularly**: Weekly or when MEMORY.md exceeds 300-500 lines
2. **Use descriptive comments**: Helps when searching archives later
3. **Clear after archiving**: Consider clearing MEMORY.md after archiving to start fresh
4. **Search before asking**: Check archives before asking about historical information
5. **Keep archives manageable**: Very large MEMORY_ARCHIVE.md files can be split by date

### Troubleshooting
- **"MEMORY.md not found"**: Run from OpenClaw workspace directory
- **Permission denied**: Make script executable with `chmod +x`
- **Archive too large**: Consider splitting MEMORY_ARCHIVE.md by year
- **Search not finding**: Use case-insensitive grep (`-i`) or check spelling

### Advanced Usage
```bash
# Archive and clear in one command
./archive-memory.sh && echo "" > MEMORY.md

# Archive and notify via OpenClaw
./archive-memory.sh "Automated archive" && openclaw message send -m "Memory archived successfully"

# Archive with line count in comment
LINES=$(wc -l < MEMORY.md)
./archive-memory.sh "Archiving ${LINES} lines before clearing"
```

### Related Concepts
- **OpenClaw memory system**: Understand the three-tier approach
- **Token management**: Archived memory reduces context size
- **Session management**: Fresh sessions after clearing memory
- **Knowledge persistence**: Archives preserve important learnings