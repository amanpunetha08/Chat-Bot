FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment
ENV NLP_PROVIDER=gemini
ENV KNOWLEDGE_BASE_DIR=/app/knowledge_base
ENV DEBUG=0

# Pre-download embedding model and index knowledge base during build
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
RUN python manage.py index_knowledge --reset

# Make sure data is readable
RUN chmod -R 777 /app/knowledge_base

EXPOSE 7860

CMD ["gunicorn", "chatbot.wsgi:application", "--bind", "0.0.0.0:7860", "--timeout", "120"]
