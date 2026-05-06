from django.conf import settings
from openai import OpenAI

from chatbot.nlp.providers.base import BaseProvider


class OpenAIProvider(BaseProvider):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def process(self, message, context=None):
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        if context:
            for msg in context[-10:]:  # last 10 messages for context window
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": message})

        resp = self.client.chat.completions.create(model=self.model, messages=messages)
        return {
            "intent": "conversation",
            "confidence": 1.0,
            "response": resp.choices[0].message.content,
        }
