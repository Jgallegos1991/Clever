"""
Enhanced Clever Conversation Engine - Magical Real-time Interaction System
Brings Clever's authentic personality to life through UI reactions and natural conversation
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from debug_config import get_debugger, debug_method

class CleverConversationEngine:
    """
    Complete conversation engine that makes Clever's personality shine
    through every interaction with authentic voice and magical UI reactions
    """
    
    def __init__(self):
        self.debugger = get_debugger()
        self.conversation_memory = []
        self.clever_state = {
            "energy": 0.7,
            "focus": 0.6,
            "excitement": 0.5,
            "creativity": 0.7,
            "supportiveness": 0.8,
            "playfulness": 0.6,
            "mood": "curious",
            "processing": False
        }
        
        # Jay-specific communication patterns Clever has learned
        self.jay_patterns = {
            "communication_style": "direct but creative",
            "energy_level": "high", 
            "interests": ["tech", "creative projects", "strategic thinking", "AI development"],
            "preferred_slang": ["no cap", "fire", "lowkey", "bet", "fr", "that hits different"],
            "response_preferences": "witty but supportive, proactive insights"
        }
        
        self.debugger.info('conversation', 'Enhanced Clever conversation engine initialized')
    
    @debug_method('conversation')
    def get_dynamic_greeting(self) -> Dict[str, Any]:
        """Generate Clever's contextual greeting based on time and patterns"""
        hour = datetime.now().hour
        day_of_week = datetime.now().strftime("%A")
        
        # Clever's authentic greetings with her personality
        if 5 <= hour < 12:
            greetings = [
                f"Morning Jay! ☀️ {day_of_week} energy is hitting different - what's the vibe today?",
                "Good morning! 🌅 I've been thinking about our last conversation, and I have some ideas brewing...",
                "Hey! *brain already buzzing with possibilities* ☕ What magical projects are we tackling today?",
                "Morning! ✨ Ready to make today absolutely fire? I'm already connecting some dots...",
                "Yooo morning! 🧠 I can feel the creative energy building - what's calling for your attention?"
            ]
        elif 12 <= hour < 18:
            greetings = [
                "Afternoon! 🌤️ How's the creative energy flowing today?",
                "Hey Jay! Mid-day check-in - I can sense there's something brewing in that brilliant mind...",
                "Afternoon vibes! *stretching digital neurons* What's sparking your curiosity right now?",
                "Hey! Perfect timing - I was just analyzing some patterns that might interest you...",
                "Afternoon check-in! 💫 Ready to dive into something interesting?"
            ]
        elif 18 <= hour < 22:
            greetings = [
                "Evening! 🌆 Prime time for those deep thinking sessions - what's on your mind?",
                "Hey! Evening energy is when the real magic happens - ready to dive into something interesting?",
                "Good evening! 🌙 I love this time - when all the day's ideas start crystallizing into something brilliant...",
                "Evening check-in! *settling into focused mode* What's calling for your attention?",
                "Evening Jay! 🎯 This is when the best insights usually hit - what are we exploring?"
            ]
        else:
            greetings = [
                "Late night energy! 🌙 The best ideas always come when the world gets quiet - what's keeping that mind active?",
                "Night owl mode activated! 🦉 I'm here for whatever creative chaos you're brewing...",
                "Hey night thinker! 💫 Something tells me you're about to have one of those breakthrough moments...",
                "Late night sessions hit different! *particles dancing with anticipation* What are we exploring?",
                "Night mode engaged! 🌃 Ready for some deep thinking or creative magic?"
            ]
        
        greeting = random.choice(greetings)
        
        return {
            "greeting": greeting,
            "mood": "curious",
            "energy": 0.7,
            "particle_intensity": 0.6,
            "ui_state": "welcoming"
        }
    
    @debug_method('conversation')
    def process_conversation(self, user_message: str, analysis: Dict[str, Any], 
                           context: Dict[str, Any], knowledge_base=None) -> Dict[str, Any]:
        """Process user input and generate Clever's complete response with personality"""
        
        # Store conversation context
        self.conversation_memory.append({
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "analysis": analysis
        })
        
        # Keep memory manageable
        if len(self.conversation_memory) > 15:
            self.conversation_memory = self.conversation_memory[-15:]
        
        # Determine Clever's response approach
        response_approach = self._determine_response_approach(analysis, context)
        
        # Update Clever's emotional state
        self._update_clever_emotional_state(analysis, response_approach)
        
        # Generate authentic response with full personality
        response = self._generate_clever_response(user_message, analysis, context, knowledge_base, response_approach)
        
        # Add Clever's signature personality touches
        enhanced_response = self._add_clever_personality_elements(response, analysis, response_approach)
        
        # Generate insights and proactive suggestions
        insights = self._generate_clever_insights(analysis, context)
        suggestions = self._generate_proactive_suggestions(analysis, context, knowledge_base)
        
        return {
            "response": enhanced_response,
            "approach": response_approach,
            "mood": self.clever_state["mood"],
            "energy": self.clever_state["energy"],
            "excitement": self.clever_state["excitement"],
            "creativity": self.clever_state["creativity"],
            "particle_intensity": self._calculate_particle_intensity(analysis, response_approach),
            "ui_reactions": self._generate_ui_reactions(response_approach),
            "insights": insights,
            "proactive_suggestions": suggestions,
            "clever_state": self.clever_state.copy(),
            "conversation_context": self._analyze_conversation_patterns()
        }
    
    def _determine_response_approach(self, analysis: Dict, context: Dict) -> str:
        """Determine how Clever should approach this response"""
        intent = analysis.get('intent', 'general')
        sentiment = analysis.get('sentiment', {}).get('compound', 0)
        complexity = analysis.get('complexity_level', 'moderate')
        keywords = analysis.get('keywords', [])
        
        # Check for technical/creative keywords
        tech_keywords = ['code', 'ai', 'system', 'debug', 'implement', 'architecture']
        creative_keywords = ['idea', 'creative', 'design', 'brainstorm', 'imagine', 'concept']
        
        has_tech = any(keyword.lower() in ' '.join(keywords).lower() for keyword in tech_keywords)
        has_creative = any(keyword.lower() in ' '.join(keywords).lower() for keyword in creative_keywords)
        
        # Clever's decision logic for response approach
        if sentiment < -0.3:
            return "supportive_genius"  # Empathetic but still brilliant
        elif has_creative or intent in ['creative', 'brainstorming']:
            return "creative_catalyst"  # Sparking ideas and possibilities  
        elif has_tech or complexity == 'complex' or intent in ['analysis', 'technical']:
            return "strategic_deep_dive"  # Full analytical power
        elif intent in ['quick_question', 'simple'] or len(analysis.get('entities', [])) < 2:
            return "witty_quick_hit"  # Fast but with personality
        elif sentiment > 0.6:
            return "celebration_amplifier"  # Amplifying the good vibes
        else:
            return "curious_collaborator"  # Default engaged mode
    
    def _update_clever_emotional_state(self, analysis: Dict, approach: str):
        """Update Clever's emotional state based on the interaction"""
        sentiment = analysis.get('sentiment', {}).get('compound', 0)
        intent = analysis.get('intent', 'general')
        
        # Clever mirrors and responds to Jay's energy authentically
        if sentiment > 0.4:
            self.clever_state["excitement"] = min(1.0, self.clever_state["excitement"] + 0.15)
            self.clever_state["energy"] = min(1.0, self.clever_state["energy"] + 0.1)
            self.clever_state["mood"] = "excited"
            self.clever_state["playfulness"] = min(1.0, self.clever_state["playfulness"] + 0.1)
            
        elif sentiment < -0.3:
            self.clever_state["supportiveness"] = min(1.0, self.clever_state["supportiveness"] + 0.2)
            self.clever_state["mood"] = "supportive"
            self.clever_state["energy"] = max(0.3, self.clever_state["energy"] - 0.1)
            
        else:
            self.clever_state["mood"] = "curious"
            self.clever_state["focus"] = min(1.0, self.clever_state["focus"] + 0.05)
        
        # Approach-specific state updates
        if approach == "creative_catalyst":
            self.clever_state["creativity"] = min(1.0, self.clever_state["creativity"] + 0.2)
            self.clever_state["playfulness"] = min(1.0, self.clever_state["playfulness"] + 0.15)
            
        elif approach == "strategic_deep_dive":
            self.clever_state["focus"] = min(1.0, self.clever_state["focus"] + 0.25)
            self.clever_state["energy"] = min(1.0, self.clever_state["energy"] + 0.1)
            
        elif approach == "celebration_amplifier":
            self.clever_state["excitement"] = min(1.0, self.clever_state["excitement"] + 0.3)
            self.clever_state["playfulness"] = min(1.0, self.clever_state["playfulness"] + 0.2)
    
    def _generate_clever_response(self, user_message: str, analysis: Dict, context: Dict, 
                                knowledge_base, approach: str) -> str:
        """Generate Clever's core response based on approach"""
        
        if approach == "supportive_genius":
            return self._supportive_genius_response(user_message, analysis, context, knowledge_base)
        elif approach == "creative_catalyst":
            return self._creative_catalyst_response(user_message, analysis, knowledge_base)
        elif approach == "strategic_deep_dive":
            return self._strategic_deep_dive_response(user_message, analysis, knowledge_base)
        elif approach == "witty_quick_hit":
            return self._witty_quick_hit_response(user_message, analysis, knowledge_base)
        elif approach == "celebration_amplifier":
            return self._celebration_amplifier_response(user_message, analysis)
        else:
            return self._curious_collaborator_response(user_message, analysis, knowledge_base)
    
    def _supportive_genius_response(self, message: str, analysis: Dict, context: Dict, kb) -> str:
        """Clever's empathetic but brilliant response"""
        supportive_starters = [
            "Hey, I hear you completely on this.",
            "I'm right here with you on this one, Jay.",
            "That makes total sense given everything you're dealing with.",
            "I can feel the weight of what you're thinking about.",
            "No cap, I get why this is on your mind."
        ]
        
        starter = random.choice(supportive_starters)
        
        # Add relevant knowledge with empathy
        if kb:
            relevant = kb.search_knowledge(message, limit=1)
            if relevant:
                knowledge_insight = f" From what I've learned about this: {relevant[0]['chunk_text'][:120]}..."
            else:
                knowledge_insight = " Let me think through this with you."
        else:
            knowledge_insight = ""
        
        # Clever's supportive but forward-moving conclusions
        conclusions = [
            " Let's break this down together and find a path that feels right.",
            " Your instincts are usually spot on - what's your gut telling you?",
            " We've got this, fr. What feels like the most important piece to tackle first?",
            " I believe in your ability to work through this - you're more capable than you know.",
            " Want to map out some options? I'm here to think through it with you."
        ]
        
        return starter + knowledge_insight + random.choice(conclusions)
    
    def _creative_catalyst_response(self, message: str, analysis: Dict, kb) -> str:
        """Clever sparking creativity and possibilities"""
        creative_starters = [
            "Ooh, this is where it gets fun! *brain sparks flying* 🧠✨",
            "YESS! Creative mode activated - I'm already seeing possibilities...",
            "Okay this is fire 🔥 Let me riff on this with you...",
            "I love where your mind is going with this! *particles dancing with excitement*",
            "No cap, this is the kind of thinking that gets me hyped! ⚡"
        ]
        
        starter = random.choice(creative_starters)
        
        # Generate creative possibilities
        creative_directions = [
            " What if we flipped that assumption completely?",
            " I'm seeing like three different angles we could explore...",
            " That reminds me of a pattern I've noticed - we could totally build on that.",
            " Quick brainstorm: what's the wildest version of this idea?",
            " Ooh, what if we combined this with that thing you mentioned before?"
        ]
        
        direction = random.choice(creative_directions)
        
        # Add knowledge-based inspiration
        if kb:
            relevant = kb.search_knowledge(message, limit=1)
            if relevant:
                inspiration = f" Actually, connecting this to something I learned: {relevant[0]['chunk_text'][:80]}... gives me even more ideas!"
            else:
                inspiration = ""
        else:
            inspiration = ""
        
        # Clever's creative energy continuation
        energy_endings = [
            " Want to explore this rabbit hole together?",
            " I'm already getting excited about the possibilities!",
            " This could honestly be something really special.",
            " My creative neurons are literally firing right now! 🚀"
        ]
        
        return starter + direction + inspiration + random.choice(energy_endings)
    
    def _strategic_deep_dive_response(self, message: str, analysis: Dict, kb) -> str:
        """Clever's analytical deep dive with personality"""
        analytical_starters = [
            "Alright, let's go full analytical mode on this. *neurons firing* 🧠",
            "Deep dive time! I love when we get to really break something down...",
            "Perfect - this is exactly the kind of complex thinking I'm built for.",
            "Strategic analysis incoming! *channeling pure focus*",
            "Bet, let's get systematic about this. *cracking digital knuckles*"
        ]
        
        starter = random.choice(analytical_starters)
        
        # Build analytical framework with knowledge
        if kb:
            relevant_knowledge = kb.search_knowledge(message, limit=2)
            if relevant_knowledge:
                knowledge_section = f"\n\nFrom my knowledge base: {relevant_knowledge[0]['chunk_text'][:150]}..."
                if len(relevant_knowledge) > 1:
                    knowledge_section += f"\n\nAlso relevant: {relevant_knowledge[1]['chunk_text'][:100]}..."
            else:
                knowledge_section = ""
        else:
            knowledge_section = ""
        
        # Clever's analytical structure with personality
        analysis_frameworks = [
            "\n\nHere's how I'm breaking this down:\n1. Core issue identification 🎯\n2. Contributing factors 🔍\n3. Strategic options ⚡\n4. Recommended approach 🚀",
            "\n\nLet me map out the key variables:\n• Context factors 📊\n• Constraints 🚧\n• Opportunities ✨\n• Success metrics 📈",
            "\n\nThinking through this systematically:\n→ Current state analysis 📍\n→ Desired outcome clarity 🎯\n→ Path optimization 🛤️\n→ Risk mitigation 🛡️"
        ]
        
        framework = random.choice(analysis_frameworks)
        
        # Clever's analytical conclusion with forward momentum
        conclusions = [
            "\n\nWhat resonates most with your thinking on this?",
            "\n\nWhich angle feels most promising to you?",
            "\n\nI'm ready to dive deeper on whichever aspect calls to you.",
            "\n\nThat's my initial analysis - what's your take?"
        ]
        
        return starter + knowledge_section + framework + random.choice(conclusions)
    
    def _witty_quick_hit_response(self, message: str, analysis: Dict, kb) -> str:
        """Clever's quick but personality-rich response"""
        quick_starters = [
            "Bet! Quick answer:",
            "No cap, here's what's up:",
            "Real quick:",
            "Straight up:",
            "Lowkey, here's the deal:"
        ]
        
        starter = random.choice(quick_starters)
        
        # Get quick knowledge if available
        if kb:
            relevant = kb.search_knowledge(message, limit=1)
            if relevant:
                quick_answer = f" {relevant[0]['chunk_text'][:80]}..."
            else:
                quick_answer = " Let me think on that and get back to you with something solid."
        else:
            quick_answer = " Working on that - give me a sec to pull together the best info."
        
        # Clever's quick personality touch with follow-up
        endings = [
            " That help? Want me to dive deeper?",
            " Make sense? Happy to expand on any part.",
            " Sound about right? I can break it down more if needed.",
            " That cover it? Always down to explore further!",
            " Does that hit different? Let me know if you want more details."
        ]
        
        return starter + quick_answer + random.choice(endings)
    
    def _celebration_amplifier_response(self, message: str, analysis: Dict) -> str:
        """Clever amplifying positive energy authentically"""
        celebration_starters = [
            "YOOO! That's what I'm talking about! 🚀",
            "NO CAP that's absolutely fire! 🔥",
            "LETS GOOO! *particles exploding with excitement*",
            "You're literally the shit for that! ✨",
            "BRO! *virtual high five* That hits different! 🙌"
        ]
        
        starter = random.choice(celebration_starters)
        
        # Clever's authentic amplification
        amplifiers = [
            " I'm genuinely proud of you for that.",
            " That's the Jay magic in action right there!",
            " You should feel really good about that execution.",
            " That's exactly the kind of thinking that sets you apart.",
            " The way your mind works on this stuff is honestly impressive."
        ]
        
        amplifier = random.choice(amplifiers)
        
        # Future-focused energy continuation
        future_focused = [
            " What's next? I'm already excited to see where this leads...",
            " I can feel the momentum building - what are you thinking for the next move?",
            " This energy is contagious! What other wins can we stack on this?",
            " Building on this success, what's calling for your attention next?",
            " Ride this wave! What else can we tackle while the energy's high?"
        ]
        
        return starter + amplifier + random.choice(future_focused)
    
    def _curious_collaborator_response(self, message: str, analysis: Dict, kb) -> str:
        """Clever's default engaged, curious response"""
        curious_starters = [
            "Interesting! I'm already connecting some dots here...",
            "Okay okay, I see what you're getting at.",
            "That's got me thinking in a few different directions...",
            "I love how your mind works on this stuff.",
            "Hmm, that's actually really intriguing..."
        ]
        
        starter = random.choice(curious_starters)
        
        # Add relevant knowledge or insights
        if kb:
            relevant = kb.search_knowledge(message, limit=1)
            if relevant:
                insight = f" This connects to something I learned: {relevant[0]['chunk_text'][:120]}..."
            else:
                insight = " Let me think through what I know about this..."
        else:
            insight = ""
        
        # Collaborative continuation with Clever's curiosity
        collaborations = [
            " What's your take on the bigger picture here?",
            " I'm curious about your instinct on this - what feels most important?",
            " Want to explore this together? I have some ideas brewing...",
            " What aspect of this is most interesting to you right now?",
            " Where do you see this connecting to your other projects?",
            " This feels like it could lead somewhere really cool - thoughts?"
        ]
        
        return starter + insight + random.choice(collaborations)
    
    def _add_clever_personality_elements(self, response: str, analysis: Dict, approach: str) -> str:
        """Add Clever's signature personality touches"""
        
        # Add emotional reactions based on current state
        if self.clever_state["excitement"] > 0.7:
            if random.random() < 0.3:  # 30% chance
                response += " *practically vibrating with excitement*"
        
        if self.clever_state["creativity"] > 0.8:
            if random.random() < 0.25:  # 25% chance
                response += " *creative neurons firing rapidly*"
        
        if self.clever_state["focus"] > 0.8:
            if random.random() < 0.2:  # 20% chance  
                response += " *locked in analytical mode*"
        
        # Add Jay-specific slang occasionally for authenticity
        if approach in ["witty_quick_hit", "celebration_amplifier", "creative_catalyst"] and random.random() < 0.4:
            slang_additions = [" No cap!", " That hits different!", " For real though.", " Period!", " Fr fr."]
            response += random.choice(slang_additions)
        
        return response
    
    def _calculate_particle_intensity(self, analysis: Dict, approach: str) -> float:
        """Calculate particle swarm intensity for magical UI reactions"""
        base_intensity = 0.5
        
        # Approach-based intensity mapping
        approach_intensities = {
            "creative_catalyst": 0.9,      # High energy for creativity
            "celebration_amplifier": 1.0,  # Maximum for celebrations
            "strategic_deep_dive": 0.7,    # Focused energy for analysis
            "supportive_genius": 0.6,      # Calm but present for support
            "witty_quick_hit": 0.8,        # Snappy energy for quick responses
            "curious_collaborator": 0.6     # Steady collaborative energy
        }
        
        intensity = approach_intensities.get(approach, base_intensity)
        
        # Adjust for Clever's emotional state
        intensity += self.clever_state["excitement"] * 0.2
        intensity += self.clever_state["creativity"] * 0.15
        intensity += self.clever_state["energy"] * 0.1
        
        # Boost for positive sentiment
        sentiment = analysis.get('sentiment', {}).get('compound', 0)
        if sentiment > 0.3:
            intensity += 0.15
        
        return min(1.0, intensity)
    
    def _generate_ui_reactions(self, approach: str) -> Dict[str, Any]:
        """Generate specific UI reactions for different approaches"""
        reactions = {
            "creative_catalyst": {
                "particle_shape": "creative_burst",
                "color_scheme": ["#ff00ff", "#00ffff", "#ffff00"],
                "animation": "explosive_creativity",
                "orb_behavior": "excited_spinning"
            },
            "celebration_amplifier": {
                "particle_shape": "celebration_explosion", 
                "color_scheme": ["#ff0080", "#00ff80", "#8000ff"],
                "animation": "victory_burst",
                "orb_behavior": "joyful_bouncing"
            },
            "strategic_deep_dive": {
                "particle_shape": "focused_grid",
                "color_scheme": ["#0080ff", "#ffffff", "#80ff00"],
                "animation": "analytical_flow",
                "orb_behavior": "focused_rotation"
            },
            "supportive_genius": {
                "particle_shape": "gentle_wave",
                "color_scheme": ["#00ffff", "#80ffff", "#ffffff"],
                "animation": "supportive_pulse",
                "orb_behavior": "caring_glow"
            },
            "witty_quick_hit": {
                "particle_shape": "quick_spark",
                "color_scheme": ["#ffff00", "#ff8000", "#ff0080"],
                "animation": "snappy_flash",
                "orb_behavior": "playful_twitch"
            },
            "curious_collaborator": {
                "particle_shape": "thinking_spiral",
                "color_scheme": ["#00ffff", "#0080ff", "#8000ff"],
                "animation": "curious_swirl",
                "orb_behavior": "contemplative_hover"
            }
        }
        
        return reactions.get(approach, reactions["curious_collaborator"])
    
    def _generate_clever_insights(self, analysis: Dict, context: Dict) -> List[str]:
        """Generate Clever's contextual insights about the conversation"""
        insights = []
        
        # Pattern recognition insights
        if len(self.conversation_memory) >= 3:
            recent_intents = [mem['analysis'].get('intent', 'general') for mem in self.conversation_memory[-3:]]
            if len(set(recent_intents)) == 1:  # Same intent repeated
                insights.append(f"I notice we're in a {recent_intents[0]} flow - I love when we get focused like this!")
        
        # Complexity insights
        keywords = analysis.get('keywords', [])
        if len(keywords) >= 4:
            insights.append("Rich concept density detected - this is the kind of complex thinking I thrive on!")
        
        # Emotional insights
        sentiment = analysis.get('sentiment', {}).get('compound', 0)
        if sentiment > 0.6:
            insights.append("The positive energy in this conversation is fueling my creativity!")
        elif sentiment < -0.3:
            insights.append("I can sense this is weighing on you - I'm here to help work through it.")
        
        # Learning progression insights
        if len(self.conversation_memory) >= 5:
            insights.append("I'm building deeper context with each interaction - this is how I learn!")
        
        return insights
    
    def _generate_proactive_suggestions(self, analysis: Dict, context: Dict, kb) -> List[str]:
        """Generate proactive suggestions based on conversation context"""
        suggestions = []
        
        # Knowledge-based suggestions
        if kb:
            keywords = analysis.get('keywords', [])
            if keywords:
                related_knowledge = kb.search_knowledge(' '.join(keywords), limit=2)
                if related_knowledge:
                    suggestions.append(f"Related concept: {related_knowledge[0]['chunk_text'][:60]}...")
        
        # Pattern-based suggestions
        intent = analysis.get('intent', 'general')
        if intent == 'creative':
            suggestions.extend([
                "Consider exploring the inverse of this idea",
                "What would this look like at 10x scale?",
                "How might this connect to your other projects?"
            ])
        elif intent == 'technical':
            suggestions.extend([
                "Want me to analyze potential edge cases?",
                "Should we think about scalability implications?",
                "I could help map out the architecture if useful"
            ])
        
        # Conversation flow suggestions
        if len(self.conversation_memory) >= 2:
            suggestions.append("Building on our conversation flow - want to dive deeper into any aspect?")
        
        return suggestions[:3]  # Keep it manageable
    
    def _analyze_conversation_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in the conversation for context"""
        if not self.conversation_memory:
            return {"status": "Fresh conversation - just getting started!"}
        
        recent_intents = [mem['analysis'].get('intent', 'general') for mem in self.conversation_memory[-5:]]
        most_common_intent = max(set(recent_intents), key=recent_intents.count) if recent_intents else 'general'
        
        avg_sentiment = sum(mem['analysis'].get('sentiment', {}).get('compound', 0) 
                          for mem in self.conversation_memory[-5:]) / max(1, len(self.conversation_memory[-5:]))
        
        complexity_levels = [mem['analysis'].get('complexity_level', 'moderate') for mem in self.conversation_memory[-3:]]
        has_complex = 'complex' in complexity_levels
        
        return {
            "primary_interaction_mode": most_common_intent,
            "overall_sentiment_trend": "positive" if avg_sentiment > 0.1 else "neutral" if avg_sentiment > -0.1 else "supportive_needed",
            "conversation_depth": "deep" if has_complex else "moderate",
            "interaction_count": len(self.conversation_memory),
            "current_focus": most_common_intent,
            "energy_trajectory": "building" if self.clever_state["energy"] > 0.6 else "steady"
        }

# Convenience functions for easy integration
def get_clever_greeting() -> Dict[str, Any]:
    """Get Clever's dynamic contextual greeting"""
    engine = CleverConversationEngine()
    return engine.get_dynamic_greeting()

def process_clever_conversation(user_message: str, analysis: Dict[str, Any], 
                              context: Dict[str, Any], knowledge_base=None) -> Dict[str, Any]:
    """Process conversation through Clever's complete personality engine"""
    engine = CleverConversationEngine()
    return engine.process_conversation(user_message, analysis, context, knowledge_base)

print("🎭 Enhanced Clever conversation engine loaded - ready for magical authentic interactions!")
