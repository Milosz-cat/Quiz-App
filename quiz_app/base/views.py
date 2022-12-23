from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import QuizForm, QuestionForm, AnswerForm
from .models import Quiz

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

    form = QuizForm()

    if request.method == "POST":
        form = QuizForm(request.POST)  
        if form.is_valid():
            form.save()

        return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/create_quiz.html', context)

def question(request):
    return render(request, 'base/question.html')

def start(request):
    return render(request, 'base/start.html')
