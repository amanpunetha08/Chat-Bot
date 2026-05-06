from chatbot.nlp.providers.base import BaseProvider

RULES = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "greetings", "good morning", "good evening"],
        "response": "Hello! How can I help you today?",
    },
    "farewell": {
        "keywords": ["bye", "goodbye", "see you", "later", "quit"],
        "response": "Goodbye! Have a great day!",
    },
    "help": {
        "keywords": ["help", "support", "assist", "what can you do"],
        "response": "I can help you with general questions. Just type your message!",
    },
    "thanks": {
        "keywords": ["thank", "thanks", "appreciate"],
        "response": "You're welcome!",
    },
}


class RuleBasedProvider(BaseProvider):
    def process(self, message, context=None):
        msg = message.lower()
        for intent, data in RULES.items():
            if any(kw in msg for kw in data["keywords"]):
                return {"intent": intent, "confidence": 0.9, "response": data["response"]}
        return {"intent": "unknown", "confidence": 0.0, "response": f"I received your message: '{message}'. I'm not sure how to help with that yet."}
