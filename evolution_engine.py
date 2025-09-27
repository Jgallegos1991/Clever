"""
Simple Evolution Engine for Clever AI

Why:
    Captures each interaction as a temporal arrow in the system's growth
    narrative—enabling retrospective analysis (patterns, mode usage) and future
    adaptive behaviors without introducing heavy external services. Light, fast,
    and memory-first to respect offline constraints.
Where:
    Positioned between the chat surface (`app.py`) and deeper analytics: it is
    invoked post-response generation to log context and mode, feeding telemetry
    into both memory insights and runtime introspection (`runtime_state.evolution`).
How:
    Maintains an in-memory rolling list plus counters, offering summary methods
    for quick dashboards. Interaction objects carry timestamps, raw data, and
    session-relative timing. Persistence (if/when needed) flows through the
    database layer—keeping this engine side-effect minimal.

Connects to:
    - app.py:
        - `chat()` -> `log_interaction()`: The main chat endpoint calls this to log every user interaction, forming the basis of Clever's learning.
    - persona.py: The `PersonaResponse` object created in `persona.py` provides the `mode` and `sentiment` data that is passed into `log_interaction()`.
    - database.py: While currently memory-first, the design intends for this engine to persist its learned data and interaction logs to the database for long-term growth.
    - introspection.py:
        - `runtime_state()` -> `get_evolution_engine()`: The runtime introspection system calls this module to get a summary of interaction counts for the debug overlay.
    - health_monitor.py:
        - `check_evolution_engine()` -> `get_evolution_engine()`: The health monitor accesses this engine to check its status and report on learning progress.
"""
import time
from datetime import datetime
from typing import Dict, List, Any, Optional


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