from django.urls import path
from . import views

urlpatterns = [
    path('',  views.home, name='home'),
    path('sing_up/',  views.sing_up, name='sing_up'),
    path('sing_in/',  views.sing_in, name='sing_in'),
    path('sing_out/',  views.sing_out, name='sing_out'),
    path('question/',  views.question, name='question'),
    path('start/',  views.start, name='start'),
]

