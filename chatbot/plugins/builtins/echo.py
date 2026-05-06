from chatbot.plugins import registry
from chatbot.plugins.base import BasePlugin


class EchoPlugin(BasePlugin):
    name = "echo"
    intents = ["echo"]

    def handle(self, intent, message, context=None):
        return {"intent": "echo", "confidence": 1.0, "response": f"Echo: {message}"}


registry.register(EchoPlugin)
