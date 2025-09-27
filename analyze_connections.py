#!/usr/bin/env python3
"""
Analyze all "Connects to" references in Clever's codebase and verify actual connections.

Why: Clean up documentation debt by removing non-functional connection references
Where: Scans all files for "Connects to:" sections and validates actual imports/calls
How: Parse docstrings, check imports, verify function calls, report invalid connections
"""

import re
import ast

def find_connects_to_references(file_path: str) -> List[Tuple[int, str, List[str]]]:
    """Find all 'Connects to:' blocks in a file and extract referenced modules/functions.
    
    Returns list of (line_number, full_block_text, [referenced_modules])
    """
    references = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        i = 0
        while i < len(lines):
            line = lines[i].strip().lower()
            if 'connects to' in line and ':' in line:
                # Found a "Connects to:" section - collect the full block
                start_line = i + 1
                block_lines = []
                references_found = []
                
                # Read until we hit a blank line or new section
                j = i + 1
                while j < len(lines):
                    current = lines[j].strip()
                    if not current:  # Empty line ends the block
                        break
                    if current.startswith(('"""', "'''", '*/', '#')):  # End of docstring
                        break
                    if re.match(r'^\s*[A-Z][a-zA-Z\s]+:', current):  # New section (Why:, Where:, etc.)
                        break
                    
                    block_lines.append(current)
                    
                    # Extract module references (look for .py files and module names)
                    module_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*\.py)', current)
                    references_found.extend(module_matches)
                    
                    # Also look for bare module names followed by ':'
                    bare_matches = re.findall(r'-\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*):?', current)
                    references_found.extend(bare_matches)
                    
                    j += 1
                
                if block_lines:
                    full_block = '\n'.join(block_lines)
                    references.append((start_line, full_block, references_found))
                
                i = j
            else:
                i += 1
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return references

def get_python_imports(file_path: str) -> Set[str]:
    """Extract all import statements from a Python file."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Parse AST to get imports
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
                        # Also add the full module.name format
                        for alias in node.names:
                            imports.add(f"{node.module}.{alias.name}")
        except SyntaxError:
            # Fallback to regex for files with syntax issues
            import_patterns = [
                r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)',
                r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import'
            ]
            for line in content.split('\n'):
                line = line.strip()
                for pattern in import_patterns:
                    match = re.match(pattern, line)
                    if match:
                        imports.add(match.group(1))
    
    except Exception as e:
        print(f"Error parsing imports from {file_path}: {e}")
    
    return imports

def get_javascript_references(file_path: str) -> Set[str]:
    """Extract referenced files and modules from JavaScript."""
    references = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Look for script src, import statements, and require calls
        patterns = [
            r'src=[\'""]([^\'""]+\.js)[\'"""]',
            r'import.*from\s+[\'""]([^\'""]+)[\'"""]',
            r'require\([\'""]([^\'""]+)[\'""]\)',
            r'window\.([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\.([a-zA-Z_][a-zA-Z0-9_]*\.js)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            references.update(matches)
            
    except Exception as e:
        print(f"Error parsing JavaScript references from {file_path}: {e}")
    
    return references

def file_exists_in_project(file_ref: str, project_root: str) -> bool:
    """Check if a referenced file actually exists in the project."""
    # Handle various reference formats
    possible_paths = [
        file_ref,
        f"{file_ref}.py" if not file_ref.endswith('.py') else file_ref,
        f"static/js/{file_ref}",
        f"static/js/components/{file_ref}",
        f"static/js/engines/{file_ref}",
        f"templates/{file_ref}",
        f"utils/{file_ref}",
        f"tools/{file_ref}",
    ]
    
    for path in possible_paths:
        full_path = os.path.join(project_root, path)
        if os.path.exists(full_path):
            return True
    
    return False

def analyze_connections():
    """Main analysis function."""
    project_root = "/home/jgallegos1991/Clever"
    issues = []
    
    # Find all relevant files
    for root, dirs, files in os.walk(project_root):
        # Skip certain directories
        skip_dirs = {'__pycache__', '.git', '.venv', 'node_modules', '.pytest_cache'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith(('.py', '.js', '.md', '.html')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, project_root)
                
                # Find "Connects to:" references
                connects_refs = find_connects_to_references(file_path)
                
                if connects_refs:
                    # Get actual imports/references for this file
                    if file.endswith('.py'):
                        actual_imports = get_python_imports(file_path)
                    elif file.endswith('.js'):
                        actual_imports = get_javascript_references(file_path)
                    else:
                        actual_imports = set()
                    
                    # Check each "Connects to:" block
                    for line_num, block_text, referenced_modules in connects_refs:
                        for ref in referenced_modules:
                            # Clean up the reference
                            clean_ref = ref.replace('.py', '').replace('static/js/', '').replace('components/', '').replace('engines/', '')
                            
                            # Check if the reference is valid
                            is_imported = any(clean_ref in imp for imp in actual_imports)
                            file_exists = file_exists_in_project(ref, project_root)
                            
                            if not is_imported and not file_exists:
                                issues.append({
                                    'file': rel_path,
                                    'line': line_num,
                                    'reference': ref,
                                    'block': block_text[:100] + '...' if len(block_text) > 100 else block_text,
                                    'reason': 'Neither imported nor file exists'
                                })
                            elif not is_imported and file_exists:
                                # File exists but not imported - might be a valid reference for documentation
                                # but let's flag it for review
                                issues.append({
                                    'file': rel_path,
                                    'line': line_num,
                                    'reference': ref,
                                    'block': block_text[:100] + '...' if len(block_text) > 100 else block_text,
                                    'reason': 'File exists but not imported/referenced in code'
                                })
    
    return issues

if __name__ == "__main__":
    print("🔍 Analyzing 'Connects to:' references in Clever codebase...")
    issues = analyze_connections()
    
    if not issues:
        print("✅ All 'Connects to:' references appear to be valid!")
    else:
        print(f"❌ Found {len(issues)} potentially invalid references:\n")
        
        grouped = {}
        for issue in issues:
            if issue['file'] not in grouped:
                grouped[issue['file']] = []
            grouped[issue['file']].append(issue)
        
        for file_path, file_issues in grouped.items():
            print(f"📁 {file_path}")
            for issue in file_issues:
                print(f"  Line {issue['line']}: {issue['reference']}")
                print(f"    Reason: {issue['reason']}")
                print(f"    Context: {issue['block']}")
                print()
        
        print(f"\n💡 Total files with issues: {len(grouped)}")
        print("💡 These references should be either:")
        print("   1. Fixed to point to actual files/modules")
        print("   2. Removed if no longer relevant")
        print("   3. Updated to match current code structure")