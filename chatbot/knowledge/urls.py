from django.urls import path
from chatbot.knowledge import views

urlpatterns = [
    path("status/", views.KnowledgeStatusView.as_view()),
    path("search/", views.KnowledgeSearchView.as_view()),
    path("index/", views.KnowledgeIndexView.as_view()),
]
