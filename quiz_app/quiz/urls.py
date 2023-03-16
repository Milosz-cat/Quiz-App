from django.urls import path
from . import views

urlpatterns = [
    path("create_quiz/", views.create_quiz, name="create_quiz"),
    path("create_question/<int:quiz_id>/", views.create_question, name="create_question"),
    path("start_quiz/<int:pk>/", views.QuizDetailView.as_view(), name="start_quiz"),
    path("quiz/<int:quiz_id>/", views.question, name="question"),
    path("summary/<int:quiz_id>/", views.summary, name="summary"),
]
