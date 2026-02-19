# OpenClaw Utilities

A collection of useful scripts and tools for OpenClaw, the personal AI assistant platform.

## 📦 What's Included

### 📧 Email Automation
- **`unified_email_scanner_v2.py`** - AI-powered email classification system that learns from your existing email folders to automatically categorize incoming emails (rejections, confirmations, requests for more info, etc.)

### 🔒 Security Tools
- **`check-clawsec-advisories.sh`** - Security advisory scanner that checks the ClawSec advisory feed against your installed OpenClaw skills

### 📊 Monitoring & Performance
- **`session_token_monitor.py`** - Token usage monitor that alerts you when session context approaches limits
- **Cron job examples** - Scheduled task configurations for automated monitoring

### 🧠 Memory Management
- **`archive-memory.sh`** - Memory archiving system for OpenClaw's MEMORY.md file with automatic timestamping and search capabilities

### 🔧 Development Tools
- **`add-tool.sh`** - Helper script for adding new tools to the repository with interactive prompts and automatic documentation

## 🚀 Getting Started

### Prerequisites
- OpenClaw installed and running
- GitHub CLI (`gh`) for some scripts
- Python 3.x for Python scripts
- Basic shell access

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/johnfire/openclaw-utils.git
   cd openclaw-utils
   ```

2. Review each tool's README for specific setup instructions

## 🛠️ Tool Details

### Email Scanner
The email scanner connects to your IMAP server (like Proton Mail Bridge) and:
- Learns from existing email folders
- Classifies new emails based on content
- Can automatically move emails to appropriate folders
- Uses machine learning to improve over time

### Security Advisor
Regularly checks for:
- Security advisories from the ClawSec feed
- Vulnerabilities in installed OpenClaw skills
- Version compatibility issues

### Token Monitor
Helps prevent session timeouts by:
- Monitoring token usage in real-time
- Sending alerts when approaching limits
- Suggesting when to start a new session

### Memory Archiver
Manages OpenClaw's memory system by:
- Archiving old memories to prevent context bloat
- Maintaining searchable history
- Providing clean memory management workflows

### Development Helper
Simplifies adding new tools to the collection by:
- Interactive prompts for tool details
- Automatic file copying and organization
- README template generation
- Git integration for easy commits

## ⚙️ Configuration

Most tools require configuration. See each tool's directory for:
- `.env.example` files
- Configuration templates
- Setup instructions

## 🤝 Contributing

Feel free to submit issues and pull requests! This is an open collection of tools that can benefit the OpenClaw community.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built for [OpenClaw](https://openclaw.ai)
- Inspired by real-world automation needs
- Community-driven tool development