from django.conf import settings


def get_provider():
    name = settings.NLP_PROVIDER
    if name == "openai":
        from chatbot.nlp.providers.openai_provider import OpenAIProvider
        return OpenAIProvider()
    if name == "rag":
        from chatbot.nlp.providers.rag_provider import RAGProvider
        return RAGProvider()
    if name == "gemini":
        from chatbot.nlp.providers.gemini_provider import GeminiRAGProvider
        return GeminiRAGProvider()
    from chatbot.nlp.providers.rule_based import RuleBasedProvider
    return RuleBasedProvider()
