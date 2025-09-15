"""
<<<<<<< HEAD
from database import DatabaseManager
=======
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
Automated Testing System - Comprehensive test runner and validation for Clever AI
"""

import unittest
import sys
import os
import time
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional
from debug_config import get_debugger, debug_method

class CleverTestSuite:
    """Comprehensive test suite for Clever AI components"""
    
    def __init__(self):
        self.debugger = get_debugger()
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        
        self.debugger.info('test_suite', 'Clever Test Suite initialized')
    
    @debug_method('test_suite')
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test categories"""
        self.start_time = datetime.now()
        self.debugger.info('test_suite', 'Starting comprehensive test suite')
        
        test_categories = [
            ('database_tests', self.test_database_components),
            ('nlp_tests', self.test_nlp_components),
            ('evolution_tests', self.test_evolution_engine),
            ('persona_tests', self.test_persona_system),
            ('file_processing_tests', self.test_file_processing),
            ('api_tests', self.test_api_endpoints),
            ('ui_tooltip_tests', self.test_ui_tooltips),
            ('integration_tests', self.test_integration)
        ]
        
        overall_status = 'passed'
        total_tests = 0
        passed_tests = 0
        
        for category_name, test_func in test_categories:
            try:
                self.debugger.info('test_suite', f'Running {category_name}')
                category_result = test_func()
                self.test_results[category_name] = category_result
                
                total_tests += category_result.get('total', 0)
                passed_tests += category_result.get('passed', 0)
                
                if category_result.get('status') != 'passed':
                    overall_status = 'failed'
                    
            except Exception as e:
                self.debugger.error('test_suite', f'Test category {category_name} failed', e)
                self.test_results[category_name] = {
                    'status': 'error',
                    'error': str(e),
                    'total': 0,
                    'passed': 0,
                    'failed': 1
                }
                overall_status = 'failed'
        
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        summary = {
            'overall_status': overall_status,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / max(1, total_tests)) * 100,
            'duration_seconds': duration,
            'timestamp': self.end_time.isoformat(),
            'categories': self.test_results
        }
        
        self.debugger.info('test_suite', f'Test suite complete: {passed_tests}/{total_tests} passed', {
            'success_rate': summary['success_rate'],
            'duration': duration
        })
        
        return summary
    
    def test_database_components(self) -> Dict[str, Any]:
        """Test database functionality"""
        tests = []
        
        # Test 1: Database connection
        try:
<<<<<<< HEAD
            from config import DB_PATH
            from database import DatabaseManager
            with DatabaseManager(DB_PATH)._connect() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT 1')
=======
            conn = sqlite3.connect('clever.db')
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            tests.append({'name': 'database_connection', 'status': 'passed'})
        except Exception as e:
            tests.append({'name': 'database_connection', 'status': 'failed', 'error': str(e)})
        
        # Test 2: Table existence
        try:
            from knowledge_base import init_db
            init_db()
            
<<<<<<< HEAD
            from config import DB_PATH
            conn = with DatabaseManager(DB_PATH)._connect() as conn:
=======
            conn = sqlite3.connect('clever.db')
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            cursor = conn.cursor()
            
            required_tables = [
                'interactions', 'knowledge_sources', 'content_chunks',
                'user_preferences', 'personality_state', 'system_metrics'
            ]
            
            for table in required_tables:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if cursor.fetchone():
                    tests.append({'name': f'table_{table}_exists', 'status': 'passed'})
                else:
                    tests.append({'name': f'table_{table}_exists', 'status': 'failed', 'error': 'Table not found'})
            
            conn.close()
            
        except Exception as e:
            tests.append({'name': 'table_verification', 'status': 'failed', 'error': str(e)})
        
        # Test 3: Basic CRUD operations
        try:
            from knowledge_base import log_interaction, get_recent_interactions
            
            # Test insert
            log_interaction(
                user_message="Test message",
                clever_response="Test response",
                intent_detected="test",
                sentiment_compound=0.5,
                nlp_analysis={"test": True}
            )
            
            # Test read
            recent = get_recent_interactions(limit=1)
            if recent and len(recent) > 0:
                tests.append({'name': 'crud_operations', 'status': 'passed'})
            else:
                tests.append({'name': 'crud_operations', 'status': 'failed', 'error': 'No data retrieved'})
                
        except Exception as e:
            tests.append({'name': 'crud_operations', 'status': 'failed', 'error': str(e)})
        
        # Calculate results
        passed = sum(1 for test in tests if test['status'] == 'passed')
        total = len(tests)
        
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': tests
        }
    
    def test_nlp_components(self) -> Dict[str, Any]:
        """Test NLP functionality"""
        tests = []
        
        # Test 1: spaCy model loading
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            doc = nlp("This is a test sentence.")
            tests.append({'name': 'spacy_model_loading', 'status': 'passed'})
        except Exception as e:
            tests.append({'name': 'spacy_model_loading', 'status': 'failed', 'error': str(e)})
        
        # Test 2: VADER sentiment analysis
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            analyzer = SentimentIntensityAnalyzer()
            scores = analyzer.polarity_scores("This is a great day!")
            if 'compound' in scores and isinstance(scores['compound'], (int, float)):
                tests.append({'name': 'vader_sentiment', 'status': 'passed'})
            else:
                tests.append({'name': 'vader_sentiment', 'status': 'failed', 'error': 'Invalid sentiment scores'})
        except Exception as e:
            tests.append({'name': 'vader_sentiment', 'status': 'failed', 'error': str(e)})
        
        # Test 3: TextBlob functionality
        try:
            from textblob import TextBlob
            blob = TextBlob("This is a wonderful day.")
            polarity = blob.sentiment.polarity
            if isinstance(polarity, (int, float)):
                tests.append({'name': 'textblob_sentiment', 'status': 'passed'})
            else:
                tests.append({'name': 'textblob_sentiment', 'status': 'failed', 'error': 'Invalid polarity score'})
        except Exception as e:
            tests.append({'name': 'textblob_sentiment', 'status': 'failed', 'error': str(e)})
        
        # Test 4: NLP Processor integration
        try:
            from nlp_processor import analyze_text
            analysis = analyze_text("Jay is feeling great today!")
            
            required_keys = ['entities', 'sentiment', 'keywords', 'intent_hints']
            if all(key in analysis for key in required_keys):
                tests.append({'name': 'nlp_processor_integration', 'status': 'passed'})
            else:
                tests.append({'name': 'nlp_processor_integration', 'status': 'failed', 'error': 'Missing analysis keys'})
        except Exception as e:
            tests.append({'name': 'nlp_processor_integration', 'status': 'failed', 'error': str(e)})
        
        # Calculate results
        passed = sum(1 for test in tests if test['status'] == 'passed')
        total = len(tests)
        
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': tests
        }
    
    def test_evolution_engine(self) -> Dict[str, Any]:
        """Test evolution engine functionality"""
        tests = []
        
        # Test 1: Evolution engine initialization
        try:
            from evolution_engine import get_evolution_engine
            engine = get_evolution_engine()
            tests.append({'name': 'evolution_engine_init', 'status': 'passed'})
        except Exception as e:
            tests.append({'name': 'evolution_engine_init', 'status': 'failed', 'error': str(e)})
        
        # Test 2: Learning from interaction
        try:
            from evolution_engine import get_evolution_engine
            engine = get_evolution_engine()
            
            # Simulate learning
            engine.learn_from_interaction(
                user_input="Test learning",
                clever_response="Learning response",
                context={"test": True}
            )
            tests.append({'name': 'learning_interaction', 'status': 'passed'})
        except Exception as e:
            tests.append({'name': 'learning_interaction', 'status': 'failed', 'error': str(e)})
        
        # Test 3: Evolution status retrieval
        try:
            from evolution_engine import get_evolution_engine
            engine = get_evolution_engine()
            status = engine.get_evolution_status()
            
            if isinstance(status, dict) and 'evolution_score' in status:
                tests.append({'name': 'evolution_status', 'status': 'passed'})
            else:
                tests.append({'name': 'evolution_status', 'status': 'failed', 'error': 'Invalid status format'})
        except Exception as e:
            tests.append({'name': 'evolution_status', 'status': 'failed', 'error': str(e)})
        
        # Calculate results
        passed = sum(1 for test in tests if test['status'] == 'passed')
        total = len(tests)
        
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': tests
        }
    
    def test_persona_system(self) -> Dict[str, Any]:
        """Test persona system functionality"""
        tests = []
        
        # Test 1: Persona loading
        try:
            from persona import PERSONA, get_greeting
            if isinstance(PERSONA, dict) and 'traits' in PERSONA:
                tests.append({'name': 'persona_loading', 'status': 'passed'})
            else:
                tests.append({'name': 'persona_loading', 'status': 'failed', 'error': 'Invalid persona format'})
        except Exception as e:
            tests.append({'name': 'persona_loading', 'status': 'failed', 'error': str(e)})
        
        # Test 2: Greeting generation
        try:
            from persona import get_greeting
            greeting = get_greeting()
            if isinstance(greeting, str) and len(greeting) > 0:
                tests.append({'name': 'greeting_generation', 'status': 'passed'})
            else:
                tests.append({'name': 'greeting_generation', 'status': 'failed', 'error': 'Invalid greeting'})
        except Exception as e:
            tests.append({'name': 'greeting_generation', 'status': 'failed', 'error': str(e)})
        
        # Test 3: Dynamic response generation
        try:
            from persona import get_dynamic_response
            response = get_dynamic_response(
                user_input="Hello Clever",
                analysis={'sentiment': {'compound': 0.5}},
                context={}
            )
            if isinstance(response, str) and len(response) > 0:
                tests.append({'name': 'dynamic_response', 'status': 'passed'})
            else:
                tests.append({'name': 'dynamic_response', 'status': 'failed', 'error': 'Invalid response'})
        except Exception as e:
            tests.append({'name': 'dynamic_response', 'status': 'failed', 'error': str(e)})
        
        # Calculate results
        passed = sum(1 for test in tests if test['status'] == 'passed')
        total = len(tests)
        
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': tests
        }
    
    def test_file_processing(self) -> Dict[str, Any]:
        """Test file processing functionality"""
        tests = []
        
        # Test 1: File ingestor import
        try:
            from file_ingestor import process_text_file, process_uploaded_file
            tests.append({'name': 'file_ingestor_import', 'status': 'passed'})
        except Exception as e:
            tests.append({'name': 'file_ingestor_import', 'status': 'failed', 'error': str(e)})
        
        # Test 2: Text file processing
        try:
            # Create a test file
            test_content = "This is a test file for processing.\nIt has multiple lines.\nAnd should be chunked properly."
            test_file_path = "test_file.txt"
            
            with open(test_file_path, 'w') as f:
                f.write(test_content)
            
            from file_ingestor import process_text_file
            result = process_text_file(test_file_path)
            
            # Cleanup
            os.remove(test_file_path)
            
            if result and isinstance(result, dict):
                tests.append({'name': 'text_file_processing', 'status': 'passed'})
            else:
                tests.append({'name': 'text_file_processing', 'status': 'failed', 'error': 'Invalid processing result'})
        except Exception as e:
            tests.append({'name': 'text_file_processing', 'status': 'failed', 'error': str(e)})
        
        # Calculate results
        passed = sum(1 for test in tests if test['status'] == 'passed')
        total = len(tests)
        
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': tests
        }
    
    def test_api_endpoints(self) -> Dict[str, Any]:
        """Test API endpoints (requires running Flask app)"""
        tests = []
        
        # Note: These tests would require the Flask app to be running
        # For now, just test that the Flask app can be imported
        try:
            from app import app
            tests.append({'name': 'flask_app_import', 'status': 'passed'})
        except Exception as e:
            tests.append({'name': 'flask_app_import', 'status': 'failed', 'error': str(e)})
        
        # Calculate results
        passed = sum(1 for test in tests if test['status'] == 'passed')
        total = len(tests)
        
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': tests
        }
    
    def test_ui_tooltips(self) -> Dict[str, Any]:
        """Test UI tooltip functionality"""
        tests = []
        
        # Test 1: Import UI tooltip test module
        try:
            from tests.test_ui_functionality import run_ui_tooltip_tests
            tests.append({'name': 'ui_tooltip_module_import', 'status': 'passed'})
        except Exception as e:
            tests.append({'name': 'ui_tooltip_module_import', 'status': 'failed', 'error': str(e)})
            # Return early if we can't import the module
            return {
                'status': 'failed',
                'total': 1,
                'passed': 0,
                'failed': 1,
                'tests': tests
            }
        
        # Test 2: Run tooltip tests
        try:
            from tests.test_ui_functionality import run_ui_tooltip_tests
            tooltip_results = run_ui_tooltip_tests()
            
            if tooltip_results.get('status') == 'passed':
                tests.append({'name': 'tooltip_functionality', 'status': 'passed', 'details': tooltip_results})
            else:
                tests.append({'name': 'tooltip_functionality', 'status': 'failed', 'details': tooltip_results})
        except Exception as e:
            tests.append({'name': 'tooltip_functionality', 'status': 'failed', 'error': str(e)})
        
        # Test 3: Template files exist
        try:
            import os
            templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
            if os.path.exists(templates_dir):
                html_files = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
                if len(html_files) > 0:
                    tests.append({'name': 'template_files_exist', 'status': 'passed', 'count': len(html_files)})
                else:
                    tests.append({'name': 'template_files_exist', 'status': 'failed', 'error': 'No HTML templates found'})
            else:
                tests.append({'name': 'template_files_exist', 'status': 'failed', 'error': 'Templates directory not found'})
        except Exception as e:
            tests.append({'name': 'template_files_exist', 'status': 'failed', 'error': str(e)})
        
        # Calculate results
        passed = sum(1 for test in tests if test['status'] == 'passed')
        total = len(tests)
        
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': tests
        }
    
    def test_integration(self) -> Dict[str, Any]:
        """Test system integration"""
        tests = []
        
        # Test 1: Full processing pipeline
        try:
            from nlp_processor import analyze_text
            from persona import get_dynamic_response
            from knowledge_base import log_interaction
            
            # Simulate full interaction
            user_input = "Hello Clever, how are you today?"
            analysis = analyze_text(user_input)
            response = get_dynamic_response(user_input, analysis, {})
            
            # Log interaction
            log_interaction(
                user_message=user_input,
                clever_response=response,
                intent_detected=analysis.get('intent_hints', {}).get('primary', 'unknown'),
                sentiment_compound=analysis.get('sentiment', {}).get('compound', 0),
                nlp_analysis=analysis
            )
            
            tests.append({'name': 'full_processing_pipeline', 'status': 'passed'})
            
        except Exception as e:
            tests.append({'name': 'full_processing_pipeline', 'status': 'failed', 'error': str(e)})
        
        # Calculate results
        passed = sum(1 for test in tests if test['status'] == 'passed')
        total = len(tests)
        
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': tests
        }

# Global test suite
_test_suite = None

def get_test_suite() -> CleverTestSuite:
    """Get global test suite instance"""
    global _test_suite
    if _test_suite is None:
        _test_suite = CleverTestSuite()
    return _test_suite

def run_quick_tests() -> Dict[str, Any]:
    """Run a quick subset of tests"""
    suite = get_test_suite()
    
    # Run only critical tests
    critical_tests = {
        'database': suite.test_database_components(),
        'nlp': suite.test_nlp_components(),
        'persona': suite.test_persona_system()
    }
    
    total_passed = sum(result['passed'] for result in critical_tests.values())
    total_tests = sum(result['total'] for result in critical_tests.values())
    
    return {
        'status': 'passed' if total_passed == total_tests else 'failed',
        'total_tests': total_tests,
        'passed_tests': total_passed,
        'success_rate': (total_passed / max(1, total_tests)) * 100,
        'results': critical_tests
    }
