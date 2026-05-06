from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from chatbot.knowledge import vectorstore
from chatbot.knowledge.loader import load_documents, chunk_text


class KnowledgeStatusView(APIView):
    def get(self, request):
        return Response({
            "total_chunks": vectorstore.count(),
            "knowledge_dir": settings.KNOWLEDGE_BASE_DIR,
        })


class KnowledgeSearchView(APIView):
    def post(self, request):
        query = request.data.get("query")
        top_k = request.data.get("top_k", 3)
        if not query:
            return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)
        results = vectorstore.search(query, top_k=top_k)
        return Response({"query": query, "results": results})


class KnowledgeIndexView(APIView):
    def post(self, request):
        """Re-index the knowledge base from the configured directory."""
        reset = request.data.get("reset", False)
        if reset:
            vectorstore.reset()

        docs = load_documents(settings.KNOWLEDGE_BASE_DIR)
        if not docs:
            return Response({"message": "No documents found"}, status=status.HTTP_404_NOT_FOUND)

        total_chunks = 0
        for doc in docs:
            chunks = chunk_text(doc["content"])
            metadatas = [{"source": doc["source"], "type": doc["type"]}] * len(chunks)
            vectorstore.add_documents(chunks, metadatas)
            total_chunks += len(chunks)

        return Response({"documents": len(docs), "chunks": total_chunks})
