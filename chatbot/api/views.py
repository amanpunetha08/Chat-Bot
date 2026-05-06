from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatbot.api import session
from chatbot.nlp import get_provider
from chatbot.plugins import registry


class ChatView(APIView):
    def post(self, request):
        message = request.data.get("message")
        if not message:
            return Response({"error": "message is required"}, status=status.HTTP_400_BAD_REQUEST)

        session_id = request.data.get("session_id") or session.create_session()
        session.add_message(session_id, "user", message)

        # Get NLP response
        provider = get_provider()
        history = session.get_history(session_id)
        result = provider.process(message, context=history)

        # Check if a plugin should handle this intent
        plugin = registry.get_by_intent(result.get("intent", ""))
        if plugin:
            result = plugin.handle(result["intent"], message, context=history)

        response_text = result.get("response", "")
        session.add_message(session_id, "assistant", response_text)

        return Response({
            "session_id": session_id,
            "response": response_text,
            "intent": result.get("intent"),
            "confidence": result.get("confidence"),
        })


class HistoryView(APIView):
    def get(self, request, session_id):
        history = session.get_history(session_id)
        return Response({"session_id": session_id, "history": history})


class ClearSessionView(APIView):
    def delete(self, request, session_id):
        session.clear_session(session_id)
        return Response({"status": "cleared"})


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"})
