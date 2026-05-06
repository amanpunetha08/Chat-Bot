# Universal ChatBot Microservice

A single Django microservice that provides chatbot functionality via REST API. Plug it into any application.

```
┌──────────────┐         ┌──────────────────────────────────────┐
│  Your App    │──HTTP──▶│  ChatBot Microservice (:8000)        │
│  (any lang)  │◀────────│  ┌─────┐ ┌─────┐ ┌───────┐         │
└──────────────┘         │  │ API │→│ NLP │→│Plugins│         │
                         │  └─────┘ └──┬──┘ └───────┘         │
                         │             │                        │
                         │     ┌───────▼────────┐              │
                         │     │ Knowledge Base  │              │
                         │     │ (ChromaDB +     │              │
                         │     │  Embeddings)    │              │
                         │     └────────────────┘              │
                         │         ┌───────┐                    │
                         │         │ Redis │                    │
                         │         └───────┘                    │
                         └──────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- Redis

### Setup

```bash
# Clone
git clone git@github.com:amanpunetha08/Chat-Bot.git
cd Chat-Bot

# Install dependencies
pip install -r requirements.txt

# Start Redis
brew services start redis

# Run the server
python manage.py runserver
```

### Test it

```bash
curl -s -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' | python -m json.tool
```

## NLP Providers

Set via `NLP_PROVIDER` environment variable:

| Provider | Command | Description |
|----------|---------|-------------|
| `rule_based` | `NLP_PROVIDER=rule_based python manage.py runserver` | Keyword matching (default, no setup needed) |
| `rag` | `NLP_PROVIDER=rag python manage.py runserver` | Answers from your knowledge base (free, local) |
| `openai` | `NLP_PROVIDER=openai OPENAI_API_KEY=sk-... python manage.py runserver` | GPT-powered responses (paid) |

## Knowledge Base (RAG)

Answer questions from your own documents — PDFs, text files, markdown. Completely free, runs locally.

### Step 1: Add documents

Drop files into the `knowledge_base/` folder:

```bash
cp ~/Documents/my-docs.pdf knowledge_base/
cp ~/notes.md knowledge_base/
```

Supported formats: `.pdf`, `.txt`, `.md`

### Step 2: Index documents

```bash
python manage.py index_knowledge
```

To re-index from scratch:

```bash
python manage.py index_knowledge --reset
```

### Step 3: Run with RAG provider

```bash
NLP_PROVIDER=rag python manage.py runserver
```

### Step 4: Ask questions

```bash
curl -s -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "what is the return policy?"}' | python -m json.tool
```

If the answer isn't in the knowledge base, the bot responds: *"I don't have information about that in my knowledge base."*

## API Reference

### Chat

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | `/api/chat/` | `{"message": "hi", "session_id": "optional"}` | Send a message |
| GET | `/api/history/<session_id>/` | — | Get conversation history |
| DELETE | `/api/session/<session_id>/` | — | Clear a session |
| GET | `/api/health/` | — | Health check |

### Knowledge Base

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| GET | `/api/knowledge/status/` | — | Number of indexed chunks |
| POST | `/api/knowledge/search/` | `{"query": "search term", "top_k": 3}` | Search the KB directly |
| POST | `/api/knowledge/index/` | `{"reset": true}` | Re-index via API |

## Using from Any Application

### Python SDK

```bash
pip install -e ./sdk
```

```python
from chatbot_sdk import ChatBot

bot = ChatBot("http://localhost:8000")
resp = bot.send("Hello!")
print(resp["response"])

# Continue conversation
resp = bot.send("Tell me more", session_id=resp["session_id"])

# Get history
history = bot.history(resp["session_id"])

# Clear session
bot.clear(resp["session_id"])
```

### JavaScript / Any Language

```javascript
const resp = await fetch("http://localhost:8000/api/chat/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: "hello", session_id: "optional-uuid" })
});
const data = await resp.json();
console.log(data.response);
```

## Docker

```bash
cp .env.example .env
docker-compose up --build
```

## Adding Custom NLP Providers

Create `chatbot/nlp/providers/my_provider.py`:

```python
from chatbot.nlp.providers.base import BaseProvider

class MyProvider(BaseProvider):
    def process(self, message, context=None):
        return {"intent": "custom", "confidence": 1.0, "response": "Hello from my provider"}
```

Register in `chatbot/nlp/__init__.py`:

```python
if name == "my_provider":
    from chatbot.nlp.providers.my_provider import MyProvider
    return MyProvider()
```

## Adding Custom Plugins

Create `chatbot/plugins/builtins/my_plugin.py`:

```python
from chatbot.plugins import registry
from chatbot.plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    name = "my_plugin"
    intents = ["my_intent"]

    def handle(self, intent, message, context=None):
        return {"intent": intent, "confidence": 1.0, "response": "Handled by my plugin"}

registry.register(MyPlugin)
```

Plugins auto-load on startup.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NLP_PROVIDER` | `rule_based` | NLP backend (`rule_based`, `rag`, `openai`) |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `OPENAI_API_KEY` | — | Required for openai provider |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | OpenAI model to use |
| `KNOWLEDGE_BASE_DIR` | `./knowledge_base` | Folder with documents to index |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model for embeddings |
| `SECRET_KEY` | `dev-secret-key...` | Django secret key |
| `DEBUG` | `1` | Debug mode |

## Project Structure

```
Chat-Bot/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── knowledge_base/          ← Drop your documents here
│   ├── faq.md
│   └── products.txt
├── chatbot/
│   ├── settings.py
│   ├── urls.py
│   ├── api/                 ← REST endpoints + session manager
│   ├── nlp/                 ← Pluggable NLP providers
│   │   └── providers/
│   │       ├── rule_based.py
│   │       ├── rag_provider.py
│   │       └── openai_provider.py
│   ├── knowledge/           ← RAG: loader, vectorstore, search
│   └── plugins/             ← Extensible plugin system
└── sdk/                     ← Python SDK for consumers
```

## License

MIT
