# Email Automation

AI-powered email classification system for OpenClaw.

## unified_email_scanner_v2.py

### Features
- **Learning-based classification**: Trains from your existing email folders
- **Employment email focus**: Classifies job application rejections, confirmations, and requests for more information
- **Modular design**: Easy to add new email categories (coupons, newsletters, etc.)
- **Confidence scoring**: Only routes emails when classification confidence is high (>60%)
- **IMAP support**: Works with any IMAP server including Proton Mail Bridge

### How It Works
1. **Training Phase**: Scans your existing email folders to learn patterns
2. **Classification**: Analyzes new emails based on subject and content
3. **Routing**: Moves emails to appropriate folders based on classification
4. **Continuous Learning**: Can be retrained as your email patterns change

### Setup
1. **Install dependencies**:
   ```bash
   pip3 install imaplib2 email python-dotenv
   ```

2. **Configure credentials**:
   Create `~/.config/openclaw/proton_bridge.env`:
   ```env
   EMAIL_ADDR="your-email@example.com"
   PASSWORD="your-imap-password"
   ```

3. **Configure training folders**:
   Edit the `EMPLOYMENT_TRAINING_FOLDERS` section in the script to point to your existing email folders.

4. **Configure output folders**:
   Edit the `OUTPUT_FOLDERS` section to specify where classified emails should go.

### Usage
```bash
python3 unified_email_scanner_v2.py
```

### Cron Job Example
```bash
# Run every 30 minutes
*/30 * * * * cd /path/to/openclaw-utils/email-automation && python3 unified_email_scanner_v2.py
```

### Output Folders
- **Rejections**: `Folders/0 - AI/0 AI - Jobs/ToBeChecked - R`
- **Confirmations**: Left in INBOX (for manual review)
- **More info needed**: Left in INBOX (for follow-up)
- **Unknown**: Left in INBOX (manual classification needed)

### Training Data
The classifier needs at least:
- 20+ rejection emails
- 20+ confirmation emails  
- 10+ "more info needed" emails

More training data = better accuracy.

### Customization
To add new email categories:
1. Add new training folders to `EMPLOYMENT_TRAINING_FOLDERS`
2. Add corresponding output folders to `OUTPUT_FOLDERS`
3. Retrain the classifier

### Troubleshooting
- **Connection issues**: Check your IMAP server settings and credentials
- **Low accuracy**: Add more training emails to each folder
- **Permission errors**: Ensure you have proper folder access rights

### Notes
- This tool respects email privacy - all processing happens locally
- No emails are sent or shared externally
- Classification is based only on email content you already have access to