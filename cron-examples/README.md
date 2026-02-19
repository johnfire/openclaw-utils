# Cron Job Examples

Scheduled task configurations for automating OpenClaw utilities.

## Overview
Cron jobs allow you to run scripts automatically at scheduled intervals. This directory contains examples for common OpenClaw automation tasks.

## Types of Cron Jobs

### 1. System Cron (Traditional)
Uses the system's cron daemon. Edit with `crontab -e`.

### 2. OpenClaw Cron Jobs
Uses OpenClaw's built-in cron system. More integrated with OpenClaw features.

### 3. Hybrid Approach
System cron triggers OpenClaw commands for more complex workflows.

## Example Files

### `system-updates.cron`
Automated system updates with OpenClaw notifications.

### `security-scan.cron`  
Regular security advisory checks.

### `token-monitor.cron`
Session token monitoring and alerts.

### `email-scanner.cron`
Email classification automation.

### `memory-archive.cron`
Scheduled memory archiving.

## Quick Start

### System Cron
```bash
# Edit your user's crontab
crontab -e

# Add a test job (runs every minute)
* * * * * echo "Test cron job" >> /tmp/cron-test.log
```

### OpenClaw Cron
```bash
# List existing OpenClaw cron jobs
openclaw cron list

# Add a new job
openclaw cron add --name "Test Job" --every 3600 --sessionTarget isolated --payload '{"kind":"agentTurn","message":"Do something"}'
```

## Best Practices

1. **Test manually first**: Always run scripts manually before automating
2. **Use absolute paths**: Cron has a limited PATH, use full paths to binaries
3. **Log everything**: Redirect output to log files for debugging
4. **Set reasonable intervals**: Don't overload your system
5. **Monitor job health**: Check logs regularly for failures
6. **Use meaningful names**: Helps identify jobs later
7. **Include error handling**: Scripts should handle failures gracefully
8. **Consider timezones**: Cron uses system timezone

## Troubleshooting

### Common Issues
- **Script doesn't run**: Check permissions and shebang (`#!/bin/bash`)
- **Environment variables missing**: Cron has minimal env, set them in script
- **Path issues**: Use absolute paths or set PATH at top of script
- **Permission errors**: Ensure user has necessary permissions
- **No output**: Redirect stderr and stdout to a log file

### Debugging Tips
```bash
# Check cron logs
sudo grep CRON /var/log/syslog

# Test with simplified command
* * * * * /path/to/script.sh >> /tmp/debug.log 2>&1

# Check script permissions
ls -la /path/to/script.sh
```

## Security Considerations
- **Limit privileges**: Don't run as root unless necessary
- **Validate inputs**: Especially for scripts that handle data
- **Secure credentials**: Use environment variables or config files
- **Audit regularly**: Review cron jobs periodically
- **Disable unused jobs**: Remove or comment out jobs no longer needed

## Integration Examples

### Combined Monitoring Job
A single cron job that runs multiple checks:
```bash
#!/bin/bash
# Run every hour
/path/to/security-check.sh
/path/to/token-monitor.py  
/path/to/system-check.sh
```

### Conditional Execution
Only run if certain conditions are met:
```bash
#!/bin/bash
# Only run during business hours
HOUR=$(date +%H)
if [ $HOUR -ge 9 ] && [ $HOUR -lt 17 ]; then
    /path/to/active-monitoring.sh
else
    /path/to/passive-monitoring.sh
fi
```

### OpenClaw Integration
System cron triggering OpenClaw commands:
```bash
#!/bin/bash
# System cron runs this script
# Script triggers OpenClaw action
/path/to/openclaw message send -m "Cron job completed at $(date)"
```

## Advanced Topics

### Lock Files
Prevent multiple instances from running:
```bash
#!/bin/bash
LOCKFILE="/tmp/myjob.lock"
if [ -f "$LOCKFILE" ]; then
    echo "Job already running" >> /tmp/job.log
    exit 1
fi
touch "$LOCKFILE"
# ... do work ...
rm "$LOCKFILE"
```

### Error Notification
Send alerts on failure:
```bash
#!/bin/bash
if ! /path/to/important-job.sh; then
    /path/to/openclaw message send -m "Job failed at $(date)"
    exit 1
fi
```

### Rotating Logs
Prevent log files from growing too large:
```bash
#!/bin/bash
LOG="/tmp/myjobs.log"
# Keep last 1000 lines
tail -1000 "$LOG" > "${LOG}.tmp" && mv "${LOG}.tmp" "$LOG"
echo "Job started: $(date)" >> "$LOG"
# ... do work ...
```

## Resources
- [Cron Guru](https://crontab.guru/) - Help with cron syntax
- [OpenClaw Cron Docs](https://docs.openclaw.ai/features/cron) - Official documentation
- [bash(1) man page](https://man7.org/linux/man-pages/man1/bash.1.html) - Shell reference