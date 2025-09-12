#!/bin/bash
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