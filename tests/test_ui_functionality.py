"""
UI Tooltip Testing Module
Tests tooltip functionality using built-in libraries
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Any


class UITooltipTests:
    """
    Comprehensive UI tooltip testing system for Clever AI interface validation.
    
    Why: Ensures user interface tooltips are consistent, accessible, and
         properly structured across all template files for optimal UX.
    Where: Used by testing infrastructure to validate UI components meet
           accessibility standards and tooltip consistency requirements.
    How: Parses HTML templates using regex, extracts button elements,
         validates tooltip attributes, and checks accessibility compliance.
    """
    
    def __init__(self):
        self.templates_dir = Path(__file__).resolve().parents[1] / 'templates'
        self.test_results = []
    
    def run_all_tooltip_tests(self) -> Dict[str, Any]:
        """
        Execute comprehensive tooltip test suite and aggregate results.
        
        Why: Provides unified entry point for all tooltip-related validation
             with structured reporting and error handling for CI/CD integration.
        Where: Main testing method called by test runners and validation
               systems to verify UI tooltip compliance across templates.
        How: Runs battery of tooltip tests, captures results and errors,
             calculates pass/fail statistics, returns structured report.
             
        Returns:
            Dict[str, Any]: Comprehensive test results with status and details
        """
        tests = [
            ('button_tooltips_exist', self.test_button_tooltips_exist),
            ('tooltip_consistency', self.test_tooltip_consistency),
            ('accessibility_attributes', self.test_accessibility_attributes),
            ('tooltip_html_structure', self.test_tooltip_html_structure)
        ]
        
        passed = 0
        total = len(tests)
        results = {}
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = {
                    'status': 'passed' if result['passed'] else 'failed',
                    'details': result
                }
                if result['passed']:
                    passed += 1
            except Exception as e:
                results[test_name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': results
        }
    
    def get_template_files(self) -> List[Path]:
        """Get all HTML template files"""
        if not self.templates_dir.exists():
            return []
        return list(self.templates_dir.glob('*.html'))
    
    def extract_buttons_from_html(self, file_path: Path) -> List[Dict[str, str]]:
        """Extract button information from HTML file using regex"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all button tags
        button_pattern = r'<button([^>]*?)>(.*?)</button>'
        buttons = re.findall(button_pattern, content, re.IGNORECASE | re.DOTALL)
        
        button_data = []
        for attributes, inner_text in buttons:
            # Extract key attributes
            id_match = re.search(r'id=["\']([^"\']*)["\']', attributes, re.IGNORECASE)
            class_match = re.search(r'class=["\']([^"\']*)["\']', attributes, re.IGNORECASE)
            title_match = re.search(r'title=["\']([^"\']*)["\']', attributes, re.IGNORECASE)
            aria_label_match = re.search(r'aria-label=["\']([^"\']*)["\']', attributes, re.IGNORECASE)
            type_match = re.search(r'type=["\']([^"\']*)["\']', attributes, re.IGNORECASE)
            
            button_data.append({
                'id': id_match.group(1) if id_match else '',
                'class': class_match.group(1) if class_match else '',
                'title': title_match.group(1) if title_match else '',
                'aria_label': aria_label_match.group(1) if aria_label_match else '',
                'type': type_match.group(1) if type_match else '',
                'text': re.sub(r'<[^>]+>', '', inner_text).strip(),
                'full_attributes': attributes,
                'file': file_path.name
            })
        
        return button_data
    
    def test_button_tooltips_exist(self) -> Dict[str, Any]:
        """Test that all buttons have tooltips (title attribute)"""
        template_files = self.get_template_files()
        missing_tooltips = []
        total_buttons = 0
        
        for template_file in template_files:
            buttons = self.extract_buttons_from_html(template_file)
            total_buttons += len(buttons)
            
            for button in buttons:
                if not button['title']:
                    missing_tooltips.append({
                        'file': button['file'],
                        'button_id': button['id'] or 'unnamed',
                        'button_text': button['text'],
                        'button_class': button['class']
                    })
        
        return {
            'passed': len(missing_tooltips) == 0,
            'total_buttons': total_buttons,
            'missing_tooltips': missing_tooltips,
            'message': f'Checked {total_buttons} buttons across {len(template_files)} templates'
        }
    
    def test_tooltip_consistency(self) -> Dict[str, Any]:
        """Test that similar buttons have consistent tooltip patterns"""
        template_files = self.get_template_files()
        button_patterns = {}
        
        for template_file in template_files:
            buttons = self.extract_buttons_from_html(template_file)
            
            for button in buttons:
                # Categorize buttons by function
                button_text = button['text'].lower()
                button_id = button['id'].lower()
                
                if any(keyword in button_id or keyword in button_text for keyword in ['send', '⬆', '✨']):
                    pattern = 'send_button'
                elif any(keyword in button_id or keyword in button_text for keyword in ['mic', '🎤', 'voice']):
                    pattern = 'mic_button'
                elif any(keyword in button_id or keyword in button_text for keyword in ['close', '×', 'cancel']):
                    pattern = 'close_button'
                elif any(keyword in button_id for keyword in ['generate', 'create']):
                    pattern = 'action_button'
                else:
                    pattern = 'other'
                
                if pattern not in button_patterns:
                    button_patterns[pattern] = []
                
                button_patterns[pattern].append(button)
        
        inconsistencies = []
        for pattern, buttons in button_patterns.items():
            if len(buttons) > 1:
                titles = [b['title'].lower().strip() for b in buttons if b['title']]
                unique_titles = list(set(titles))
                
                # Check for semantic consistency
                if pattern == 'send_button':
                    if not all('send' in title for title in unique_titles if title):
                        inconsistencies.append({
                            'pattern': pattern,
                            'issue': 'Send buttons should contain "send" in tooltip',
                            'buttons': [{'file': b['file'], 'id': b['id'], 'title': b['title']} for b in buttons]
                        })
                elif pattern == 'mic_button':
                    if not all(any(word in title for word in ['voice', 'input', 'talk']) for title in unique_titles if title):
                        inconsistencies.append({
                            'pattern': pattern,
                            'issue': 'Mic buttons should contain voice-related words in tooltip',
                            'buttons': [{'file': b['file'], 'id': b['id'], 'title': b['title']} for b in buttons]
                        })
        
        return {
            'passed': len(inconsistencies) == 0,
            'patterns_found': list(button_patterns.keys()),
            'inconsistencies': inconsistencies,
            'total_patterns': len(button_patterns)
        }
    
    def test_accessibility_attributes(self) -> Dict[str, Any]:
        """Test that buttons have proper accessibility attributes"""
        template_files = self.get_template_files()
        accessibility_issues = []
        
        for template_file in template_files:
            buttons = self.extract_buttons_from_html(template_file)
            
            for button in buttons:
                issues = []
                
                # Check icon-only buttons for accessibility
                button_text = button['text'].strip()
                is_icon_only = len(button_text) <= 2 or all(ord(char) > 127 for char in button_text)  # Emojis
                
                if is_icon_only and not (button['aria_label'] or button['title']):
                    issues.append('Icon-only button missing aria-label or title')
                
                # Check form buttons for type attribute
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '<form' in content and button['id']:
                    # Check if button is in a form context
                    button_match = re.search(rf'<button[^>]*id=["\']?{re.escape(button["id"])}["\']?[^>]*>', content, re.IGNORECASE)
                    if button_match:
                        before_button = content[:button_match.start()]
                        after_button = content[button_match.end():]
                        
                        # Count form tags before and after
                        forms_before = before_button.count('<form') - before_button.count('</form>')
                        forms_after = after_button.count('</form>') - after_button.count('<form')
                        
                        if forms_before > 0 and not button['type']:
                            issues.append('Button in form missing type attribute')
                
                if issues:
                    accessibility_issues.append({
                        'file': button['file'],
                        'button_id': button['id'] or 'unnamed',
                        'issues': issues
                    })
        
        return {
            'passed': len(accessibility_issues) == 0,
            'accessibility_issues': accessibility_issues,
            'total_checked': sum(len(self.extract_buttons_from_html(f)) for f in template_files)
        }
    
    def test_tooltip_html_structure(self) -> Dict[str, Any]:
        """Test that tooltips are properly structured in HTML"""
        template_files = self.get_template_files()
        html_issues = []
        
        for template_file in template_files:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find buttons with title attributes
            button_pattern = r'<button[^>]*title=[^>]*>'
            buttons = re.findall(button_pattern, content, re.IGNORECASE)
            
            for button_html in buttons:
                # Check for proper quoting
                title_match = re.search(r'title=(["\'])(.*?)\1', button_html, re.IGNORECASE)
                if not title_match:
                    # Title exists but not properly quoted
                    title_unquoted = re.search(r'title=([^\s>]+)', button_html, re.IGNORECASE)
                    if title_unquoted:
                        html_issues.append({
                            'file': template_file.name,
                            'issue': 'Title attribute not properly quoted',
                            'html_snippet': button_html
                        })
                else:
                    title_value = title_match.group(2)
                    # Check for unescaped characters
                    if '"' in title_value and title_match.group(1) == '"':
                        html_issues.append({
                            'file': template_file.name,
                            'issue': 'Unescaped quotes in title attribute',
                            'html_snippet': button_html
                        })
        
        return {
            'passed': len(html_issues) == 0,
            'html_issues': html_issues,
            'files_checked': len(template_files)
        }


def run_ui_tooltip_tests() -> Dict[str, Any]:
    """
    Execute UI tooltip validation tests and return structured results.
    
    Why: Provides programmatic interface for tooltip testing that can be
         integrated into automated testing pipelines and validation systems.
    Where: Called by test automation, CI/CD processes, and manual validation
           tools to verify UI tooltip compliance and consistency.
    How: Creates UITooltipTests instance, executes full test suite,
         returns structured results for further processing or reporting.
         
    Returns:
        Dict[str, Any]: Complete test results including pass/fail status
    """
    test_runner = UITooltipTests()
    return test_runner.run_all_tooltip_tests()


if __name__ == '__main__':
    # Run tests directly
    results = run_ui_tooltip_tests()
    print("UI Tooltip Test Results:")
    print(f"Status: {results['status']}")
    print(f"Tests: {results['passed']}/{results['total']} passed")
    
    for test_name, test_result in results['tests'].items():
        print(f"\n{test_name}: {test_result['status']}")
        if test_result['status'] == 'failed':
            print(f"  Details: {test_result['details']}")
        elif test_result['status'] == 'error':
            print(f"  Error: {test_result['error']}")
