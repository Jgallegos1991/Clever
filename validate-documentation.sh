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