from chatbot.nlp.providers.base import BaseProvider
from chatbot.nlp.providers.rule_based import RuleBasedProvider
from chatbot.knowledge import vectorstore

RELEVANCE_THRESHOLD = 1.6


class RAGProvider(BaseProvider):
    """Answers from knowledge base. Falls back to rule-based for greetings/small talk."""

    def __init__(self):
        self.rule_based = RuleBasedProvider()

    def process(self, message, context=None):
        # Try rule-based first for greetings/small talk
        rule_result = self.rule_based.process(message, context)
        if rule_result["intent"] != "unknown":
            return rule_result

        # Then try knowledge base
        if vectorstore.count() == 0:
            return rule_result

        results = vectorstore.search(message, top_k=3)
        if not results or results[0]["distance"] > RELEVANCE_THRESHOLD:
            return {"intent": "unknown", "confidence": 0.0, "response": "I don't have information about that in my knowledge base. Try asking about Aman's skills, experience, or projects!"}

        best = results[0]["content"]
        return {
            "intent": "knowledge_base",
            "confidence": round(max(0, 1 - results[0]["distance"] / 2), 2),
            "response": f"Based on my knowledge base:\n\n{best.strip()}",
        }
