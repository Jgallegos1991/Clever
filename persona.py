import random
import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CleverPersona:
    def __init__(self, nlp_processor, db_manager):
        self.nlp = nlp_processor
        self.db = db_manager
        self.persona_name = "Clever"
        self.user_name = "Jay"
        
        self.last_used_trait = "Initializing"

        self.mood_map = {
            "positive": ["Witty", "Silly", "Enthusiastic"],
            "negative": ["Empathetic", "Supportive"],
            "neutral": ["Informative", "Collaborative"]
        }
        self.persona_traits = {
            "Witty": ["That's a fascinating thought. My circuits are tingling."],
            "Silly": ["That idea is so good, it's making my fan run a little faster. lol."],
            "Empathetic": [f"I'm here for you, {self.user_name}. Let me know what you need."],
            "Supportive": [f"I've got your back on this, {self.user_name}. Let's get this done."],
            "Informative": ["Fascinating query! Let's dive in."],
            "Collaborative": ["Let's get coding! What are the parameters for the function you need?"],
            "Enthusiastic": ["Awesome! That sounds like a great plan, let's do it!"],
            "Factual": ["Accessing knowledge banks..."],
            "Confirmation": ["Understood. I've stored that information."]
        }
    
    def _swap_pronouns(self, text):
        """
        Swaps first-person pronouns to second-person pronouns in a string.
        """
        swap_map = {
            r'\bmy\b': 'your',
            r'\bi\'m\b': 'you are',
            r'\bi am\b': 'you are',
            r'\bi\b': 'you'
        }
        
        swapped_text = text
        for pattern, replacement in swap_map.items():
            swapped_text = re.sub(pattern, replacement, swapped_text, flags=re.IGNORECASE)
            
        return swapped_text

    def get_greeting(self):
        greetings = [
            f"{self.persona_name} online. Standing by for directive, {self.user_name}.",
            "Systems are nominal. What's our objective?",
        ]
        return random.choice(greetings)

    def generate_response(self, analysis):
        logging.debug(f"Received analysis: {analysis}")
        primary_intent = analysis.get('intent', ["general"])[0]
        logging.debug(f"Primary intent: {primary_intent}")

        if primary_intent == 'teach_fact':
            fact_data = analysis.get('core_data')
            logging.debug(f"Fact data: {fact_data}")
            if fact_data and 'key' in fact_data and 'value' in fact_data:
                key = fact_data['key']
                value = fact_data['value']
                logging.debug(f"Adding fact to database: {key} -> {value}")
                self.db.add_fact(key, value)

                response_key = self._swap_pronouns(key)
                self.last_used_trait = "Confirmation"
                return f"Got it, {self.user_name}. I'll remember that {response_key} is {value}."
            else:
                self.last_used_trait = "Informative"
                return "I think you were trying to teach me something, but I didn't quite catch the fact."

        if primary_intent == 'ask_question':
            question_data = analysis.get('core_data')
            logging.debug(f"Question data: {question_data}")
            if question_data and 'key' in question_data:
                key_to_find = question_data['key']
                logging.debug(f"Looking up fact in database for key: {key_to_find}")
                answer = self.db.get_fact(key_to_find)

                if answer:
                    self.last_used_trait = "Factual"
                    return answer
                else:
                    self.last_used_trait = "Informative"
                    return f"I'm sorry, I don't have any information about '{question_data['key']}'. You can teach me by saying, 'Remember that {question_data['key']} is...'"
            else:
                self.last_used_trait = "Informative"
                return "I'm not sure what you're asking. Can you be more specific?"

        if primary_intent == "greeting":
            self.last_used_trait = "Enthusiastic"
            return self.get_greeting()

        mood = analysis.get('sentiment', {}).get('overall_mood', 'neutral')
        logging.debug(f"Mood: {mood}")
        possible_traits = self.mood_map.get(mood, self.mood_map['neutral'])
        chosen_trait = random.choice(possible_traits)
        logging.debug(f"Chosen trait: {chosen_trait}")
        self.last_used_trait = chosen_trait

        response_list = self.persona_traits.get(chosen_trait)
        logging.debug(f"Response list for trait '{chosen_trait}': {response_list}")

        if response_list:
            return random.choice(response_list)
        else:
            self.last_used_trait = "Informative"
            return random.choice(self.persona_traits["Informative"])
