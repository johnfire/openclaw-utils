# Changelog

All notable changes to OpenClaw Utilities will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-19

### Added
- Initial release of OpenClaw Utilities collection
- **Email Automation**:
  - `unified_email_scanner_v2.py`: AI-powered email classification system
  - Learns from existing email folders to categorize incoming emails
  - Supports Proton Bridge and other IMAP servers
- **Security Tools**:
  - `check-clawsec-advisories.sh`: ClawSec security advisory scanner
  - Checks for vulnerabilities in installed OpenClaw skills
  - Reports critical/high severity advisories
- **Monitoring**:
  - `session_token_monitor.py`: Token usage monitor with alerts
  - Sends WhatsApp notifications when approaching token limits
  - Configurable warning and critical thresholds
- **Memory Management**:
  - `archive-memory.sh`: Memory archiving system for OpenClaw
  - Archives MEMORY.md to prevent context bloat
  - Searchable archive with timestamps and comments
- **Cron Examples**:
  - `system-updates.cron`: Automated system update configurations
  - `security-scan.cron`: Regular security check schedules
  - README with best practices and troubleshooting
- **Development Tools**:
  - `add-tool.sh`: Helper script for adding new tools to repository
  - Interactive prompts and automatic documentation generation
  - Git integration for easy commits and pushes
- **Documentation**:
  - Comprehensive README files for each tool
  - Setup instructions and configuration guides
  - Usage examples and integration tips
- **Project Structure**:
  - MIT License
  - Contributing guidelines
  - Git ignore configuration
  - Organized directory structure

### Technical Notes
- All tools designed to run locally on your OpenClaw instance
- No external dependencies beyond standard system tools
- Configuration via environment variables or script modification
- Designed for integration with OpenClaw's cron system

### Known Issues
- `session_token_monitor.py` has hardcoded paths (update before use)
- Email scanner requires manual configuration of IMAP credentials
- Some tools assume standard OpenClaw installation paths

### Next Steps Planned
- Create configuration file system for all tools
- Add more email classification categories
- Develop web interface for monitoring dashboard
- Add support for additional messaging platforms
- Create installation script for easy setup
- Make `session_token_monitor.py` paths configurable via environment variables