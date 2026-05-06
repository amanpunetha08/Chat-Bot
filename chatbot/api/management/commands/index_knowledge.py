from django.core.management.base import BaseCommand
from django.conf import settings

from chatbot.knowledge.loader import load_documents, chunk_text
from chatbot.knowledge import vectorstore


class Command(BaseCommand):
    help = "Index documents from knowledge_base/ folder into the vector store"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Clear existing index before indexing")
        parser.add_argument("--dir", type=str, default=settings.KNOWLEDGE_BASE_DIR, help="Directory to index")

    def handle(self, *args, **options):
        directory = options["dir"]

        if options["reset"]:
            vectorstore.reset()
            self.stdout.write("Cleared existing index.")

        docs = load_documents(directory)
        if not docs:
            self.stdout.write(self.style.WARNING(f"No documents found in {directory}"))
            return

        total_chunks = 0
        for doc in docs:
            chunks = chunk_text(doc["content"])
            metadatas = [{"source": doc["source"], "type": doc["type"]}] * len(chunks)
            vectorstore.add_documents(chunks, metadatas)
            total_chunks += len(chunks)
            self.stdout.write(f"  Indexed: {doc['source']} ({len(chunks)} chunks)")

        self.stdout.write(self.style.SUCCESS(f"Done! Indexed {len(docs)} documents, {total_chunks} chunks total."))
