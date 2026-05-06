from abc import ABC, abstractmethod


class BasePlugin(ABC):
    name = ""
    intents = []

    @abstractmethod
    def handle(self, intent, message, context=None):
        """Return dict with keys: intent, confidence, response"""
