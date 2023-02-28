from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import QuizForm, QuestionForm, AnswerForm, Answer_Select_Form
from django.forms import formset_factory
from .models import Quiz, Question, Answer

from django.views.generic import DetailView
from django.core.paginator import Paginator

def sing_up(request):

    if request.method == "POST":
        #username = request.POST.get("username")
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password_1 = request.POST['pass1']
        password_2 = request.POST['pass2']

        my_user = User.objects.create_user(username, email, password_1)
        my_user.first_name = first_name
        my_user.last_name = last_name

        my_user.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect("sing_in")
                                               
    return render(request, 'base/sing_up.html')


def sing_in(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "Bad Credentials!")
            return redirect("sing_in")

    return render(request, 'base/sing_in.html')

def sing_out(request):
   logout(request)
   messages.success(request, "Logged Out Successfully!")
   return redirect('sing_in')

def home(request):

    quizzes = Quiz.objects.all()

    return render(request, 'base/home.html', {'quizzes': quizzes})

def create_quiz(request):  

    title = 'Create a new quiz!'
    form = QuizForm()

    if request.method == "POST":
        form = QuizForm(request.POST)  
        if form.is_valid():
            form.save()

        return redirect('home')
    
    context = {'form': form, 'title': title}
    return render(request, 'base/create.html', context)



def create_question(request, quiz_id):

    title = 'Create a new question!'
    form = QuestionForm()

    AnswerFormSet = formset_factory(AnswerForm, extra=4)
    formset = AnswerFormSet()

    if request.method == "POST":

        form = QuestionForm(request.POST)  
        formset = AnswerFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid() :

            messages.success(request, "Creating question Successfully!")
            
            question = form.save(commit=False)
            quiz = Quiz.objects.get(pk=quiz_id)
            question.quiz = quiz
            question.save()

            for answer_form in formset:
                answer = answer_form.save(commit=False)
                answer.question = question
                answer.save()
        else:
            messages.error(request, "Bad Credentials!")
        return redirect(reverse('start_quiz', kwargs={'pk': quiz_id}))

    context = {'form': form, 'formset': formset, 'title': title}
    return render(request, 'base/create.html', context)

class QuizDetailView(DetailView):

    model = Quiz
    template_name = 'base/start_quiz.html'
    context_object_name = 'quiz'




def question(request, quiz_id):

    Current_Quiz = Quiz.objects.get(id=quiz_id)
    Questions = Question.objects.filter(quiz=Current_Quiz)
        
    Answers = Answer.objects.all()
    list = []

    AnswerFormSet = formset_factory(Answer_Select_Form, extra=len(Questions))
    formset = AnswerFormSet()

    for i, form in enumerate(formset.forms):
        form.fields['answers'].queryset = Answers.filter(question=Questions[i])
        list.append((form, Questions[i]))

    context = {'quiz_id':quiz_id, 'list': list}
    return render(request, 'base/question.html', context)

def summary(request, quiz_id):

    points=0

    if request.method == 'POST' :
        print(request.POST)

        Current_Quiz = Quiz.objects.get(id=quiz_id)
        Questions = Question.objects.filter(quiz=Current_Quiz)
        
        for i in range(len(Questions)):
            selected_answers = request.POST.getlist(f'form-{i}-answers')
            all_answers = Answer.objects.filter(question=Questions[i])
            correct_answers = all_answers.filter(is_correct=1)


            for n in all_answers:
                if (str(n.pk) in selected_answers and n in correct_answers) or (str(n.pk) not in selected_answers and n not in correct_answers):
                    points+=1
    
    
    answers_count = len(Answer.objects.filter(question__quiz_id=quiz_id))
    percentages = round((points / answers_count) * 100)
    return render(request, 'base/summary.html', {'points': points, 'percentages':percentages})
