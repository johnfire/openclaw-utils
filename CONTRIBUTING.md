# Contributing to OpenClaw Utilities

Thank you for considering contributing to OpenClaw Utilities! This project aims to build a collection of useful tools for the OpenClaw community.

## How to Contribute

### 1. Report Issues
Found a bug or have a feature request? Please:
- Check if the issue already exists
- Use the issue templates if available
- Provide as much detail as possible
- Include steps to reproduce (for bugs)

### 2. Submit Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test your changes
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

### 3. Improve Documentation
- Fix typos or unclear explanations
- Add examples
- Improve README files
- Translate documentation

## Development Setup

### Prerequisites
- OpenClaw installed and running
- Git
- Python 3.x (for Python scripts)
- Bash (for shell scripts)

### Local Setup
```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/openclaw-utils.git
cd openclaw-utils

# Add upstream remote
git remote add upstream https://github.com/johnfire/openclaw-utils.git
```

## Code Guidelines

### General
- Keep scripts simple and focused
- Use clear, descriptive names
- Include comments for complex logic
- Follow existing code style

### Shell Scripts
- Use `#!/bin/bash` shebang
- Set `-e` for error handling (if appropriate)
- Quote variables: `"$variable"`
- Use `[[ ]]` for conditionals in bash
- Include a header comment with purpose

### Python Scripts
- Use Python 3.x
- Follow PEP 8 style guide
- Include docstrings for functions
- Use type hints where helpful
- Handle exceptions gracefully

### Documentation
- Each tool should have its own README.md
- Include setup instructions
- Provide usage examples
- Document configuration options
- Note any dependencies

## Project Structure

```
openclaw-utils/
├── email-automation/     # Email classification tools
├── security/            # Security scanning tools
├── monitoring/          # Performance monitoring
├── memory-management/   # Memory archiving tools
├── cron-examples/       # Automation configurations
└── docs/               # Additional documentation
```

## Adding New Tools

1. Create a new directory for your tool category (or use existing)
2. Include:
   - The main script(s)
   - README.md with documentation
   - Configuration examples
   - Test files (if applicable)
3. Update the main README.md to list your tool
4. Consider adding cron examples if applicable

## Testing

- Test scripts manually before submitting
- Include test instructions in README
- Consider edge cases and error handling
- Test on different systems if possible

## Security Considerations

- Never commit secrets or credentials
- Use environment variables for configuration
- Validate user input in scripts
- Consider security implications of new features
- Document any security requirements

## Code Review Process

1. Pull Requests will be reviewed by maintainers
2. Feedback will be provided within a few days
3. Changes may be requested before merging
4. All contributions must pass basic checks

## Questions?

- Open an issue for questions
- Check existing documentation first
- Be respectful and patient

## Recognition

Contributors will be acknowledged in:
- The README.md file
- Release notes
- Project documentation

Thank you for helping build better tools for the OpenClaw community! 🚀