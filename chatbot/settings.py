import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = os.environ.get("DEBUG", "1") == "1"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "rest_framework",
    "corsheaders",
    "chatbot.api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "chatbot.urls"
WSGI_APPLICATION = "chatbot.wsgi.application"

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "UNAUTHENTICATED_USER": None,
}

# Redis
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# NLP Provider: "rule_based", "openai", "rag"
NLP_PROVIDER = os.environ.get("NLP_PROVIDER", "rule_based")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

# Knowledge Base (RAG)
KNOWLEDGE_BASE_DIR = os.environ.get("KNOWLEDGE_BASE_DIR", str(BASE_DIR / "knowledge_base"))
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Grok (xAI)
GROK_API_KEY = os.environ.get("GROK_API_KEY", "")

# Groq (fast LLM inference)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
