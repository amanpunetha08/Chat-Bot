import requests
from django.conf import settings

from chatbot.nlp.providers.base import BaseProvider
from chatbot.knowledge import vectorstore

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


class GeminiRAGProvider(BaseProvider):
    """Uses local KB for retrieval + Gemini for natural language generation."""

    def process(self, message, context=None):
        msg = message.lower().strip()

        # Quick fallback for greetings
        if len(message.split()) <= 2 and any(w in msg for w in ["hi", "hello", "hey"]):
            return {"intent": "greeting", "confidence": 1.0, "response": "Hello! How can I help you? Ask me anything about Aman's skills, experience, or projects!"}

        # Retrieve relevant chunks from KB
        kb_context = ""
        if vectorstore.count() > 0:
            results = vectorstore.search(message, top_k=3)
            if results and results[0]["distance"] < 1.8:
                kb_context = "\n\n".join(r["content"] for r in results)

        # Build prompt for Gemini
        system_prompt = (
            "You are Aman Punetha's AI assistant on his portfolio website. "
            "Answer questions about Aman based on the context provided. "
            "Be concise, friendly, and professional. "
            "If the context doesn't contain the answer, say you don't have that information."
        )

        user_prompt = message
        if kb_context:
            user_prompt = f"Context from Aman's resume:\n{kb_context}\n\nQuestion: {message}"

        # Call Gemini API
        resp = requests.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}],
            },
            timeout=15,
        )

        if resp.status_code != 200:
            return {"intent": "error", "confidence": 0.0, "response": "Sorry, I'm having trouble right now. Try again!"}

        data = resp.json()
        answer = data["candidates"][0]["content"]["parts"][0]["text"]

        return {"intent": "knowledge_base", "confidence": 0.9, "response": answer}
