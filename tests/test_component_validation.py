"""
Test Component Validation System

Why: Ensure the component validation catches CSS/HTML/JS mismatches that cause invisible UI
Where: Test suite for tools/validate_components.py and introspection component validation
How: Mock file contents and verify validation logic detects known mismatch patterns

Connects to:
    - tools/validate_components.py: ComponentValidator class being tested
    - introspection.py: validate_ui_components() function validation
    - tests/test_introspection.py: Integration with introspection system tests
"""
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
import sys

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from validate_components import ComponentValidator


class TestComponentValidator:
    """Test suite for ComponentValidator class"""
    
    def test_particle_system_validation_healthy(self):
        """
        Test particle system validation with matching IDs
        
        Why: Verify validator correctly identifies healthy component configurations
        Where: Unit test for particle system validation logic
        How: Mock consistent HTML/CSS/JS with matching canvas IDs
        """
        # Mock file contents with matching canvas ID
        html_content = '<canvas id="particles" width="100" height="100"></canvas>'
        css_content = '#particles { position: fixed; z-index: 9999; }'
        js_content = 'const canvas = document.getElementById("particles");'
        
        validator = ComponentValidator()
        
        with patch('pathlib.Path.read_text') as mock_read:
            with patch('pathlib.Path.exists', return_value=True):
                # Setup mock to return different content based on file
                def side_effect(encoding=None, errors=None):
                    if 'index.html' in str(mock_read.call_count):
                        return html_content
                    elif 'style.css' in str(mock_read.call_count):  
                        return css_content
                    else:
                        return js_content
                
                mock_read.side_effect = side_effect
                
                result = validator._validate_particle_system()
                
                assert result["status"] == "healthy"
                assert result["html_canvas_id"] == "particles"
                assert len(result["issues"]) == 0
    
    def test_particle_system_validation_css_mismatch(self):
        """
        Test particle system validation with CSS/HTML ID mismatch
        
        Why: Verify validator catches the exact issue that caused invisible particles
        Where: Unit test simulating the #particle-canvas vs id="particles" mismatch
        How: Mock HTML with "particles" ID but CSS with different selector
        """
        # Mock the exact mismatch that caused the original issue
        html_content = '<canvas id="particles" width="100" height="100"></canvas>'
        css_content = '#particle-canvas { position: fixed; z-index: 9999; }'  # Wrong selector!
        js_content = 'const canvas = document.getElementById("particles");'
        
        validator = ComponentValidator()
        
        with patch.object(validator.template_path, 'read_text', return_value=html_content):
            with patch.object(validator.css_path, 'read_text', return_value=css_content):
                with patch.object(validator.js_main_path, 'read_text', return_value=js_content):
                    with patch.object(validator.template_path, 'exists', return_value=True):
                        with patch.object(validator.css_path, 'exists', return_value=True):
                            with patch.object(validator.js_main_path, 'exists', return_value=True):
                                
                                result = validator._validate_particle_system()
                                
                                assert result["status"] == "error"
                                assert result["html_canvas_id"] == "particles"
                                
                                # Should detect CSS selector missing
                                issues = result["issues"]
                                assert len(issues) > 0
                                assert any("CSS missing selector" in issue["message"] for issue in issues)
    
    def test_z_index_hierarchy_validation(self):
        """
        Test z-index hierarchy validation detects conflicts
        
        Why: Ensure validator catches z-index conflicts that can hide UI elements
        Where: Unit test for z-index validation logic  
        How: Mock CSS with duplicate z-index values and verify conflict detection
        """
        # Mock CSS with z-index conflicts
        css_content = """
        #particles { z-index: 9999; }
        .chat-container { z-index: 9999; }  /* Duplicate! */
        #input-bar { z-index: 10; }
        """
        
        validator = ComponentValidator()
        
        with patch.object(validator.css_path, 'read_text', return_value=css_content):
            with patch.object(validator.css_path, 'exists', return_value=True):
                
                result = validator._validate_z_index_hierarchy()
                
                assert result["status"] == "warning"  # Should warn about conflicts
                assert len(result["conflicts"]) > 0
                
                # Should detect the duplicate z-index
                conflict = result["conflicts"][0]
                assert "Duplicate z-index 9999" in conflict["message"]
    
    def test_validation_file_missing(self):
        """
        Test validation handles missing template files gracefully
        
        Why: Ensure validator provides clear error messages for missing files
        Where: Error handling test for file system issues
        How: Mock missing template file and verify error response
        """
        validator = ComponentValidator()
        
        with patch.object(validator.template_path, 'exists', return_value=False):
            
            result = validator._validate_particle_system()
            
            assert result["status"] == "error" 
            assert "Template file not found" in result["message"]


def test_integration_with_introspection():
    """
    Test component validation integration with introspection system
    
    Why: Verify the introspection system properly includes component validation
    Where: Integration test between validate_components and introspection.py
    How: Import and call introspection validation to ensure it works
    """
    try:
        from introspection import validate_ui_components
        
        result = validate_ui_components()
        
        # Should return validation structure
        assert isinstance(result, dict)
        assert "canvas_particle_system" in result
        assert "timestamp" in result
        assert "overall_status" in result
        
    except ImportError:
        pytest.skip("introspection module not available")