from chatbot.nlp.providers.base import BaseProvider
from chatbot.knowledge.rag import retrieve_context, build_rag_prompt
from chatbot.knowledge import vectorstore


class RAGProvider(BaseProvider):
    """Answers from knowledge base. Falls back to a simple message if no context found."""

    RELEVANCE_THRESHOLD = 0.85  # ChromaDB L2 distance; lower = more similar

    def process(self, message, context=None):
        if vectorstore.count() == 0:
            return {"intent": "no_knowledge", "confidence": 0.0, "response": "Knowledge base is empty. Please index some documents first."}

        results = vectorstore.search(message, top_k=3)
        if not results or results[0]["distance"] > self.RELEVANCE_THRESHOLD:
            return {"intent": "unknown", "confidence": 0.0, "response": "I don't have information about that in my knowledge base."}

        best = results[0]["content"]
        return {
            "intent": "knowledge_base",
            "confidence": round(max(0, 1 - results[0]["distance"] / 2), 2),
            "response": f"Based on my knowledge base:\n\n{best.strip()}",
        }
