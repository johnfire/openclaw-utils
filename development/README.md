# Development Tools

Tools for developing and maintaining the OpenClaw Utilities repository.

## add-tool.sh

Helper script for adding new tools to the repository.

### Features
- **Interactive mode**: Guided process for adding tools
- **Category management**: Organized placement in appropriate directories
- **File copying**: Copies files from workspace to repository
- **README generation**: Creates template documentation
- **Git integration**: Automates commit and push operations

### Usage

#### Interactive Mode
```bash
cd /path/to/openclaw-utils
./development/add-tool.sh --interactive
```

#### Command Line Mode
```bash
cd /path/to/openclaw-utils
./development/add-tool.sh \
  -n "tool-name" \
  -c "category" \
  -f "file1.sh file2.py" \
  -d "Description of the tool"
```

### Examples

```bash
# Add a monitoring tool
./development/add-tool.sh \
  -n "disk-monitor" \
  -c "monitoring" \
  -f "check-disk.sh disk-alerts.py" \
  -d "Monitors disk usage and sends alerts"

# Add a security tool interactively
./development/add-tool.sh --interactive
```

### Available Categories
- `email-automation` - Email classification and processing tools
- `security` - Security scanning and advisory tools
- `monitoring` - Performance and token monitoring tools
- `memory-management` - Memory archiving and management tools
- `cron-examples` - Automation configuration examples
- `docs` - Documentation and guides
- `development` - Repository development tools (this category)

### Workflow

1. **Develop tool** in your OpenClaw workspace
2. **Test thoroughly** before adding to repository
3. **Run add-tool.sh** to copy and document
4. **Review generated README** and update as needed
5. **Update main README.md** if adding new category
6. **Push to GitHub** to share with community

### Notes

- Files are copied from `~/home/chris/.openclaw/workspace/` by default
- Update the `WORKSPACE_ROOT` variable in the script if your workspace is elsewhere
- Generated READMEs are templates - update with actual usage instructions
- Main README.md may need manual updating for new categories

### Customization

Edit the script to:
- Change default workspace path
- Add new categories
- Modify README templates
- Adjust git commit messages
- Add pre-commit checks

### Best Practices

1. **Test before adding**: Ensure tools work correctly
2. **Document thoroughly**: Update generated README with actual instructions
3. **Use meaningful names**: Clear, descriptive tool names
4. **Organize by category**: Keep repository structure clean
5. **Follow existing patterns**: Maintain consistency with other tools
6. **Update CHANGELOG.md**: Document new additions

### Troubleshooting

- **"File not found"**: Check `WORKSPACE_ROOT` path in script
- **"Invalid category"**: Use one of the predefined categories or add new one
- **Git errors**: Ensure you have write access to repository
- **Permission errors**: Make scripts executable with `chmod +x`

### Related Tools

- **Git**: Version control system
- **GitHub CLI**: For repository management
- **OpenClaw CLI**: For testing tools in context