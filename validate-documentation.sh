#!/bin/bash
# Documentation and Architecture Standards Validation Script
# Validates that all Python files meet the Clever AI documentation standards

set -e

echo "🔍 Validating Clever AI Documentation and Architecture Standards..."

PROJECT_ROOT="/home/runner/work/projects/projects"
cd "$PROJECT_ROOT"

ERRORS=0
WARNINGS=0

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ((ERRORS++))
}

log_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
    ((WARNINGS++))
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Check 1: All functions and classes have Why/Where/How documentation
check_documentation() {
    echo -e "\n${BLUE}📝 Checking function and class documentation...${NC}"
    
    python3 << 'EOF'
import ast
import os
import sys

def check_docstring_quality(docstring):
    """Check if docstring follows Why/Where/How pattern."""
    if not docstring:
        return False, "Missing docstring"
    
    # Convert to lowercase for checking
    doc_lower = docstring.lower()
    
    # Check for Why/Where/How pattern or comprehensive explanation
    has_why = any(word in doc_lower for word in ['why:', 'purpose:', 'reason:', 'because'])
    has_where = any(word in doc_lower for word in ['where:', 'location:', 'context:', 'used in'])
    has_how = any(word in doc_lower for word in ['how:', 'process:', 'implementation:', 'algorithm:'])
    
    # Accept if it has at least comprehensive explanation even without explicit Why/Where/How
    is_comprehensive = len(docstring.strip()) >= 50  # At least 50 chars of meaningful documentation
    
    if has_why or has_where or has_how or is_comprehensive:
        return True, "Good documentation"
    else:
        return False, "Lacks Why/Where/How pattern or comprehensive explanation"

def analyze_file(filepath):
    """Analyze a Python file for documentation standards."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = node.name
                docstring = ast.get_docstring(node)
                
                # Skip private methods and test methods for now
                if name.startswith('_') and not name.startswith('__'):
                    continue
                    
                is_good, reason = check_docstring_quality(docstring)
                if not is_good:
                    line_num = node.lineno
                    issues.append(f"  Line {line_num}: {type(node).__name__} '{name}' - {reason}")
        
        return issues
        
    except Exception as e:
        return [f"  Error parsing file: {e}"]

# Find all Python files
for root, dirs, files in os.walk('.'):
    # Skip hidden directories and __pycache__
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
    
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            issues = analyze_file(filepath)
            
            if issues:
                print(f"❌ {filepath}:")
                for issue in issues:
                    print(issue)
                sys.exit(1)  # Exit with error for any documentation issues
            else:
                print(f"✅ {filepath}")

print("✅ All Python files have proper documentation")
EOF
    
    if [ $? -ne 0 ]; then
        log_error "Documentation validation failed"
    else
        log_success "All functions and classes have proper documentation"
    fi
}

# Check 2: All database paths use config.DB_PATH
check_database_paths() {
    echo -e "\n${BLUE}🗄️  Checking database path configuration...${NC}"
    
    # Search for hardcoded database paths
    hardcoded_paths=$(grep -r "clever\.db\|clever_memory\.db" --include="*.py" . | grep -v "config.py" | grep -v "validate-documentation.sh" || true)
    
    if [ -n "$hardcoded_paths" ]; then
        log_error "Found hardcoded database paths (should use config.DB_PATH):"
        echo "$hardcoded_paths"
    else
        log_success "All database paths use config.DB_PATH"
    fi
    
    # Check that files import config.DB_PATH when needed
    db_usage=$(grep -l "\.db" --include="*.py" . -r | grep -v config.py | grep -v validate-documentation.sh || true)
    for file in $db_usage; do
        if ! grep -q "config\.DB_PATH\|config import" "$file" 2>/dev/null; then
            log_warning "$file uses database but doesn't import config.DB_PATH"
        fi
    done
}

# Check 3: No fallback or placeholder logic
check_fallback_logic() {
    echo -e "\n${BLUE}🚫 Checking for fallback and placeholder logic...${NC}"
    
    # Search for common fallback patterns
    fallback_patterns=(
        "except.*ImportError.*:"
        "except.*Exception.*:"
        "try:.*except:"
        "fallback"
        "placeholder"
        "TODO"
        "FIXME"
        "HACK"
    )
    
    for pattern in "${fallback_patterns[@]}"; do
        matches=$(grep -r "$pattern" --include="*.py" . | grep -v "validate-documentation.sh" | grep -v "# Allow fallbacks in tests" || true)
        if [ -n "$matches" ]; then
            log_warning "Found potential fallback/placeholder logic for pattern '$pattern':"
            echo "$matches" | head -5  # Show first 5 matches
            if [ $(echo "$matches" | wc -l) -gt 5 ]; then
                echo "... and $(( $(echo "$matches" | wc -l) - 5 )) more matches"
            fi
        fi
    done
}

# Check 4: Configuration centralization
check_config_centralization() {
    echo -e "\n${BLUE}⚙️  Checking configuration centralization...${NC}"
    
    # Check that all imports from config are present
    config_imports=$(grep -r "from config import\|import config" --include="*.py" . | wc -l)
    log_info "Found $config_imports files importing from config"
    
    # Check for hardcoded configuration values
    hardcoded_configs=$(grep -r "DEBUG.*=.*True\|HOST.*=.*[\"']" --include="*.py" . | grep -v config.py | grep -v validate-documentation.sh || true)
    if [ -n "$hardcoded_configs" ]; then
        log_warning "Found potential hardcoded configuration (should be in config.py):"
        echo "$hardcoded_configs" | head -5
    else
        log_success "Configuration appears to be centralized"
    fi
}

# Run all checks
check_documentation
check_database_paths  
check_fallback_logic
check_config_centralization

# Summary
echo -e "\n${BLUE}📊 Validation Summary:${NC}"
if [ $ERRORS -eq 0 ]; then
    log_success "Documentation and architecture standards validation PASSED"
    log_info "Errors: $ERRORS, Warnings: $WARNINGS"
    exit 0
else
    log_error "Documentation and architecture standards validation FAILED"
    log_info "Errors: $ERRORS, Warnings: $WARNINGS"
    exit 1
fi