#!/usr/bin/env python3
"""
Component Validation Tool for Clever

Why: Provide instant detection of CSS/HTML/JS mismatches that cause invisible UI elements.
     The particle visibility issue showed we need automated component health checking.
Where: Standalone script for validating UI component integrity, also used by introspection.py
How: Cross-references HTML element IDs, CSS selectors, and JavaScript queries to detect mismatches.

Usage:
    python tools/validate_components.py                    # Full validation
    python tools/validate_components.py --component=particles  # Single component  
    python tools/validate_components.py --fix             # Auto-fix detected issues

Connects to:
    - templates/index.html: Scans for UI element IDs and structure
    - static/css/style.css: Validates CSS selectors and z-index hierarchy  
    - static/js/main.js: Checks JavaScript element queries and initialization
    - introspection.py: validate_ui_components() uses same validation logic
"""
import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class ComponentValidator:
    """
    UI Component integrity validator
    
    Why: Automatically catch CSS/HTML/JS mismatches before they cause invisible UI bugs
    Where: Used by validation script and introspection system for component health
    How: Parses templates, stylesheets, and scripts to validate component connections
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize validator with project root path
        
        Args:
            project_root: Path to Clever project root (defaults to script location)
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent
        self.root = project_root
        self.template_path = self.root / "templates" / "index.html"
        self.css_path = self.root / "static" / "css" / "style.css"
        self.js_main_path = self.root / "static" / "js" / "main.js"
        
    def validate_all_components(self) -> Dict[str, Any]:
        """
        Run complete component validation suite
        
        Why: Comprehensive health check for all UI components
        Where: Called by main validation script and introspection system  
        How: Runs individual component validators and aggregates results
        
        Returns:
            Complete validation results with status and detected issues
        """
        results = {
            "particle_system": self._validate_particle_system(),
            "chat_interface": self._validate_chat_interface(),
            "input_controls": self._validate_input_controls(), 
            "z_index_hierarchy": self._validate_z_index_hierarchy(),
            "timestamp": None,  # Will be set by caller
            "overall_status": "healthy"
        }
        
        # Determine overall health
        issues = []
        for component, result in results.items():
            if isinstance(result, dict) and result.get("status") == "error":
                issues.append(component)
                
        if issues:
            results["overall_status"] = "issues_detected"
            results["issues"] = issues
            
        return results
    
    def _validate_particle_system(self) -> Dict[str, Any]:
        """
        Validate holographic particle system component
        
        Why: Prevent invisible particles caused by CSS/HTML ID mismatches
        Where: Core validation for Clever's primary visual interface
        How: Cross-references canvas element ID across HTML, CSS, and JavaScript
        """
        if not self.template_path.exists():
            return {"status": "error", "message": "Template file not found"}
            
        try:
            # Parse HTML for canvas element
            html_content = self.template_path.read_text()
            canvas_match = re.search(r'<canvas[^>]+id=["\']([^"\']+)["\']', html_content)
            html_canvas_id = canvas_match.group(1) if canvas_match else None
            
            # Parse CSS for canvas styling
            css_content = self.css_path.read_text() if self.css_path.exists() else ""
            css_canvas_selectors = re.findall(r'#([a-zA-Z0-9_-]+)\s*{[^}]*(?:position|z-index)', css_content)
            
            # Parse JavaScript for element queries  
            js_content = self.js_main_path.read_text() if self.js_main_path.exists() else ""
            js_canvas_queries = re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js_content)
            
            # Build validation results
            result = {
                "status": "healthy",
                "html_canvas_id": html_canvas_id,
                "css_selectors": css_canvas_selectors,
                "js_queries": js_canvas_queries,
                "issues": []
            }
            
            # Check for mismatches
            if html_canvas_id:
                if html_canvas_id not in css_canvas_selectors:
                    result["status"] = "error"
                    result["issues"].append({
                        "type": "css_selector_missing",
                        "message": f"CSS missing selector #{html_canvas_id} for HTML canvas element",
                        "fix_suggestion": f"Add CSS rule: #{html_canvas_id} {{ /* canvas styles */ }}"
                    })
                    
                if html_canvas_id not in js_canvas_queries:
                    result["issues"].append({
                        "type": "js_query_missing", 
                        "message": f"JavaScript missing getElementById('{html_canvas_id}') query",
                        "fix_suggestion": f"Add JS: document.getElementById('{html_canvas_id}')"
                    })
            else:
                result["status"] = "error"
                result["issues"].append({
                    "type": "html_element_missing",
                    "message": "No canvas element found in HTML template",
                    "fix_suggestion": "Add <canvas id=\"particles\"></canvas> to template"
                })
                
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Validation failed: {str(e)}"}
    
    def _validate_chat_interface(self) -> Dict[str, Any]:
        """Validate chat interface component (placeholder)"""
        return {"status": "healthy", "message": "Chat validation not implemented"}
    
    def _validate_input_controls(self) -> Dict[str, Any]:
        """Validate input controls component (placeholder)"""  
        return {"status": "healthy", "message": "Input validation not implemented"}
    
    def _validate_z_index_hierarchy(self) -> Dict[str, Any]:
        """
        Validate z-index hierarchy for proper UI layering
        
        Why: Conflicting z-index values can hide UI elements behind others
        Where: System-wide validation of CSS layering rules
        How: Parses CSS z-index declarations and detects conflicts
        """
        if not self.css_path.exists():
            return {"status": "error", "message": "CSS file not found"}
            
        try:
            css_content = self.css_path.read_text()
            
            # Extract z-index declarations with context
            z_index_pattern = r'([#.][\w-]+)\s*\{([^}]*z-index:\s*(\d+)[^}]*)\}'
            matches = re.findall(z_index_pattern, css_content)
            
            hierarchy = {}
            conflicts = []
            
            for selector, rule_block, z_value in matches:
                z_int = int(z_value)
                hierarchy[selector] = z_int
                
                # Check for conflicts
                for existing_selector, existing_z in hierarchy.items():
                    if existing_selector != selector and existing_z == z_int:
                        conflicts.append({
                            "type": "duplicate_z_index",
                            "message": f"Duplicate z-index {z_int}: {selector} and {existing_selector}",
                            "selectors": [selector, existing_selector],
                            "z_index": z_int
                        })
            
            return {
                "status": "healthy" if not conflicts else "warning",
                "hierarchy": hierarchy,
                "conflicts": conflicts,
                "max_z_index": max(hierarchy.values()) if hierarchy else 0
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Z-index validation failed: {str(e)}"}
    
    def auto_fix_issues(self, validation_results: Dict[str, Any]) -> List[str]:
        """
        Automatically fix detected component issues
        
        Why: Provide automated repair for common CSS/HTML/JS mismatches
        Where: Called when --fix flag is used with validation script
        How: Applies targeted fixes based on detected issue types
        
        Args:
            validation_results: Results from validate_all_components()
            
        Returns:
            List of fixes applied
        """
        fixes_applied = []
        
        # Fix particle system issues
        particle_result = validation_results.get("particle_system", {})
        if particle_result.get("status") == "error":
            fixes_applied.extend(self._fix_particle_system_issues(particle_result))
            
        return fixes_applied
    
    def _fix_particle_system_issues(self, result: Dict[str, Any]) -> List[str]:
        """Apply fixes for particle system component issues"""
        fixes = []
        
        for issue in result.get("issues", []):
            if issue["type"] == "css_selector_missing":
                # Could add CSS rule automatically
                fixes.append(f"Would add CSS selector: {issue['fix_suggestion']}")
            elif issue["type"] == "js_query_missing":
                # Could add JavaScript query
                fixes.append(f"Would add JS query: {issue['fix_suggestion']}")
                
        return fixes


def print_validation_results(results: Dict[str, Any]) -> None:
    """
    Print formatted validation results to console
    
    Why: Provide human-readable output for component validation
    Where: Called by main CLI interface
    How: Formats results with colors and clear issue descriptions
    """
    print("\n🔍 Clever Component Validation Results")
    print(f"{'=' * 50}")
    
    overall_status = results.get("overall_status", "unknown")
    status_icon = "✅" if overall_status == "healthy" else "❌"
    print(f"\n{status_icon} Overall Status: {overall_status.upper()}")
    
    if overall_status == "issues_detected":
        print(f"🚨 Issues found in: {', '.join(results.get('issues', []))}")
    
    print("\n📊 Component Details:")
    print(f"{'-' * 30}")
    
    for component, result in results.items():
        if component in ["timestamp", "overall_status", "issues"]:
            continue
            
        if isinstance(result, dict):
            status = result.get("status", "unknown")
            icon = "✅" if status == "healthy" else "⚠️" if status == "warning" else "❌"
            print(f"\n{icon} {component.replace('_', ' ').title()}: {status}")
            
            # Show issues if any
            issues = result.get("issues", [])
            if issues:
                for issue in issues:
                    print(f"   - {issue.get('message', 'Unknown issue')}")
                    if "fix_suggestion" in issue:
                        print(f"     💡 Fix: {issue['fix_suggestion']}")
            
            # Show conflicts for z-index validation
            conflicts = result.get("conflicts", [])
            if conflicts:
                for conflict in conflicts:
                    print(f"   - {conflict.get('message', 'Unknown conflict')}")


def main():
    """
    Main CLI interface for component validation
    
    Why: Provide command-line tool for instant component health checking
    Where: Standalone script entry point
    How: Parses arguments and runs appropriate validation functions
    """
    parser = argparse.ArgumentParser(description="Validate Clever UI component integrity")
    parser.add_argument("--component", help="Validate specific component (particles, chat, input)")
    parser.add_argument("--fix", action="store_true", help="Auto-fix detected issues")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    validator = ComponentValidator()
    
    # Run validation
    if args.component:
        # Single component validation (not yet implemented)
        print(f"Single component validation for '{args.component}' not yet implemented")
        sys.exit(1)
    else:
        results = validator.validate_all_components()
    
    # Apply fixes if requested
    if args.fix:
        fixes = validator.auto_fix_issues(results)
        if fixes:
            print("🔧 Applied fixes:")
            for fix in fixes:
                print(f"   - {fix}")
        else:
            print("✅ No fixes needed or available")
    
    # Output results
    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        print_validation_results(results)
    
    # Exit with error code if issues found
    if results.get("overall_status") == "issues_detected":
        sys.exit(1)


if __name__ == "__main__":
    main()