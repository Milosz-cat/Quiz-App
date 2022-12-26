from django.forms import ModelForm
from .models import Question, Quiz, Answer
from django import forms

class QuizForm(ModelForm):

    class Meta:
        model = Quiz
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create a Name for Quiz'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Create a Descrition for Quiz'}),
        }
        
        labels = {
            'name': '',
            'description': '',
        }


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['text']

        widgets = {
            # 'quiz': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose a Quiz'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create a Question'}),
        }

class AnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ['content', 'is_correct']


        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create an Answer'}),
            'is_correct': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Is the answer correct?'}),
        }