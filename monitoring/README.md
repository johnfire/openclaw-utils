# Monitoring Tools

Token usage monitoring and performance tracking for OpenClaw.

## session_token_monitor.py

### Overview
Monitors OpenClaw session token usage and sends alerts when approaching context limits. Helps prevent session timeouts and maintain optimal performance.

### Features
- **Real-time monitoring**: Checks token usage via OpenClaw CLI
- **Smart thresholds**: Alerts at configurable warning and critical levels
- **Multiple notification methods**: WhatsApp alerts with customizable messages
- **Logging**: Detailed logs for troubleshooting and historical tracking
- **Cron-ready**: Designed to run as a scheduled task

### Why Monitor Tokens?
OpenClaw has a context window limit (typically 200k tokens). When this limit is approached:
- Responses slow down
- Memory becomes fragmented
- Session may become unstable
- Best practice: Start a new session before hitting limits

### Dependencies
```bash
# Python 3.x
python3 --version

# OpenClaw CLI
openclaw --version
```

### Configuration
1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file**:
   ```env
   # OpenClaw binary path (find with: which openclaw)
   OPENCLAW_PATH="/usr/local/bin/openclaw"
   
   # WhatsApp number for alerts
   ALERT_NUMBER="+1234567890"
   
   # Token thresholds (in thousands)
   WARNING_THRESHOLD=100  # 100k tokens
   ALERT_THRESHOLD=125    # 125k tokens
   MAX_TOKENS=200         # 200k tokens
   ```

3. **Make script executable**:
   ```bash
   chmod +x session_token_monitor.py
   ```

### Important Note
**⚠️ Before first use:**  
The current version has hardcoded paths and phone numbers. You MUST edit the script to:
1. Update the OpenClaw binary path (line with `"/home/chris/.nvm/versions/node/v23.0.0/bin/openclaw"`)
2. Update the WhatsApp number (line with `"+4917682060154"`)
3. Adjust thresholds as needed

A future version will read from the `.env` file.

### Usage
```bash
# Manual check
python3 session_token_monitor.py

# Test with verbose output
python3 session_token_monitor.py --verbose

# Run once and exit (for cron)
python3 session_token_monitor.py --once
```

### Cron Job Examples
```bash
# Every 15 minutes
*/15 * * * * cd /path/to/openclaw-utils/monitoring && python3 session_token_monitor.py

# Every hour during working hours
0 9-17 * * 1-5 cd /path && python3 session_token_monitor.py
```

### OpenClaw Cron Integration
You can also create an OpenClaw cron job:
```json
{
  "name": "Session Token Monitor",
  "schedule": "every 15 minutes",
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Check token usage and alert if >125k"
  }
}
```

### Alert Examples
- **Warning**: "⚠️ High token usage detected: 112k/200k (56%). Consider 'new session' command."
- **Critical**: "🚨 CRITICAL: Token usage very high: 185k/200k (92%). Send 'new session' immediately!"

### Log Files
- **Session logs**: `/tmp/openclaw_token_monitor.log`
- **Alert history**: `~/.openclaw/workspace/session_restart_log.txt`

### Troubleshooting
- **"Command not found: openclaw"**: Update the OPENCLAW_PATH in the script
- **No alerts sent**: Check WhatsApp configuration and number format
- **Incorrect token counts**: The parser may need adjustment for your OpenClaw version

### Best Practices
1. Set warning threshold at 50-60% of max tokens
2. Set critical threshold at 75-80% of max tokens  
3. Run checks every 15-30 minutes during active use
4. Review logs weekly to understand usage patterns
5. Consider lowering thresholds if you experience slowdowns

### Related Tools
- **OpenClaw's built-in `/status` command**: Quick manual checks
- **Heartbeat monitoring**: Integrate with your HEARTBEAT.md
- **Memory archiving**: Use with archive-memory.sh to manage context
---

## test-demo
