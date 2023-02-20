from django.forms import ModelForm
from django import forms
from .models import Question, Quiz, Answer
from django.forms.widgets import CheckboxInput

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
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create a Question'}),
        }

class AnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ['content', 'is_correct']

        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create an Answer'}),
            'is_correct': CheckboxInput(),
        }

class Answer_Select_Form(forms.Form):
    answers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=None,
        label='',
    )

    