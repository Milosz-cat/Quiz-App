from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def login(request):
    return render(request, 'base/login.html')

def register(request):
    return render(request, 'base/register.html')

def category(request):
    return render(request, 'base/category.html')

def register(request):
    return render(request, 'base/register.html')

def question(request):
    return render(request, 'base/question.html')

def start(request):
    return render(request, 'base/start.html')
