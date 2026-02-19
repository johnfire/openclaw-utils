# Security Tools

Security monitoring and advisory checking for OpenClaw.

## check-clawsec-advisories.sh

### Overview
Checks the ClawSec security advisory feed against your installed OpenClaw skills and alerts you to any vulnerabilities.

### Features
- **Advisory feed checking**: Regularly checks for new security advisories
- **Skill vulnerability scanning**: Compares advisories against installed skills
- **Severity filtering**: Focuses on critical and high severity vulnerabilities
- **State tracking**: Remembers which advisories you've already seen
- **Clear reporting**: Easy-to-read output with actionable recommendations

### How It Works
1. Fetches the latest ClawSec advisory feed
2. Filters for critical/high severity advisories
3. Checks if any advisories affect your installed skills
4. Reports findings and recommended actions
5. Saves state to avoid duplicate alerts

### Dependencies
```bash
# Debian/Ubuntu
sudo apt install curl jq

# macOS
brew install curl jq
```

### Setup
1. **Ensure clawsec-suite is installed**:
   The script expects the clawsec-suite skill to be installed at:
   `~/.openclaw/workspace/skills/clawsec-suite/`

2. **Make script executable**:
   ```bash
   chmod +x check-clawsec-advisories.sh
   ```

3. **Test run**:
   ```bash
   ./check-clawsec-advisories.sh
   ```

### Usage
```bash
# Manual check
./check-clawsec-advisories.sh

# Run with cron for automated monitoring
```

### Cron Job Example
```bash
# Run every 6 hours
0 */6 * * * cd /path/to/openclaw-utils/security && ./check-clawsec-advisories.sh

# Or integrate with OpenClaw's heartbeat system
# Add to your HEARTBEAT.md file
```

### Integration with OpenClaw
Add to your `HEARTBEAT.md`:
```markdown
## Security Checks
- Run `./check-clawsec-advisories.sh`
- Check for critical/high severity advisories affecting installed skills
- Report any matches immediately as security alerts
```

### Output Examples
- ✅ **Clean**: "No advisories affecting installed skills"
- ⚠️ **Warning**: "Skill X has vulnerability Y - update recommended"
- 🚨 **Alert**: "CRITICAL vulnerability in skill Z - remove immediately"

### State File
The script maintains state in:
`~/.openclaw/clawsec-suite-feed-state.json`

This tracks:
- Last feed version checked
- Last update timestamp  
- Which advisories have been seen

### Troubleshooting
- **"clawsec-suite not found"**: Install the clawsec-suite skill first
- **"curl/jq not found"**: Install dependencies as shown above
- **Permission errors**: Ensure script is executable

### Security Notes
- This tool only reads public advisory feeds
- No sensitive data is transmitted
- All checks happen locally on your machine
- Advisories are sourced from the official ClawSec repository

### Related Tools
Consider also using:
- **soul-guardian**: File integrity monitoring for OpenClaw workspace
- **System firewall rules**: Additional host-based security
- **Regular updates**: Keep OpenClaw and skills updated