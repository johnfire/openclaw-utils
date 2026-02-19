#!/usr/bin/env python3
"""
Session Token Monitor
Checks if main session token usage exceeds threshold and triggers restart.
Run via cron job every 15 minutes.
"""

import subprocess
import re
import json
import os
from datetime import datetime

def get_session_status():
    """Get session status via OpenClaw CLI"""
    try:
        # Run openclaw status command
        cmd = ["/home/chris/.nvm/versions/node/v23.0.0/bin/openclaw", "status"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout
    except Exception as e:
        print(f"Error getting session status: {e}")
        return None

def parse_token_usage(status_text):
    """Parse token usage from status output"""
    if not status_text:
        return None
    
    # Look for main session in the table
    # Pattern: agent:main:main ... deepseek-chat │ 22k/200k (11%)
    lines = status_text.split('\n')
    for line in lines:
        if 'agent:main:main' in line and ('deepseek-chat' in line or 'deepseek' in line):
            # Extract token part - split by │ and get the last part before │
            parts = [p.strip() for p in line.split('│')]
            # Find the token part (looks like "22k/200k (11%)")
            for part in parts:
                if '/' in part and 'k' in part.lower() and '%' in part:
                    token_part = part
                    # token_part looks like: "22k/200k (11%)"
                    match = re.search(r'(\d+\.?\d*[kK]?)/(\d+\.?\d*[kK]?)\s*\((\d+)%\)', token_part)
                    if match:
                        current = match.group(1)
                        total = match.group(2)
                        percent = int(match.group(3))
                        
                        # Convert k suffix to thousands
                        def parse_k(value):
                            if 'k' in value.lower():
                                num = value.lower().replace('k', '')
                                if '.' in num:
                                    return int(float(num) * 1000)
                                return int(num) * 1000
                            return int(value)
                        
                        current_tokens = parse_k(current)
                        total_tokens = parse_k(total)
                        
                        return {
                            'current': current_tokens,
                            'total': total_tokens,
                            'percent': percent,
                            'raw': token_part
                        }
    
    return None

def send_whatsapp_message(message):
    """Send WhatsApp message"""
    try:
        cmd = [
            "/home/chris/.nvm/versions/node/v23.0.0/bin/openclaw",
            "message", "send",
            "--channel", "whatsapp",
            "-t", "+4917682060154",
            "-m", message
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        print(f"Message sent, return code: {result.returncode}")
        if result.stdout:
            print(f"Stdout: {result.stdout[:200]}")
        if result.stderr:
            print(f"Stderr: {result.stderr[:200]}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def send_restart_notification(token_info):
    """Send notification that session needs restart"""
    message = f"⚠️ High token usage detected: {token_info['raw']} (>125k). Please say 'new session' to restart."
    return send_whatsapp_message(message)

def main():
    print(f"Session Token Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get status
    status = get_session_status()
    if not status:
        print("Failed to get session status")
        return
    
    print(f"Status output length: {len(status)} chars")
    
    # Parse token usage
    tokens = parse_token_usage(status)
    if not tokens:
        print("Could not parse token usage from status")
        return
    
    print(f"Token usage: {tokens['current']}/{tokens['total']} ({tokens['percent']}%)")
    
    # Check threshold (125k)
    threshold = 125000
    if tokens['current'] > threshold:
        print(f"⚠️ EXCEEDED THRESHOLD: {tokens['current']} > {threshold}")
        send_restart_notification(tokens)
        
        # Also write to a log file
        with open("/home/chris/.openclaw/workspace/session_restart_log.txt", "a") as f:
            f.write(f"{datetime.now().isoformat()}: High token usage {tokens['current']}/{tokens['total']}. Alert sent.\n")
    else:
        print(f"✓ Below threshold: {tokens['current']} <= {threshold}")
        
        # Send simplified status message
        message = f"TM: {tokens['percent']}%"
        send_whatsapp_message(message)
        
        # Log normal operation
        with open("/home/chris/.openclaw/workspace/session_restart_log.txt", "a") as f:
            f.write(f"{datetime.now().isoformat()}: Normal token usage {tokens['current']}/{tokens['total']}. Status sent.\n")

if __name__ == "__main__":
    main()