FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download embedding model and index knowledge base during build
RUN python manage.py index_knowledge --reset

# HF Spaces uses port 7860
EXPOSE 7860

CMD ["gunicorn", "chatbot.wsgi:application", "--bind", "0.0.0.0:7860", "--timeout", "120"]
