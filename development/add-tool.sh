#!/bin/bash
# add-tool.sh - Helper script to add new tools to OpenClaw Utilities repository
# Usage: ./add-tool.sh [tool-name] [category] [file1] [file2] ...

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
WORKSPACE_ROOT="/home/chris/.openclaw/workspace"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MAIN_README="$REPO_ROOT/README.md"

# Available categories
CATEGORIES=("email-automation" "security" "monitoring" "memory-management" "cron-examples" "docs" "development")

print_usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -n, --name TOOL_NAME      Name of the tool (required)"
    echo "  -c, --category CATEGORY   Category: ${CATEGORIES[*]} (required)"
    echo "  -f, --files FILES         Files to add (space-separated)"
    echo "  -d, --description DESC    Brief description of the tool"
    echo "  -i, --interactive         Interactive mode"
    echo "  -h, --help                Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 -n \"my-tool\" -c monitoring -f script.py config.json"
    echo "  $0 --interactive"
    echo ""
}

print_error() {
    echo -e "${RED}Error: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_info() {
    echo -e "${BLUE}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}Warning: $1${NC}"
}

validate_category() {
    local category="$1"
    for valid in "${CATEGORIES[@]}"; do
        if [[ "$valid" == "$category" ]]; then
            return 0
        fi
    done
    return 1
}

create_category_directory() {
    local category="$1"
    if [[ ! -d "$category" ]]; then
        print_info "Creating category directory: $category"
        mkdir -p "$category"
    fi
}

copy_files() {
    local category="$1"
    shift
    local files=("$@")
    
    for file in "${files[@]}"; do
        local source_file="$WORKSPACE_ROOT/$file"
        local dest_file="$REPO_ROOT/$category/$(basename "$file")"
        
        if [[ ! -f "$source_file" ]]; then
            print_error "File not found in workspace: $file"
            print_info "Looking in: $source_file"
            return 1
        fi
        
        print_info "Copying: $file → $category/"
        cp "$source_file" "$dest_file"
        
        # Make executable if it's a script
        if [[ "$file" == *.sh ]] || [[ "$file" == *.py ]]; then
            chmod +x "$dest_file"
        fi
    done
}

generate_readme() {
    local category="$1"
    local tool_name="$2"
    local description="$3"
    local readme_file="$REPO_ROOT/$category/README.md"
    
    # Check if README already exists
    if [[ -f "$readme_file" ]]; then
        print_warning "README.md already exists in $category/. Appending new tool."
        echo -e "\n---\n" >> "$readme_file"
        echo "## $tool_name" >> "$readme_file"
    else
        print_info "Creating README.md for $category/"
        echo "# $(echo "$category" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')" > "$readme_file"
        echo "" >> "$readme_file"
        echo "$description" >> "$readme_file"
        echo "" >> "$readme_file"
    fi
    
    # Add tool section
    if [[ -f "$readme_file" ]] && ! grep -q "## $tool_name" "$readme_file"; then
        echo "## $tool_name" >> "$readme_file"
        echo "" >> "$readme_file"
        echo "**Description:** $description" >> "$readme_file"
        echo "" >> "$readme_file"
        echo "### Files" >> "$readme_file"
        echo "" >> "$readme_file"
        
        # List files in category
        for file in "$REPO_ROOT/$category"/*; do
            if [[ -f "$file" ]] && [[ "$(basename "$file")" != "README.md" ]]; then
                echo "- \`$(basename "$file")\`" >> "$readme_file"
            fi
        done
        
        echo "" >> "$readme_file"
        echo "### Setup" >> "$readme_file"
        echo "" >> "$readme_file"
        echo "Add setup instructions here..." >> "$readme_file"
        echo "" >> "$readme_file"
        echo "### Usage" >> "$readme_file"
        echo "" >> "$readme_file"
        echo "Add usage examples here..." >> "$readme_file"
        echo "" >> "$readme_file"
        echo "### Configuration" >> "$readme_file"
        echo "" >> "$readme_file"
        echo "Add configuration details here..." >> "$readme_file"
    fi
}

update_main_readme() {
    local category="$1"
    local tool_name="$2"
    local description="$3"
    
    print_info "Updating main README.md..."
    
    # Check if category is already in main README
    if ! grep -q "### $(echo "$category" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')" "$MAIN_README"; then
        # Add new category section
        echo "" >> "$MAIN_README"
        echo "### $(echo "$category" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')" >> "$MAIN_README"
        echo "" >> "$MAIN_README"
    fi
    
    # Add tool to category section
    # This is a bit complex - for now, just note that manual update is needed
    print_warning "Please manually update the main README.md to include $tool_name in the $category section."
}

git_operations() {
    local category="$1"
    local tool_name="$2"
    
    print_info "Running git operations..."
    
    # Add files
    git add "$category/" 2>/dev/null || true
    
    # Commit
    local commit_msg="Add $tool_name to $category"
    if git commit -m "$commit_msg" 2>/dev/null; then
        print_success "Committed: $commit_msg"
        
        # Ask about pushing
        read -p "Push to GitHub? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if git push; then
                print_success "Pushed to GitHub!"
            else
                print_error "Failed to push to GitHub"
            fi
        fi
    else
        print_warning "No changes to commit or git not configured"
    fi
}

interactive_mode() {
    print_info "Interactive tool addition"
    echo ""
    
    # Get tool name
    read -p "Tool name: " tool_name
    if [[ -z "$tool_name" ]]; then
        print_error "Tool name is required"
        exit 1
    fi
    
    # Get category
    echo ""
    echo "Available categories:"
    for i in "${!CATEGORIES[@]}"; do
        echo "  $((i+1)). ${CATEGORIES[$i]}"
    done
    echo "  $(( ${#CATEGORIES[@]} + 1 )). New category"
    echo ""
    
    read -p "Category number: " category_num
    if [[ "$category_num" -eq $((${#CATEGORIES[@]} + 1)) ]]; then
        read -p "New category name: " category
        CATEGORIES+=("$category")
    elif [[ "$category_num" -ge 1 ]] && [[ "$category_num" -le ${#CATEGORIES[@]} ]]; then
        category="${CATEGORIES[$((category_num-1))]}"
    else
        print_error "Invalid category number"
        exit 1
    fi
    
    # Get description
    echo ""
    read -p "Brief description: " description
    
    # Get files
    echo ""
    echo "Files in workspace ($WORKSPACE_ROOT):"
    find "$WORKSPACE_ROOT" -maxdepth 2 -type f \( -name "*.sh" -o -name "*.py" -o -name "*.md" \) ! -path "*/.*" ! -path "*node_modules*" | head -20
    echo ""
    read -p "Files to add (space-separated, relative to workspace): " -a files
    
    # Confirm
    echo ""
    echo "Summary:"
    echo "  Tool: $tool_name"
    echo "  Category: $category"
    echo "  Description: $description"
    echo "  Files: ${files[*]}"
    echo ""
    
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cancelled"
        exit 0
    fi
    
    # Process
    main "$tool_name" "$category" "$description" "${files[@]}"
}

