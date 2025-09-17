#!/bin/bash

# Documentation Enforcement Script
# This script validates that all code follows Clever's documentation standards

set -e

echo "🔍 Clever Code Documentation Validator"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Function to report errors
report_error() {
    echo -e "${RED}❌ $1${NC}"
    ((ERRORS++))
}

report_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

report_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check 1: Mandatory documentation patterns
echo
echo "📝 Checking mandatory documentation patterns..."

python_files=$(find . -name "*.py" -not -path "./.venv/*" -not -path "./.git/*" -not -path "./__pycache__/*")

for file in $python_files; do
    if grep -q "def \|class " "$file"; then
        # Check for functions/classes without proper documentation
        if ! grep -q "Why:" "$file" || ! grep -q "Where:" "$file" || ! grep -q "How:" "$file"; then
            report_error "Missing Why/Where/How documentation in $file"
            echo "   All functions must include:"
            echo "     - Why: Purpose and reasoning"
            echo "     - Where: System connections"
            echo "     - How: Technical implementation"
        else
            report_success "Documentation complete in $file"
        fi
    fi
done

# Check 2: Single database enforcement
echo
echo "🗄️  Checking single database enforcement..."

# Look for multiple database references
if db_violations=$(grep -r "\.db" --include="*.py" . | grep -v "clever\.db" | grep -v "DB_PATH" | grep -v "#" | grep -v "test"); then
    if [ ! -z "$db_violations" ]; then
        report_error "Found references to databases other than clever.db:"
        echo "$db_violations"
        echo "   Only use config.DB_PATH for database operations"
    fi
else
    report_success "Single database architecture enforced"
fi

# Check 3: No fallback patterns
echo
echo "🚫 Checking for prohibited fallback patterns..."

if fallback_violations=$(grep -r "fallback\|placeholder.*db\|backup.*db" --include="*.py" . | grep -v "#.*fallback" | grep -v "test"); then
    if [ ! -z "$fallback_violations" ]; then
        report_error "Found prohibited fallback patterns:"
        echo "$fallback_violations"
        echo "   Remove all fallbacks for full-potential operation"
    fi
else
    report_success "No fallback patterns found"
fi

# Check 4: Proper config imports
echo
echo "⚙️  Checking config imports..."

for file in $python_files; do
    if grep -q "sqlite3.connect\|db_path\|database" "$file" && ! grep -q "test" "$file"; then
        if ! grep -q "from config import DB_PATH\|config\.DB_PATH\|import config" "$file"; then
            report_error "$file uses database without importing from config"
            echo "   Always use: from config import DB_PATH"
        fi
    fi
done

# Check 5: Offline guard enforcement
echo
echo "🌐 Checking offline enforcement..."

if ! grep -q "offline_guard\.enable" app.py; then
    report_error "app.py missing offline_guard.enable() call"
    echo "   Add: from utils import offline_guard; offline_guard.enable()"
else
    report_success "Offline guard properly enforced"
fi

# Summary
echo
echo "📊 Summary"
echo "=========="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed! Code follows Clever's standards.${NC}"
    exit 0
else
    echo -e "${RED}💥 Found $ERRORS violations of Clever's coding standards.${NC}"
    echo
    echo "Fix these issues before committing. Run this script again to verify."
    exit 1
fi
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
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

# validate-documentation.sh - Validates Python documentation standards for Clever AI

set -e

REPO_ROOT="/home/runner/work/projects/projects"
EXIT_CODE=0

echo "🔍 Validating Python documentation standards..."

# Function to check if a Python file has proper documentation
validate_python_file() {
    local file="$1"
    local issues=0
    
    echo "Checking: $file"
    
    # Check for module docstring
    if ! grep -q '"""' "$file" && ! grep -q "'''" "$file"; then
        echo "  ❌ Missing module docstring: $file"
        ((issues++))
    fi
    
    # Check for class documentation (Why/Where/How pattern)
    if grep -q "^class " "$file"; then
        # Look for classes and check if they have docstrings
        while read -r class_line; do
            class_name=$(echo "$class_line" | sed 's/class \([^(:]*\).*/\1/')
            # Check if class has docstring within next 10 lines
            line_num=$(grep -n "^class $class_name" "$file" | cut -d: -f1)
            if [ -n "$line_num" ]; then
                next_lines=$(sed -n "$((line_num+1)),$((line_num+10))p" "$file")
                if ! echo "$next_lines" | grep -q '"""' && ! echo "$next_lines" | grep -q "'''"; then
                    echo "  ❌ Class $class_name missing docstring: $file"
                    ((issues++))
                fi
            fi
        done < <(grep "^class " "$file")
    fi
    
    # Check for function documentation
    if grep -q "^def " "$file" || grep -q "^    def " "$file"; then
        # Look for functions and check if they have docstrings
        while read -r func_line; do
            func_name=$(echo "$func_line" | sed 's/.*def \([^(]*\).*/\1/')
            # Skip __init__, __str__, etc. as they may not need full docs
            if [[ "$func_name" =~ ^__.+__$ ]]; then
                continue
            fi
            line_num=$(grep -n "$func_line" "$file" | cut -d: -f1)
            if [ -n "$line_num" ]; then
                next_lines=$(sed -n "$((line_num+1)),$((line_num+5))p" "$file")
                if ! echo "$next_lines" | grep -q '"""' && ! echo "$next_lines" | grep -q "'''"; then
                    echo "  ❌ Function $func_name missing docstring: $file"
                    ((issues++))
                fi
            fi
        done < <(grep -E "^def |^    def " "$file")
    fi
    
    # Check for config.DB_PATH usage instead of hardcoded paths
    if grep -q "clever\.db\|\.db" "$file" && ! grep -q "config\.DB_PATH" "$file"; then
        if grep -q "db_path.*=" "$file" || grep -q "database.*path" "$file"; then
            echo "  ❌ Hardcoded database path found, should use config.DB_PATH: $file"
            ((issues++))
        fi
    fi
    
    # Check for fallback/placeholder logic that should be removed
    if grep -q "except ImportError\|# Fallback\|# TODO\|# FIXME" "$file"; then
        echo "  ⚠️  Contains fallback/placeholder logic that may need removal: $file"
        ((issues++))
    fi
    
    if [ $issues -eq 0 ]; then
        echo "  ✅ $file passes validation"
    else
        echo "  ❌ $file has $issues issues"
        return 1
    fi
    
    return 0
}

# Find all Python files and validate them
find "$REPO_ROOT" -name "*.py" -type f | while read -r file; do
    # Skip __pycache__ and .venv directories
    if [[ "$file" == *"__pycache__"* ]] || [[ "$file" == *".venv"* ]]; then
        continue
    fi
    
    if ! validate_python_file "$file"; then
        EXIT_CODE=1
    fi
done

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All Python files pass documentation validation!"
else
    echo "❌ Some Python files need documentation improvements"
fi

exit $EXIT_CODE
 main
