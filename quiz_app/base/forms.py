from django.forms import ModelForm
from django import forms
from .models import Question, Quiz, Answer
from django.forms.widgets import CheckboxInput


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Create a Name for Quiz"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Create a Descrition for Quiz",
                }
            ),
        }

        labels = {
            "name": "",
            "description": "",
        }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["text"]

        widgets = {
            "text": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Create a Question"}
            ),
        }
        labels = {
            "text": "",
        }


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["content", "is_correct"]

        widgets = {
            "content": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Create an Answer"}
            ),
            "is_correct": CheckboxInput(
            attrs={
            "class": "form-check-input",
            "style": "width: 1.5rem; height: 1.5rem; margin-top: 0.3rem;"}
            ),
        }
        labels = {
            "content": "",
        }


class Answer_Select_Form(forms.Form):
    answers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=None,
        label="",
    )
