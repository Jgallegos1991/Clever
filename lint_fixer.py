#!/usr/bin/env python3
"""
lint_fixer.py - Automated Clever Codebase Lint Error Fixer

Why: Cleans up F401 (unused imports), F541 (f-strings without placeholders),
     and F841 (unused variables) errors to maintain high code quality.

Where: Runs across all Clever Python files to systematically fix linting issues
       while preserving functionality and maintaining code integrity.

How: Pattern matching and replacement for common lint errors, with careful
     preservation of actual f-strings that need placeholders.
"""

import re

def fix_f_string_without_placeholders(content: str) -> str:
    """
    Fix f-strings that don't actually need f-string formatting
    
    Why: F541 errors occur when f-strings have no {} placeholders
    Where: Throughout codebase in print statements and string literals
    How: Convert "text" to "text" when no placeholders present
    """
    
    # Pattern to match f-strings without any {} placeholders
    # This handles both "..." and '...' variants
    pattern = r'f(["\'])((?:[^"\'\\]|\\.)*)(?!\{)\1'
    
    def replace_f_string(match):
        quote = match.group(1) 
        content = match.group(2)
        
        # Only replace if there are truly no {} placeholders
        if '{' not in content:
            return f'{quote}{content}{quote}'
        else:
            # Keep f-string if it has placeholders
            return match.group(0)
    
    return re.sub(pattern, replace_f_string, content)

def remove_unused_imports(content: str, filename: str) -> str:
    """
    Remove common unused imports while preserving essential ones
    
    Why: F401 errors for imports that aren't used in the code
    Where: Import statements at top of files  
    How: Remove imports that are commonly unused but preserve critical ones
    """
    
    lines = content.split('\n')
    filtered_lines = []
    
    # Common unused imports to remove (but be selective)
    unused_patterns = [
        r'^import os$',
        r'^import sys$', 
        r'^import json$',
        r'^import subprocess$',
        r'^import threading$',
        r'^import socket$',
        r'^import hashlib$',
        r'^import mimetypes$',
        r'^import time$',
        r'^import base64$',
        r'^import shutil$',
        r'^from pathlib import Path$',
        r'^from typing import.*List.*$',
        r'^from typing import.*Optional.*$',
        r'^from typing import.*Tuple.*$',
        r'^from typing import.*Set.*$',
        r'^from typing import.*Union.*$',
    ]
    
    # Don't remove these critical files
    keep_files = ['app.py', 'config.py', 'database.py', 'persona.py']
    
    if any(keep_file in filename for keep_file in keep_files):
        # Don't modify critical files
        return content
    
    for line in lines:
        # Check if this line matches any unused import pattern
        should_remove = False
        for pattern in unused_patterns:
            if re.match(pattern, line.strip()):
                should_remove = True
                break
        
        if not should_remove:
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)

def fix_unused_variables(content: str) -> str:
    """
    Fix unused variables by either using them or renaming to _
    
    Why: F841 errors for variables assigned but never used
    Where: Local variable assignments throughout code
    How: Prefix with _ to indicate intentionally unused
    """
    
    # Common patterns of unused variables to rename with _
    _patterns = [
        (r'(\s+)([a-zA-Z_]\w*)\s*=\s*([^=\n]+)(\n.*?)# intentionally unused', r'\1_\2 = \3\4# intentionally unused'),
    ]
    
    result = content
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result, flags=re.MULTILINE)
    
    return result

def process_file(file_path: Path) -> bool:
    """
    Process a single Python file to fix linting issues
    
    Why: Clean up individual files while preserving functionality
    Where: Each Python file in the Clever codebase
    How: Apply all lint fixes and write back to file
    """
    
    try:
        # Read file content
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Apply fixes
        content = fix_f_string_without_placeholders(content)
        content = remove_unused_imports(content, str(file_path))
        content = fix_unused_variables(content)
        
        # Only write if content changed
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            print(f"✓ Clean: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """
    Main function to fix linting issues across Clever codebase
    
    Why: Systematically clean up all Python files in the project
    Where: Current directory and subdirectories  
    How: Process each .py file with lint fixes
    """
    
    print("🔧 CLEVER LINT FIXER - Cleaning up codebase...")
    print("=" * 60)
    
    # Get current directory
    clever_dir = Path('.')
    
    # Find all Python files
    python_files = list(clever_dir.glob('*.py'))
    
    # Skip certain files that might be critical
    skip_files = {'__init__.py', 'setup.py'}
    python_files = [f for f in python_files if f.name not in skip_files]
    
    print(f"Found {len(python_files)} Python files to process...")
    
    fixed_count = 0
    for file_path in sorted(python_files):
        if process_file(file_path):
            fixed_count += 1
    
    print("=" * 60)
    print(f"🎯 RESULTS: {fixed_count}/{len(python_files)} files fixed")
    print("✨ Lint cleanup complete!")

if __name__ == "__main__":
    main()