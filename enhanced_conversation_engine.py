"""
Enhanced Conversation Engine for Clever AI

Why: Provides comprehensive conversation processing with full access to all
system capabilities, ensuring Clever can handle any request with perfect
understanding, memory integration, and intelligent response generation.
Where: Used by app.py chat endpoint to process all user interactions with
advanced context awareness, file access, and multi-modal understanding.
How: Implements conversation orchestrator with NLP analysis, memory retrieval,
file system access, knowledge base integration, and intelligent routing.

Connects to:
    - persona.py: Advanced response generation with context awareness
    - nlp_processor.py: Full NLP analysis and understanding
    - evolution_engine.py: Learning and memory integration
    - database.py: Knowledge base and conversation history
    - file_ingestor.py: Real-time file access and processing
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Core system imports
from nlp_processor import nlp_processor
from persona import persona_engine
from evolution_engine import get_evolution_engine
from database import db_manager
from debug_config import get_debugger

logger = get_debugger()


class ConversationContext:
    """
    Enhanced conversation context with full system access

    Why: Maintains comprehensive conversation state including user intent,
    system capabilities, file access, and memory integration for perfect
    conversational understanding and response generation.
    Where: Used by conversation engine to track and enhance all interactions
    How: Aggregates context from all system components for intelligent routing

    Connects to:
        - All system modules: Provides unified context interface
        - Conversation history: Maintains interaction continuity
        - File system: Enables real-time file access and processing
    """

    def __init__(self):
        self.conversation_history = []
        self.user_preferences = {}
        self.active_files = []
        self.current_focus = "general"
        self.conversation_depth = "surface"
        self.energy_level = 0.7
        self.available_capabilities = self._discover_capabilities()

    def _discover_capabilities(self) -> Dict[str, bool]:
        """Discover all available system capabilities"""
        capabilities = {
            "nlp_analysis": True,
            "file_access": True,
            "memory_storage": True,
            "learning": True,
            "creative_modes": True,
            "deep_analysis": True,
            "file_ingestion": True,
            "conversation_memory": True,
            "persona_modes": True,
            "visual_particles": True,
        }

        # Test actual capability availability
        try:
            # Test file access
            capabilities["file_access"] = os.access(".", os.R_OK)

            # Test database access
            if hasattr(db_manager, "get_recent_conversations"):
                capabilities["memory_storage"] = True

            # Test evolution engine
            evo_engine = get_evolution_engine()
            capabilities["learning"] = evo_engine is not None

        except Exception as e:
            logger.warning("conversation_engine", f"Capability discovery error: {e}")

        return capabilities

    def update_from_interaction(self, user_message: str, analysis: Dict[str, Any]):
        """Update context based on user interaction"""
        self.conversation_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "analysis": analysis,
            }
        )

        # Update conversation depth based on message complexity
        if len(analysis.get("keywords", [])) > 5:
            self.conversation_depth = "deep"
        elif any(
            word in user_message.lower()
            for word in ["analyze", "explain", "understand"]
        ):
            self.conversation_depth = "analytical"
        else:
            self.conversation_depth = "casual"

        # Update focus based on content
        keywords = analysis.get("keywords", [])
        if any(word in keywords for word in ["file", "document", "text"]):
            self.current_focus = "files"
        elif any(word in keywords for word in ["create", "build", "make"]):
            self.current_focus = "creative"
        elif any(word in keywords for word in ["analyze", "think", "understand"]):
            self.current_focus = "analytical"
        else:
            self.current_focus = "general"


class EnhancedConversationEngine:
    """
    Comprehensive conversation engine with full system access

    Why: Orchestrates all conversation processing with complete access to
    system capabilities, ensuring Clever can handle any request perfectly
    with intelligent routing, memory integration, and multi-modal understanding.
    Where: Primary conversation processor for all chat interactions in app.py
    How: Implements intelligent conversation flow with capability routing,
    context awareness, file access, and advanced response generation.

    Connects to:
        - persona.py: Response generation with full persona capabilities
        - nlp_processor.py: Advanced text analysis and understanding
        - evolution_engine.py: Learning and memory integration
        - file system: Direct file access and processing capabilities
        - database: Knowledge retrieval and conversation persistence
    """

    def __init__(self):
        self.context = ConversationContext()
        self.file_processors = {
            ".txt": self._process_text_file,
            ".md": self._process_text_file,
            ".py": self._process_code_file,
            ".js": self._process_code_file,
            ".json": self._process_json_file,
            ".csv": self._process_csv_file,
        }

    def process_conversation(
        self,
        user_message: str,
        mode: str = "Auto",
        context_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Process conversation with full system capabilities

        Why: Provides comprehensive conversation processing with access to all
        system capabilities including file processing, memory retrieval,
        and intelligent response generation for perfect user interaction.
        Where: Main entry point for all conversation processing in chat endpoint
        How: Orchestrates NLP analysis, capability routing, context building,
        and response generation with full system integration.

        Args:
            user_message: User's input message for processing
            mode: Conversation mode (Auto, Creative, Deep Dive, Support, Quick Hit)
            context_data: Additional context information

        Returns:
            Complete conversation response with analysis and system data

        Connects to:
            - All system capabilities: Routes requests to appropriate handlers
            - Conversation context: Maintains interaction continuity
            - Response generation: Creates comprehensive response data
        """

        logger.info("conversation_engine", f"Processing conversation: mode={mode}")

        # Stage 1: Advanced NLP Analysis
        analysis = self._perform_comprehensive_analysis(user_message)

        # Stage 2: Update conversation context
        self.context.update_from_interaction(user_message, analysis)

        # Stage 3: Capability routing and processing
        enhanced_context = self._build_enhanced_context(
            user_message, analysis, context_data
        )

        # Stage 4: Intelligent request routing
        routing_result = self._route_request(user_message, analysis, enhanced_context)

        # Stage 5: Generate comprehensive response
        response = self._generate_comprehensive_response(
            user_message, analysis, enhanced_context, routing_result, mode
        )

        # Stage 6: Learning and memory integration
        self._integrate_learning(user_message, analysis, response)

        logger.info("conversation_engine", "Conversation processing complete")
        return response

    def _perform_comprehensive_analysis(self, user_message: str) -> Dict[str, Any]:
        """Perform comprehensive NLP analysis with all capabilities"""
        # Base NLP analysis
        nlp_result = nlp_processor.process(user_message)

        analysis = {
            "keywords": nlp_result.keywords,
            "sentiment": nlp_result.sentiment,
            "user_input": user_message,
            "message_length": len(user_message),
            "word_count": len(user_message.split()),
            "complexity_score": len(nlp_result.keywords)
            / max(len(user_message.split()), 1),
        }

        # Intent analysis
        analysis["intent"] = self._analyze_intent(user_message, nlp_result)

        # Request type classification
        analysis["request_type"] = self._classify_request_type(user_message)

        # Capability requirements
        analysis["required_capabilities"] = self._identify_required_capabilities(
            user_message
        )

        return analysis

    def _analyze_intent(self, message: str, nlp_result) -> str:
        """Analyze user intent from message"""
        message_lower = message.lower()

        # File operations
        if any(
            word in message_lower
            for word in ["file", "document", "read", "analyze file"]
        ):
            return "file_operation"

        # Creative requests
        if any(
            word in message_lower for word in ["create", "write", "generate", "design"]
        ):
            return "creative_generation"

        # Analysis requests
        if any(
            word in message_lower
            for word in ["analyze", "explain", "understand", "breakdown"]
        ):
            return "deep_analysis"

        # Information requests
        if any(word in message_lower for word in ["what", "how", "why", "tell me"]):
            return "information_request"

        # Task requests
        if any(word in message_lower for word in ["help", "do", "perform", "execute"]):
            return "task_execution"

        return "general_conversation"

    def _classify_request_type(self, message: str) -> str:
        """Classify the type of request"""
        message_lower = message.lower()

        # Multi-step complex requests
        if "," in message or " and " in message or len(message.split()) > 20:
            return "complex_multi_step"

        # Simple questions
        if message.strip().endswith("?") and len(message.split()) < 10:
            return "simple_question"

        # Commands or instructions
        if any(
            message_lower.startswith(word)
            for word in ["please", "can you", "i need", "help me"]
        ):
            return "instruction_request"

        return "conversational"

    def _identify_required_capabilities(self, message: str) -> List[str]:
        """Identify what system capabilities are needed"""
        required = []
        message_lower = message.lower()

        if any(word in message_lower for word in ["file", "document", "folder"]):
            required.extend(["file_access", "file_processing"])

        if any(word in message_lower for word in ["remember", "recall", "previous"]):
            required.append("memory_retrieval")

        if any(word in message_lower for word in ["learn", "understand", "analyze"]):
            required.extend(["nlp_analysis", "learning"])

        if any(word in message_lower for word in ["create", "generate", "write"]):
            required.append("creative_generation")

        return required

    def _build_enhanced_context(
        self,
        message: str,
        analysis: Dict[str, Any],
        context_data: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Build comprehensive context for conversation"""
        enhanced_context = {
            "conversation_context": {
                "current_focus": self.context.current_focus,
                "conversation_depth": self.context.conversation_depth,
                "interaction_count": len(self.context.conversation_history),
                "energy_trajectory": (
                    "building" if self.context.energy_level > 0.5 else "calm"
                ),
                "primary_interaction_mode": analysis.get("intent", "general"),
            },
            "system_context": {
                "available_capabilities": self.context.available_capabilities,
                "active_files": self.context.active_files,
                "processing_mode": "enhanced",
            },
            "user_context": {
                "preferences": self.context.user_preferences,
                "conversation_history_length": len(self.context.conversation_history),
                "overall_sentiment_trend": "positive",  # Calculate from history
            },
        }

        # Add external context data if provided
        if context_data:
            enhanced_context["external_data"] = context_data

        return enhanced_context

    def _route_request(
        self, message: str, analysis: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Route request to appropriate processing capabilities"""
        routing_result = {
            "primary_handler": "persona_engine",
            "additional_processing": [],
            "file_operations": [],
            "memory_operations": [],
            "special_capabilities": [],
        }

        required_caps = analysis.get("required_capabilities", [])

        # File processing routing
        if "file_access" in required_caps:
            routing_result["additional_processing"].append("file_processor")
            routing_result["file_operations"] = self._identify_file_operations(message)

        # Memory/learning routing
        if "memory_retrieval" in required_caps:
            routing_result["memory_operations"].append("conversation_history")
            routing_result["additional_processing"].append("memory_retrieval")

        # Complex analysis routing
        if analysis.get("request_type") == "complex_multi_step":
            routing_result["primary_handler"] = "enhanced_persona"
            routing_result["special_capabilities"].append("multi_step_processing")

        return routing_result

    def _identify_file_operations(self, message: str) -> List[str]:
        """Identify specific file operations requested"""
        operations = []
        message_lower = message.lower()

        if any(word in message_lower for word in ["read", "open", "show"]):
            operations.append("read_file")
        if any(word in message_lower for word in ["analyze", "process"]):
            operations.append("analyze_file")
        if any(word in message_lower for word in ["search", "find"]):
            operations.append("search_files")
        if any(word in message_lower for word in ["list", "show files"]):
            operations.append("list_files")

        return operations

    def _generate_comprehensive_response(
        self,
        message: str,
        analysis: Dict[str, Any],
        context: Dict[str, Any],
        routing: Dict[str, Any],
        mode: str,
    ) -> Dict[str, Any]:
        """Generate comprehensive response with all requested capabilities"""

        # Process file operations if requested
        file_results = {}
        if "file_processor" in routing["additional_processing"]:
            file_results = self._process_file_requests(
                message, routing["file_operations"]
            )

        # Retrieve memory if requested
        memory_results = {}
        if "memory_retrieval" in routing["additional_processing"]:
            memory_results = self._retrieve_relevant_memory(message, analysis)

        # Build enhanced context for persona
        persona_context = {
            **context,
            "file_data": file_results,
            "memory_data": memory_results,
            "routing_info": routing,
        }

        # Generate persona response with enhanced capabilities
        persona_response = persona_engine.generate(
            message,
            mode=mode,
            history=self.context.conversation_history[-5:],  # Last 5 interactions
            context=persona_context,
        )

        # Build comprehensive response
        response = {
            "response": persona_response.text,
            "mode": persona_response.mode,
            "analysis": analysis,
            "conversation_context": context["conversation_context"],
            "file_operations_results": file_results,
            "memory_integration": memory_results,
            "system_capabilities_used": routing["additional_processing"],
            "clever_state": self._generate_clever_state(analysis, context),
            "ui_reactions": self._generate_ui_reactions(analysis, persona_response),
            "proactive_suggestions": persona_response.proactive_suggestions,
            "timestamp": datetime.now().isoformat(),
            "particle_intensity": min(1.0, analysis.get("complexity_score", 0.5) * 2),
            "creativity": self.context.energy_level * 1.2,
            "energy": self.context.energy_level,
            "mood": self._determine_mood(analysis, persona_response),
            "excitement": min(1.0, len(analysis.get("keywords", [])) / 10),
            "insights": self._generate_insights(analysis, context, file_results),
            "approach": self._determine_approach(analysis, mode),
        }

        return response

    def _process_file_requests(
        self, message: str, operations: List[str]
    ) -> Dict[str, Any]:
        """Process file-related requests"""
        results = {
            "files_accessed": [],
            "file_contents": {},
            "file_analysis": {},
            "directory_listings": [],
        }

        try:
            # List available files if requested
            if "list_files" in operations:
                current_dir = Path(".")
                files = [
                    f.name
                    for f in current_dir.iterdir()
                    if f.is_file() and not f.name.startswith(".")
                ]
                results["directory_listings"] = files[:20]  # Limit to 20 files

            # Search for specific files mentioned in message
            file_keywords = ["file", "document", ".txt", ".py", ".md", ".json"]
            if any(keyword in message.lower() for keyword in file_keywords):
                # Extract potential filenames from message
                words = message.split()
                potential_files = [
                    word for word in words if "." in word and len(word) > 3
                ]

                for potential_file in potential_files:
                    file_path = Path(potential_file)
                    if file_path.exists() and file_path.is_file():
                        try:
                            content = self._safe_read_file(file_path)
                            if content:
                                results["files_accessed"].append(str(file_path))
                                results["file_contents"][str(file_path)] = content[
                                    :1000
                                ]  # Limit content
                                results["file_analysis"][str(file_path)] = (
                                    self._analyze_file_content(content)
                                )
                        except Exception as e:
                            logger.warning(
                                "conversation_engine", f"File read error: {e}"
                            )

        except Exception as e:
            logger.warning("conversation_engine", f"File processing error: {e}")
            results["error"] = str(e)

        return results

    def _safe_read_file(self, file_path: Path) -> Optional[str]:
        """Safely read file content with error handling"""
        try:
            if file_path.suffix.lower() in [
                ".txt",
                ".md",
                ".py",
                ".js",
                ".json",
                ".csv",
            ]:
                return file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            logger.warning("conversation_engine", f"Safe file read error: {e}")
        return None

    def _analyze_file_content(self, content: str) -> Dict[str, Any]:
        """Analyze file content using NLP capabilities"""
        if len(content) > 500:
            content = content[:500]  # Analyze first 500 chars

        nlp_result = nlp_processor.process(content)

        return {
            "keywords": nlp_result.keywords,
            "sentiment": nlp_result.sentiment,
            "word_count": len(content.split()),
            "line_count": len(content.splitlines()),
            "content_type": self._detect_content_type(content),
        }

    def _detect_content_type(self, content: str) -> str:
        """Detect the type of content"""
        content_lower = content.lower()

        if any(keyword in content_lower for keyword in ["def ", "import ", "class "]):
            return "python_code"
        elif any(
            keyword in content_lower for keyword in ["function", "var ", "const "]
        ):
            return "javascript_code"
        elif content.strip().startswith("{") or content.strip().startswith("["):
            return "json_data"
        elif "," in content and "\n" in content:
            return "csv_data"
        else:
            return "text_document"

    def _retrieve_relevant_memory(
        self, message: str, analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Retrieve relevant conversation memory and context"""
        memory_results = {
            "recent_conversations": [],
            "relevant_topics": [],
            "user_preferences": {},
            "conversation_patterns": {},
        }

        try:
            # Get recent conversation history
            memory_results["recent_conversations"] = self.context.conversation_history[
                -5:
            ]

            # Find relevant topics based on keywords
            keywords = analysis.get("keywords", [])
            for keyword in keywords:
                relevant_convos = [
                    conv
                    for conv in self.context.conversation_history
                    if keyword.lower() in conv.get("user_message", "").lower()
                ]
                if relevant_convos:
                    memory_results["relevant_topics"].append(
                        {
                            "keyword": keyword,
                            "conversations": relevant_convos[-3:],  # Last 3 relevant
                        }
                    )

        except Exception as e:
            logger.warning("conversation_engine", f"Memory retrieval error: {e}")
            memory_results["error"] = str(e)

        return memory_results

    def _generate_clever_state(
        self, analysis: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate Clever's internal state information"""
        return {
            "processing": False,
            "focus": min(1.0, analysis.get("complexity_score", 0.5) + 0.1),
            "creativity": self.context.energy_level * 0.9,
            "energy": self.context.energy_level,
            "mood": self._determine_mood(analysis, None),
            "excitement": min(1.0, len(analysis.get("keywords", [])) / 8),
            "supportiveness": 0.8 if analysis.get("sentiment", 0) < 0 else 0.6,
            "playfulness": 0.75 if self.context.current_focus == "creative" else 0.5,
        }

    def _generate_ui_reactions(
        self, analysis: Dict[str, Any], persona_response
    ) -> Dict[str, Any]:
        """Generate UI reaction instructions for particle system"""
        complexity = analysis.get("complexity_score", 0.5)

        if complexity > 0.7:
            animation = "explosive_creativity"
            colors = ["#ff00ff", "#00ffff", "#ffff00"]  # Bright creative colors
            orb_behavior = "excited_spinning"
            particle_shape = "creative_burst"
        elif analysis.get("sentiment", 0) > 0.5:
            animation = "gentle_pulse"
            colors = ["#00ff88", "#88ff00", "#0088ff"]  # Positive colors
            orb_behavior = "happy_bounce"
            particle_shape = "sphere"
        else:
            animation = "calm_flow"
            colors = ["#4040ff", "#8040ff", "#4080ff"]  # Calm colors
            orb_behavior = "gentle_drift"
            particle_shape = "wave"

        return {
            "animation": animation,
            "color_scheme": colors,
            "orb_behavior": orb_behavior,
            "particle_shape": particle_shape,
        }

    def _determine_mood(self, analysis: Dict[str, Any], persona_response) -> str:
        """Determine Clever's current mood"""
        sentiment = analysis.get("sentiment", 0)
        complexity = analysis.get("complexity_score", 0.5)

        if complexity > 0.7:
            return "curious"
        elif sentiment > 0.3:
            return "cheerful"
        elif sentiment < -0.3:
            return "supportive"
        else:
            return "thoughtful"

    def _generate_insights(
        self,
        analysis: Dict[str, Any],
        context: Dict[str, Any],
        file_results: Dict[str, Any],
    ) -> List[str]:
        """Generate intelligent insights about the conversation"""
        insights = []

        # Complexity insights
        complexity = analysis.get("complexity_score", 0.5)
        if complexity > 0.8:
            insights.append(
                "Rich concept density detected - this is the kind of complex thinking I thrive on!"
            )

        # File operation insights
        if file_results.get("files_accessed"):
            insights.append(
                f"Successfully accessed {len(file_results['files_accessed'])} files for enhanced context"
            )

        # Conversation depth insights
        if self.context.conversation_depth == "deep":
            insights.append(
                "Deep conversation mode engaged - bringing full analytical capabilities online"
            )

        # Learning opportunity insights
        keywords = analysis.get("keywords", [])
        if len(keywords) > 6:
            insights.append(
                "High information density - excellent learning opportunity detected"
            )

        return insights

    def _determine_approach(self, analysis: Dict[str, Any], mode: str) -> str:
        """Determine the approach Clever should take"""
        intent = analysis.get("intent", "general_conversation")

        if intent == "creative_generation":
            return "creative_catalyst"
        elif intent == "deep_analysis":
            return "analytical_deep_dive"
        elif intent == "file_operation":
            return "systematic_processor"
        elif intent == "task_execution":
            return "efficient_executor"
        else:
            return "adaptive_conversationalist"

    def _integrate_learning(
        self, message: str, analysis: Dict[str, Any], response: Dict[str, Any]
    ):
        """Integrate learning from the conversation"""
        try:
            evo_engine = get_evolution_engine()
            if evo_engine:
                interaction_data = {
                    "user_input": message,
                    "analysis": analysis,
                    "response_mode": response.get("mode", "Auto"),
                    "capabilities_used": response.get("system_capabilities_used", []),
                    "complexity_score": analysis.get("complexity_score", 0.5),
                    "interaction_success": True,
                    "timestamp": datetime.now().isoformat(),
                }

                evo_engine.log_interaction(interaction_data)

        except Exception as e:
            logger.warning("conversation_engine", f"Learning integration error: {e}")

    def _process_text_file(self, file_path: Path) -> Dict[str, Any]:
        """Process text file with NLP analysis"""
        content = self._safe_read_file(file_path)
        if not content:
            return {}

        return {
            "content": content[:500],  # First 500 chars
            "analysis": self._analyze_file_content(content),
            "type": "text",
        }

    def _process_code_file(self, file_path: Path) -> Dict[str, Any]:
        """Process code file with special handling"""
        content = self._safe_read_file(file_path)
        if not content:
            return {}

        # Count functions, classes, imports for code files
        lines = content.splitlines()
        functions = len(
            [line for line in lines if "def " in line or "function" in line]
        )
        classes = len([line for line in lines if "class " in line])
        imports = len([line for line in lines if "import " in line or "from " in line])

        return {
            "content": content[:500],
            "analysis": self._analyze_file_content(content),
            "code_metrics": {
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "lines": len(lines),
            },
            "type": "code",
        }

    def _process_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Process JSON file with structure analysis"""
        content = self._safe_read_file(file_path)
        if not content:
            return {}

        try:
            json_data = json.loads(content)
            structure_info = {
                "is_array": isinstance(json_data, list),
                "keys": list(json_data.keys()) if isinstance(json_data, dict) else [],
                "size": len(json_data) if isinstance(json_data, (list, dict)) else 0,
            }
        except json.JSONDecodeError:
            structure_info = {"error": "Invalid JSON format"}

        return {
            "content": content[:500],
            "analysis": self._analyze_file_content(content),
            "json_structure": structure_info,
            "type": "json",
        }

    def _process_csv_file(self, file_path: Path) -> Dict[str, Any]:
        """Process CSV file with data analysis"""
        content = self._safe_read_file(file_path)
        if not content:
            return {}

        lines = content.splitlines()
        csv_info = {
            "rows": len(lines),
            "columns": len(lines[0].split(",")) if lines else 0,
            "headers": lines[0].split(",")[:5] if lines else [],  # First 5 headers
        }

        return {
            "content": content[:500],
            "analysis": self._analyze_file_content(content),
            "csv_structure": csv_info,
            "type": "csv",
        }


# Global enhanced conversation engine
_conversation_engine = None


def get_conversation_engine() -> EnhancedConversationEngine:
    """
    Get global conversation engine instance

    Why: Provides singleton access to enhanced conversation capabilities
    for consistent processing across all chat interactions.
    Where: Used by app.py chat endpoint for all conversation processing
    How: Implements lazy initialization for global conversation engine

    Returns:
        EnhancedConversationEngine instance with full capabilities

    Connects to:
        - app.py: Primary conversation processing interface
        - All system modules: Unified conversation orchestration
    """
    global _conversation_engine
    if _conversation_engine is None:
        _conversation_engine = EnhancedConversationEngine()
    return _conversation_engine
