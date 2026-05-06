from django.urls import path, include

urlpatterns = [
    path("api/", include("chatbot.api.urls")),
    path("api/knowledge/", include("chatbot.knowledge.urls")),
]
