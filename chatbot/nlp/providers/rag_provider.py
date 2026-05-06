from chatbot.nlp.providers.base import BaseProvider
from chatbot.knowledge import vectorstore

RELEVANCE_THRESHOLD = 1.8
SHORT_MESSAGE_THRESHOLD = 1.4  # Stricter threshold for very short messages


class RAGProvider(BaseProvider):
    """Answers from knowledge base. Uses message length to adjust relevance threshold."""

    def process(self, message, context=None):
        if vectorstore.count() == 0:
            return {"intent": "unknown", "confidence": 0.0, "response": "Knowledge base is empty."}

        # Shorter messages need stricter matching (less likely to be real questions)
        threshold = SHORT_MESSAGE_THRESHOLD if len(message.split()) <= 2 else RELEVANCE_THRESHOLD

        results = vectorstore.search(message, top_k=3)
        if not results or results[0]["distance"] > threshold:
            # No good KB match — give a helpful fallback
            return {
                "intent": "general",
                "confidence": 0.5,
                "response": self._fallback_response(message),
            }

        best = results[0]["content"]
        return {
            "intent": "knowledge_base",
            "confidence": round(max(0, 1 - results[0]["distance"] / 2), 2),
            "response": f"Based on my knowledge base:\n\n{best.strip()}",
        }

    def _fallback_response(self, message):
        msg = message.lower().strip()
        if any(w in msg for w in ["hi", "hello", "hey", "greetings"]):
            return "Hello! How can I help you? Ask me anything about what's in my knowledge base."
        if any(w in msg for w in ["bye", "goodbye", "see you"]):
            return "Goodbye! Feel free to come back anytime."
        if any(w in msg for w in ["thank", "thanks"]):
            return "You're welcome!"
        return "I don't have information about that in my knowledge base. Try asking something more specific!"
