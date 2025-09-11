#!/usr/bin/env python3
"""
Test script for sync_watcher.py functionality

Run this to validate that sync_watcher can be imported and basic functionality works.
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add current directory to path for imports
sys.path.insert(0, '.')

try:
    from sync_watcher import SyncEventHandler
    print("✅ sync_watcher.py imported successfully")
except ImportError as e:
    print(f"❌ Failed to import sync_watcher: {e}")
    sys.exit(1)

class TestSyncWatcher(unittest.TestCase):
    """Basic tests for sync_watcher functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.handler = SyncEventHandler("http://test:5000")
        
    def test_handler_creation(self):
        """Test that handler can be created"""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.flask_url, "http://test:5000")
        
    def test_debounce_logic(self):
        """Test that debouncing prevents rapid triggers"""
        import time
        
        # Create mock event
        mock_event = MagicMock()
        mock_event.is_directory = False
        mock_event.src_path = "/test/file.txt"
        
        # First call should work
        with patch.object(self.handler, 'trigger_ingestion') as mock_trigger:
            self.handler.on_any_event(mock_event)
            mock_trigger.assert_called_once()
            
        # Second call immediately should be debounced
        with patch.object(self.handler, 'trigger_ingestion') as mock_trigger:
            self.handler.on_any_event(mock_event)
            mock_trigger.assert_not_called()
            
    def test_ignore_directories(self):
        """Test that directory events are ignored"""
        mock_event = MagicMock()
        mock_event.is_directory = True
        
        with patch.object(self.handler, 'trigger_ingestion') as mock_trigger:
            self.handler.on_any_event(mock_event)
            mock_trigger.assert_not_called()
            
    def test_ignore_temp_files(self):
        """Test that temporary files are ignored"""
        temp_patterns = ['.tmp', '.swp', '~', '.DS_Store']
        
        for pattern in temp_patterns:
            with self.subTest(pattern=pattern):
                mock_event = MagicMock()
                mock_event.is_directory = False
                mock_event.src_path = f"/test/file{pattern}"
                
                with patch.object(self.handler, 'trigger_ingestion') as mock_trigger:
                    self.handler.on_any_event(mock_event)
                    mock_trigger.assert_not_called()

if __name__ == "__main__":
    print("Running sync_watcher tests...")
    unittest.main(verbosity=2)
