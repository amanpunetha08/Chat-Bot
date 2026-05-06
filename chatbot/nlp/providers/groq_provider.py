import requests
from django.conf import settings

from chatbot.nlp.providers.base import BaseProvider
from chatbot.knowledge import vectorstore

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class GroqRAGProvider(BaseProvider):
    """Uses local KB for retrieval + Groq for natural language generation."""

    def process(self, message, context=None):
        msg = message.lower().strip()

        if len(message.split()) <= 2 and any(w in msg for w in ["hi", "hello", "hey"]):
            return {"intent": "greeting", "confidence": 1.0, "response": "Hello! How can I help you? Ask me anything about Aman's skills, experience, or projects!"}

        # Retrieve relevant chunks from KB
        kb_context = ""
        if vectorstore.count() > 0:
            results = vectorstore.search(message, top_k=3)
            if results and results[0]["distance"] < 1.8:
                kb_context = "\n\n".join(r["content"] for r in results)

        system_prompt = (
            "You are Aman Punetha's AI assistant on his portfolio website. "
            "Answer questions about Aman based on the context provided. "
            "Be concise, friendly, and professional. Keep answers under 3 sentences. "
            "If the context doesn't contain the answer, say you don't have that information."
        )

        user_prompt = message
        if kb_context:
            user_prompt = f"Context from Aman's resume:\n{kb_context}\n\nQuestion: {message}"

        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.7,
                "max_tokens": 200,
            },
            timeout=15,
        )

        if resp.status_code != 200:
            return {"intent": "error", "confidence": 0.0, "response": "Sorry, I'm having trouble right now. Try again!"}

        data = resp.json()
        answer = data["choices"][0]["message"]["content"]

        return {"intent": "knowledge_base", "confidence": 0.9, "response": answer}
