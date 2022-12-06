from django.urls import path
from . import views

urlpatterns = [
    path('',  views.home, name='home'),
    path('login/',  views.login, name='login'),
    path('register/',  views.register, name='register'),
    path('category/',  views.category, name='category'),
    path('question/',  views.question, name='question'),
    path('start/',  views.start, name='start'),
]
