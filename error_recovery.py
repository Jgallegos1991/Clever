"""
Error Recovery System - Intelligent error handling and self-healing for Clever AI
"""

import traceback
import sys
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from debug_config import get_debugger, debug_method

class ErrorRecoverySystem:
    """Handles errors intelligently and attempts self-healing"""
    
    def __init__(self):
        self.debugger = get_debugger()
        self.error_history = []
        self.recovery_strategies = {}
        self.max_recovery_attempts = 3
        self.recovery_cooldown = 60  # seconds
        
        # Track recovery attempts
        self.recovery_attempts = {}
        
        self.debugger.info('error_recovery', 'Error Recovery System initialized')
        self._register_default_strategies()
    
    def _register_default_strategies(self):
        """Register default recovery strategies"""
        
        # Database connection errors
        self.register_strategy(
            'database_connection_error',
            self._recover_database_connection,
            ['connection', 'database', 'sqlite']
        )
        
        # NLP model loading errors
        self.register_strategy(
            'nlp_model_error',
            self._recover_nlp_models,
            ['spacy', 'model', 'load', 'nlp']
        )
        
        # Memory errors
        self.register_strategy(
            'memory_error',
            self._recover_memory_issues,
            ['memory', 'ram', 'allocation']
        )
        
        # File system errors
        self.register_strategy(
            'file_system_error',
            self._recover_file_system,
            ['file', 'directory', 'permission', 'path']
        )
        
        # Import errors
        self.register_strategy(
            'import_error',
            self._recover_import_issues,
            ['import', 'module', 'package']
        )
    
    @debug_method('error_recovery')
    def register_strategy(self, name: str, recovery_func: Callable, keywords: List[str]):
        """Register a recovery strategy"""
        self.recovery_strategies[name] = {
            'function': recovery_func,
            'keywords': keywords,
            'success_count': 0,
            'failure_count': 0
        }
        self.debugger.debug('error_recovery', f'Registered recovery strategy: {name}')
    
    @debug_method('error_recovery')
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle an error with intelligent recovery"""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        self.debugger.error('error_recovery', 'Error occurred', error, {'context': context})
        
        # Add to error history
        self.error_history.append(error_info)
        
        # Identify recovery strategy
        strategy = self._identify_strategy(error_info)
        
        recovery_result = {
            'error_info': error_info,
            'strategy_used': strategy,
            'recovery_attempted': False,
            'recovery_successful': False,
            'recovery_message': None
        }
        
        if strategy:
            recovery_result.update(self._attempt_recovery(strategy, error_info))
        else:
            self.debugger.warning('error_recovery', 'No recovery strategy found for error', {
                'error_type': error_info['error_type']
            })
        
        return recovery_result
    
    def _identify_strategy(self, error_info: Dict[str, Any]) -> Optional[str]:
        """Identify appropriate recovery strategy"""
        error_text = f"{error_info['error_type']} {error_info['error_message']} {error_info['traceback']}".lower()
        
        # Score strategies based on keyword matches
        strategy_scores = {}
        for strategy_name, strategy_info in self.recovery_strategies.items():
            score = 0
            for keyword in strategy_info['keywords']:
                if keyword.lower() in error_text:
                    score += 1
            
            if score > 0:
                # Boost score based on historical success
                success_rate = strategy_info['success_count'] / max(1, strategy_info['success_count'] + strategy_info['failure_count'])
                strategy_scores[strategy_name] = score * (1 + success_rate)
        
        # Return strategy with highest score
        if strategy_scores:
            best_strategy = max(strategy_scores.items(), key=lambda x: x[1])[0]
            self.debugger.debug('error_recovery', f'Selected strategy: {best_strategy}', {
                'scores': strategy_scores
            })
            return best_strategy
        
        return None
    
    def _attempt_recovery(self, strategy_name: str, error_info: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt recovery using specified strategy"""
        # Check cooldown
        last_attempt = self.recovery_attempts.get(strategy_name)
        if last_attempt and (datetime.now() - last_attempt).seconds < self.recovery_cooldown:
            return {
                'recovery_attempted': False,
                'recovery_successful': False,
                'recovery_message': f'Recovery strategy {strategy_name} in cooldown'
            }
        
        strategy_info = self.recovery_strategies[strategy_name]
        recovery_func = strategy_info['function']
        
        try:
            self.debugger.info('error_recovery', f'Attempting recovery with strategy: {strategy_name}')
            
            # Attempt recovery
            recovery_result = recovery_func(error_info)
            
            # Update tracking
            self.recovery_attempts[strategy_name] = datetime.now()
            
            if recovery_result.get('success', False):
                strategy_info['success_count'] += 1
                self.debugger.info('error_recovery', f'Recovery successful: {strategy_name}')
            else:
                strategy_info['failure_count'] += 1
                self.debugger.warning('error_recovery', f'Recovery failed: {strategy_name}')
            
            return {
                'recovery_attempted': True,
                'recovery_successful': recovery_result.get('success', False),
                'recovery_message': recovery_result.get('message', 'Recovery attempted')
            }
            
        except Exception as recovery_error:
            strategy_info['failure_count'] += 1
            self.debugger.error('error_recovery', f'Recovery strategy {strategy_name} failed', recovery_error)
            
            return {
                'recovery_attempted': True,
                'recovery_successful': False,
                'recovery_message': f'Recovery failed: {str(recovery_error)}'
            }
    
    def _recover_database_connection(self, error_info: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from database connection errors"""
        try:
            # Try to recreate database connection
            import sqlite3
            from knowledge_base import init_db
            
            # Wait a moment
            time.sleep(1)
            
            # Try to initialize database
            init_db()
            
            # Test connection
            conn = sqlite3.connect('clever.db')
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            conn.close()
            
            return {
                'success': True,
                'message': 'Database connection restored'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Database recovery failed: {str(e)}'
            }
    
    def _recover_nlp_models(self, error_info: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from NLP model loading errors"""
        try:
            # Try to reload spaCy model
            import spacy
            
            # Download model if missing
            try:
                nlp = spacy.load("en_core_web_sm")
            except OSError:
                # Model not found, try to download
                os.system("python -m spacy download en_core_web_sm")
                nlp = spacy.load("en_core_web_sm")
            
            # Test model
            doc = nlp("Test sentence")
            
            return {
                'success': True,
                'message': 'NLP models restored'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'NLP model recovery failed: {str(e)}'
            }
    
    def _recover_memory_issues(self, error_info: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from memory issues"""
        try:
            import gc
            
            # Force garbage collection
            gc.collect()
            
            # Clear caches if possible
            try:
                from functools import lru_cache
                # Clear any LRU caches
                for obj in gc.get_objects():
                    if hasattr(obj, 'cache_clear'):
                        obj.cache_clear()
            except:
                pass
            
            return {
                'success': True,
                'message': 'Memory cleanup performed'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Memory recovery failed: {str(e)}'
            }
    
    def _recover_file_system(self, error_info: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from file system errors"""
        try:
            # Create missing directories
            required_dirs = [
                'templates', 'static', 'uploads', 'logs',
                'Clever_Sync', 'synaptic_hub_sync'
            ]
            
            created_dirs = []
            for dir_name in required_dirs:
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name, exist_ok=True)
                    created_dirs.append(dir_name)
            
            message = f"Created missing directories: {created_dirs}" if created_dirs else "File system verified"
            
            return {
                'success': True,
                'message': message
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'File system recovery failed: {str(e)}'
            }
    
    def _recover_import_issues(self, error_info: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from import errors"""
        try:
            # Try to install missing packages
            error_message = error_info['error_message']
            
            # Extract package name from error
            if "No module named" in error_message:
                package_name = error_message.split("'")[1] if "'" in error_message else None
                
                if package_name:
                    # Try to install package
                    os.system(f"pip install {package_name}")
                    
                    # Try to import again
                    __import__(package_name)
                    
                    return {
                        'success': True,
                        'message': f'Installed missing package: {package_name}'
                    }
            
            return {
                'success': False,
                'message': 'Could not identify missing package'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Import recovery failed: {str(e)}'
            }
    
    @debug_method('error_recovery')
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error and recovery statistics"""
        # Recent errors (last 24 hours)
        recent_cutoff = datetime.now() - timedelta(hours=24)
        recent_errors = [
            error for error in self.error_history
            if datetime.fromisoformat(error['timestamp']) > recent_cutoff
        ]
        
        # Error types
        error_types = {}
        for error in recent_errors:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Strategy statistics
        strategy_stats = {}
        for name, info in self.recovery_strategies.items():
            total_attempts = info['success_count'] + info['failure_count']
            success_rate = info['success_count'] / max(1, total_attempts)
            strategy_stats[name] = {
                'total_attempts': total_attempts,
                'success_count': info['success_count'],
                'failure_count': info['failure_count'],
                'success_rate': success_rate
            }
        
        return {
            'total_errors': len(self.error_history),
            'recent_errors_24h': len(recent_errors),
            'error_types': error_types,
            'strategy_statistics': strategy_stats,
            'active_strategies': len(self.recovery_strategies)
        }

# Global error recovery system
_error_recovery = None

def get_error_recovery() -> ErrorRecoverySystem:
    """Get global error recovery system"""
    global _error_recovery
    if _error_recovery is None:
        _error_recovery = ErrorRecoverySystem()
    return _error_recovery

def handle_error_with_recovery(error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Convenience function to handle error with recovery"""
    recovery_system = get_error_recovery()
    return recovery_system.handle_error(error, context)
