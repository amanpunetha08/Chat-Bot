from django.urls import path
from chatbot.api import views

urlpatterns = [
    path("chat/", views.ChatView.as_view()),
    path("history/<str:session_id>/", views.HistoryView.as_view()),
    path("session/<str:session_id>/", views.ClearSessionView.as_view()),
    path("health/", views.HealthView.as_view()),
]
