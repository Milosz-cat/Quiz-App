from django.urls import path
from . import views

urlpatterns = [
    path('',  views.home, name='home'),
    path('sing_up/',  views.sing_up, name='sing_up'),
    path('sing_in/',  views.sing_in, name='sing_in'),
    path('sing_out/',  views.sing_out, name='sing_out'),
    path('question/',  views.question, name='question'),
    path('start_quiz/<int:pk>',  views.QuizDetailView.as_view(), name='start_quiz'),
    path('create_quiz/',  views.create_quiz, name='create_quiz'),
    path('create_question/<int:quiz_id>',  views.create_question, name='create_question'),
    path('quiz/<int:quiz_id>',  views.question, name='question'),
    path('summary/<int:quiz_id>',  views.summary, name='summary'),

]

