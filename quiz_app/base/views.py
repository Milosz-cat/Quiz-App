from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import QuizForm, QuestionForm, AnswerForm
from .models import Quiz

from django.views.generic import DetailView

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

def question(request):
    return render(request, 'base/question.html')

def create_question(request, quiz_id):

    title = 'Create a new question!'
    form = QuestionForm()

    if request.method == "POST":
        form = QuestionForm(request.POST)  
        if form.is_valid():

            question = form.save(commit=False)
            quiz = Quiz.objects.get(pk=quiz_id)
            question.quiz = quiz
            question.save()

        return redirect(reverse('start_quiz', kwargs={'pk': quiz_id}))

    context = {'form': form, 'title': title}
    return render(request, 'base/create.html', context)

# def create_answer(request, question_id):

#     title = 'Create answers!'
#     form1 = AnswerForm()
#     form2 = AnswerForm()
#     form3=  AnswerForm()
#     form4 = AnswerForm()

#     if request.method == "POST":

#         form1 = AnswerForm(request.POST)
#         form2 = AnswerForm(request.POST)
#         form3=  AnswerForm(request.POST)
#         form4 = AnswerForm(request.POST)

#         if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            
#             form1.save()
#             form2.save()
#             form3.save()
#             form4.save()

#         return redirect(reverse('start_quiz', kwargs={'pk': quiz_id}))

#     context = {'form1': form1,'form2': form2,'form3': form3,'form4': form4, 'title': title}
#     return render(request, 'base/create.html', context)

class QuizDetailView(DetailView):

    model = Quiz
    template_name = 'base/start_quiz.html'
    context_object_name = 'quiz'
