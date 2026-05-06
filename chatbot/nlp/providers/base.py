from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    def process(self, message, context=None):
        """Return dict with keys: intent, confidence, response"""