main() {
    local tool_name=""
    local category=""
    local description=""
    local files=()
    
    # Parse arguments if not in interactive mode
    if [[ $# -eq 0 ]]; then
        interactive_mode
        return
    fi
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--name)
                tool_name="$2"
                shift 2
                ;;
            -c|--category)
                category="$2"
                shift 2
                ;;
            -f|--files)
                shift
                while [[ $# -gt 0 ]] && [[ "$1" != -* ]]; do
                    files+=("$1")
                    shift
                done
                ;;
            -d|--description)
                description="$2"
                shift 2
                ;;
            -i|--interactive)
                interactive_mode
                return
                ;;
            -h|--help)
                print_usage
                exit 0
                ;;
            *)
                # Assume it's a file
                files+=("$1")
                shift
                ;;
        esac
    done
    
    # Validate inputs
    if [[ -z "$tool_name" ]]; then
        print_error "Tool name is required. Use -n or --name"
        print_usage
        exit 1
    fi
    
    if [[ -z "$category" ]]; then
        print_error "Category is required. Use -c or --category"
        print_usage
        exit 1
    fi
    
    if ! validate_category "$category"; then
        print_error "Invalid category: $category"
        print_info "Available categories: ${CATEGORIES[*]}"
        exit 1
    fi
    
    if [[ ${#files[@]} -eq 0 ]]; then
        print_error "No files specified. Use -f or --files"
        print_usage
        exit 1
    fi
    
    if [[ -z "$description" ]]; then
        description="A tool for OpenClaw automation."
        print_warning "No description provided. Using default: $description"
    fi
    
    print_info "Adding tool: $tool_name to category: $category"
    
    # Change to repository root
    cd "$REPO_ROOT" || {
        print_error "Failed to change to repository root: $REPO_ROOT"
        exit 1
    }
    
    # Create category directory
    create_category_directory "$category"
    
    # Copy files
    if ! copy_files "$category" "${files[@]}"; then
        print_error "Failed to copy files"
        exit 1
    fi
    
    # Generate README
    generate_readme "$category" "$tool_name" "$description"
    
    # Update main README
    update_main_readme "$category" "$tool_name" "$description"
    
    # Git operations
    git_operations "$category" "$tool_name"
    
    print_success "Tool '$tool_name' added successfully to $category/"
    print_info "Next steps:"
    print_info "  1. Review the generated README in $category/"
    print_info "  2. Update main README.md if needed"
    print_info "  3. Test the tool installation"
    print_info "  4. Consider adding to CHANGELOG.md"
}

# Run main function with all arguments
main "$@"