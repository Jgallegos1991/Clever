"""
Simple Evolution Engine for Clever AI

Why: Provides basic learning and interaction tracking without complex dependencies
Where: Tracks user interactions and system evolution
How: Simple logging and basic learning capabilities

Connects to:
    - app.py: Interaction logging from chat
    - database.py: Persistent storage via DB_PATH
"""
import time
from typing import Dict, Any, List
from datetime import datetime


class SimpleEvolutionEngine:
    """
    Simple evolution engine for interaction tracking
    
    Why: Track user interactions and system learning
    Where: Core component for system improvement
    How: Simple logging and basic pattern recognition
    """
    
    def __init__(self):
        """
        Initialize simple evolution engine
        
        Why: Set up basic tracking capabilities
        Where: Called once during system initialization
        How: Initialize interaction storage and basic metrics
        """
        self.interactions = []
        self.total_interactions = 0
        self.session_start = time.time()
        
    def log_interaction(self, interaction_data: Dict[str, Any]):
        """
        Log user interaction for learning
        
        Why: Track user patterns for system improvement
        Where: Called after each user interaction
        How: Store interaction data with timestamp
        
        Connects to:
            - app.py: Chat interaction logging
            - persona.py: Response mode tracking
        """
        interaction = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'data': interaction_data,
            'session_time': time.time() - self.session_start
        }
        
        self.interactions.append(interaction)
        self.total_interactions += 1
        
        # Keep only recent interactions to prevent memory issues
        if len(self.interactions) > 100:
            self.interactions = self.interactions[-50:]  # Keep last 50
    
    def get_interaction_summary(self) -> Dict[str, Any]:
        """
        Get summary of interaction patterns
        
        Why: Provide insights into user behavior
        Where: Used by monitoring and analytics
        How: Analyze stored interaction data
        """
        if not self.interactions:
            return {
                'total_interactions': 0,
                'session_duration': 0,
                'common_patterns': []
            }
        
        # Basic pattern analysis
        modes_used = []
        for interaction in self.interactions:
            if 'active_mode' in interaction.get('data', {}):
                modes_used.append(interaction['data']['active_mode'])
        
        mode_counts = {}
        for mode in modes_used:
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        
        return {
            'total_interactions': self.total_interactions,
            'session_duration': time.time() - self.session_start,
            'recent_interactions': len(self.interactions),
            'mode_usage': mode_counts,
            'common_patterns': list(mode_counts.keys())
        }
    
    def get_learning_insights(self) -> List[str]:
        """
        Get basic learning insights
        
        Why: Provide feedback on system adaptation
        Where: Used by monitoring and user interface
        How: Analyze interaction patterns for insights
        """
        insights = []
        
        if self.total_interactions == 0:
            insights.append("No interactions recorded yet")
            return insights
        
        summary = self.get_interaction_summary()
        
        if summary['total_interactions'] > 10:
            insights.append(f"Processed {summary['total_interactions']} interactions")
        
        if summary['mode_usage']:
            most_used = max(summary['mode_usage'], key=summary['mode_usage'].get)
            insights.append(f"Most used mode: {most_used}")
        
        session_minutes = summary['session_duration'] / 60
        if session_minutes > 5:
            insights.append(f"Active session: {session_minutes:.1f} minutes")
        
        return insights
    
    def reset_session(self):
        """
        Reset current session data
        
        Why: Allow clean session starts
        Where: Used for testing and session management
        How: Clear interaction data and reset timers
        """
        self.interactions = []
        self.session_start = time.time()


# Global evolution engine instance
_evolution_engine = None


def get_evolution_engine() -> SimpleEvolutionEngine:
    """
    Get global evolution engine instance
    
    Why: Provide singleton access across application
    Where: Used by all modules needing evolution tracking
    How: Create or return existing engine instance
    
    Connects to:
        - app.py: Main application evolution tracking
        - All modules: Universal evolution access
    """
    global _evolution_engine
    if _evolution_engine is None:
        _evolution_engine = SimpleEvolutionEngine()
    return _evolution_engine


def reset_evolution_engine():
    """
    Reset global evolution engine
    
    Why: Allow clean state for testing
    Where: Used in test cases
    How: Clear global engine variable
    """
    global _evolution_engine
    _evolution_engine = None