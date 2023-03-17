from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from quiz.models import Quiz


def sign_up(request):
    """The function checks if a user with similar data does not already exist,
    if not creating a new user.

    Args:
        request: user data directory
    """

    if request.method == "POST":
        username = request.POST["username"]

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "User with given username already exists, use another username.",
            )
            return render(request, "base/sign_up.html")

        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "User with given emails already exists, use another email address.",
            )
            return render(request, "base/sign_up.html")

        password_1 = request.POST["pass1"]
        password_2 = request.POST["pass2"]

        if password_1 != password_2:
            messages.error(
                request,
                "Verification of your passwords failed because the passwords are different. Try re-entering passwords.",
            )
            return render(request, "base/sign_up.html")

        my_user = User.objects.create_user(username, email, password_1)
        my_user.first_name = first_name
        my_user.last_name = last_name

        my_user.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect("sign_in")

    return render(request, "base/sign_up.html")


def sign_in(request):
    """The function checks the correctness of the login details,
    if correct, logs the user in.

    Args:
        request: user data directory
    """

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]
        user = authenticate(username=username, password=pass1)

        if user:
            login(request, user)
            next_url = request.GET.get("next")
            print(next_url)
            if next_url:
                return redirect(next_url)
            else:
                return redirect("home")

        else:
            messages.error(request, "Bad Credentials!")
            return redirect(request.path)

    return render(request, "base/sign_in.html")


def sign_out(request):
    """
    Logs out the user.
    """
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect("sign_in")


@login_required
def home(request):
    """A function that displays all quizzes. login is required to view
    quizzes otherwise we will be redirected to the login page
    """

    quizzes = Quiz.objects.filter(is_confirmed=True)
    return render(request, "base/home.html", {"quizzes": quizzes})
