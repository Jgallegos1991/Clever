"""
Unit tests for UI tooltip functionality
Tests that all buttons have consistent tooltip implementations
"""

import pytest
import re
from pathlib import Path
from bs4 import BeautifulSoup


class TestUITooltips:
    """Test suite for UI tooltip consistency and accessibility"""
    
    @pytest.fixture
    def template_files(self):
        """Get all HTML template files"""
        templates_dir = Path(__file__).resolve().parents[1] / 'templates'
        return list(templates_dir.glob('*.html'))
    
    def parse_html_file(self, file_path):
        """Parse HTML file and return BeautifulSoup object"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return BeautifulSoup(content, 'html.parser')
    
    def test_button_tooltips_exist(self, template_files):
        """Test that all buttons have tooltips (title attribute)"""
        missing_tooltips = []
        
        for template_file in template_files:
            soup = self.parse_html_file(template_file)
            buttons = soup.find_all('button')
            
            for button in buttons:
                button_id = button.get('id', 'unnamed')
                button_class = button.get('class', [])
                button_text = button.get_text(strip=True)
                
                if not button.get('title'):
                    missing_tooltips.append({
                        'file': template_file.name,
                        'button_id': button_id,
                        'button_class': button_class,
                        'button_text': button_text,
                        'button_html': str(button)
                    })
        
        assert len(missing_tooltips) == 0, f"Buttons missing tooltips: {missing_tooltips}"
    
    def test_tooltip_consistency(self, template_files):
        """Test that similar buttons have consistent tooltip patterns"""
        button_patterns = {}
        
        for template_file in template_files:
            soup = self.parse_html_file(template_file)
            buttons = soup.find_all('button')
            
            for button in buttons:
                button_text = button.get_text(strip=True)
                button_id = button.get('id')
                title = button.get('title', '')
                
                # Group buttons by common patterns
                if 'send' in str(button_id).lower() or '⬆' in button_text or '✨' in button_text or 'send' in button_text.lower():
                    pattern_key = 'send_button'
                elif 'mic' in str(button_id).lower() or '🎤' in button_text:
                    pattern_key = 'mic_button'
                elif 'close' in str(button_id).lower() or '×' in button_text or '&times;' in str(button):
                    pattern_key = 'close_button'
                else:
                    pattern_key = f"other_{button_id or 'unnamed'}"
                
                if pattern_key not in button_patterns:
                    button_patterns[pattern_key] = []
                
                button_patterns[pattern_key].append({
                    'file': template_file.name,
                    'title': title,
                    'button_id': button_id,
                    'button_text': button_text
                })
        
        # Check consistency within each pattern group
        inconsistencies = []
        for pattern, buttons in button_patterns.items():
            if len(buttons) > 1:
                titles = [b['title'].lower() for b in buttons if b['title']]
                if len(set(titles)) > 1:  # More than one unique title
                    inconsistencies.append({
                        'pattern': pattern,
                        'buttons': buttons,
                        'unique_titles': list(set(titles))
                    })
        
        # Allow some variation in wording but check for major inconsistencies
        significant_inconsistencies = []
        for inconsistency in inconsistencies:
            titles = inconsistency['unique_titles']
            # Check if titles are semantically similar (contain similar keywords)
            if len(titles) > 1:
                # For send buttons, expect variations of "send"
                if inconsistency['pattern'] == 'send_button':
                    if not all('send' in title for title in titles):
                        significant_inconsistencies.append(inconsistency)
                # For mic buttons, expect variations of "voice" or "input"
                elif inconsistency['pattern'] == 'mic_button':
                    if not all(any(word in title for word in ['voice', 'input']) for title in titles):
                        significant_inconsistencies.append(inconsistency)
                # For other patterns, just ensure they exist
                else:
                    if len([t for t in titles if t.strip()]) == 0:
                        significant_inconsistencies.append(inconsistency)
        
        assert len(significant_inconsistencies) == 0, f"Significant tooltip inconsistencies: {significant_inconsistencies}"
    
    def test_accessibility_attributes(self, template_files):
        """Test that buttons have proper accessibility attributes"""
        accessibility_issues = []
        
        for template_file in template_files:
            soup = self.parse_html_file(template_file)
            buttons = soup.find_all('button')
            
            for button in buttons:
                button_id = button.get('id', 'unnamed')
                issues = []
                
                # Check for aria-label or descriptive text
                has_aria_label = button.get('aria-label') is not None
                has_title = button.get('title') is not None
                has_text_content = len(button.get_text(strip=True)) > 0
                
                # Icon-only buttons should have aria-label or title
                button_text = button.get_text(strip=True)
                is_icon_only = len(button_text) <= 2  # Likely emoji or single character
                
                if is_icon_only and not (has_aria_label or has_title):
                    issues.append("Icon-only button missing aria-label or title")
                
                # Check for proper button type for forms
                if button.find_parent('form') and not button.get('type'):
                    issues.append("Button in form missing type attribute")
                
                if issues:
                    accessibility_issues.append({
                        'file': template_file.name,
                        'button_id': button_id,
                        'button_html': str(button),
                        'issues': issues
                    })
        
        assert len(accessibility_issues) == 0, f"Accessibility issues found: {accessibility_issues}"
    
    def test_tooltip_content_quality(self, template_files):
        """Test that tooltip content is descriptive and helpful"""
        poor_tooltips = []
        
        for template_file in template_files:
            soup = self.parse_html_file(template_file)
            buttons = soup.find_all('button')
            
            for button in buttons:
                title = button.get('title', '')
                button_id = button.get('id', 'unnamed')
                
                if title:
                    # Check for minimum length
                    if len(title.strip()) < 3:
                        poor_tooltips.append({
                            'file': template_file.name,
                            'button_id': button_id,
                            'title': title,
                            'issue': 'Tooltip too short'
                        })
                    
                    # Check for generic words only
                    generic_words = ['click', 'button', 'here', 'this']
                    if title.lower().strip() in generic_words:
                        poor_tooltips.append({
                            'file': template_file.name,
                            'button_id': button_id,
                            'title': title,
                            'issue': 'Tooltip too generic'
                        })
                    
                    # Check for proper sentence structure (should start with capital or be descriptive)
                    if title and not (title[0].isupper() or title.lower().startswith(('send', 'create', 'copy', 'download', 'close', 'voice', 'talk'))):
                        poor_tooltips.append({
                            'file': template_file.name,
                            'button_id': button_id,
                            'title': title,
                            'issue': 'Tooltip should be properly formatted'
                        })
        
        assert len(poor_tooltips) == 0, f"Poor quality tooltips found: {poor_tooltips}"
    
    def test_tooltip_html_structure(self, template_files):
        """Test that tooltips are properly structured in HTML"""
        html_issues = []
        
        for template_file in template_files:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all button tags with regex to check HTML structure
            button_pattern = r'<button[^>]*>'
            buttons = re.findall(button_pattern, content, re.IGNORECASE)
            
            for button_html in buttons:
                # Check that title attribute is properly quoted
                if 'title=' in button_html.lower():
                    # Extract title attribute value
                    title_match = re.search(r'title=(["\'])(.*?)\1', button_html, re.IGNORECASE)
                    if not title_match:
                        # Title exists but not properly quoted
                        html_issues.append({
                            'file': template_file.name,
                            'button_html': button_html,
                            'issue': 'Title attribute not properly quoted'
                        })
                    else:
                        title_value = title_match.group(2)
                        # Check for HTML entities in title
                        if '&' in title_value and not any(entity in title_value for entity in ['&amp;', '&lt;', '&gt;', '&quot;', '&#']):
                            html_issues.append({
                                'file': template_file.name,
                                'button_html': button_html,
                                'issue': 'Unescaped HTML entities in title'
                            })
        
        assert len(html_issues) == 0, f"HTML structure issues found: {html_issues}"


if __name__ == '__main__':
    # Run tests directly
    pytest.main([__file__, '-v'])
