from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from quiz.models import Quiz, Question, Answer
from .helpers import send_forget_password_mail


def password_reset(request):
    """The function checks whether the user with the given e-mail exists,
    and if it exists, it sends an e-mail with a link to reset the password usign the second function.

    Args:
        request[email] (string): email of the user
    """

    if request.method == "POST":
        email = request.POST.get("email")

        if not User.objects.filter(email=email).first():
            messages.error(
                request, "The email you entered does not exist, Please try again!"
            )
            return redirect(request.path)
        else:
            user_obj = User.objects.get(email=email)

            if send_forget_password_mail(user_obj.email, user_obj.pk):
                messages.success(
                    request,
                    "A link to reset your password has been sent to your email.",
                )
                return render(request, "base/sign_in.html")

    return render(request, "reset/password_reset.html")


def password_reset_confirm(request, id, token):
    """The function checks the correctness of passwords, if it is correct,
    it resets and updates the password.

    Args:
        request.POST[password_1] (string): new password
        request.POST[password_2] (string): password confirmation
        id (int): object identifier
        token (string): generated link token for security

    """

    if request.method == "POST" and token:
        password_1 = request.POST["pass1"]
        password_2 = request.POST["pass2"]

        if password_1 != password_2:
            messages.error(
                request,
                "Setting your new password failed because the passwords are different. Try re-entering passwords.",
            )
            return redirect(request.path)
        else:
            messages.success(request, "Your password has been changed.")
            user = User.objects.get(id=id)
            user.set_password(password_1)
            user.save()
            return redirect("sign_in")

    return render(request, "reset/password_reset_confirm.html")

def confirm_correctness(request, model_name, id, token):
    """The function that will run after clicking the link confirming the creation
    of a quiz or question by one of the admins, depending on the type of model, 
    the model has a validated status as confirmed.

    Args:
        model_name (string): type of the model
        id (int): Identifier of the model
        token (string): Generated token for the security
    """
    if token and model_name == "Quiz":
        model = Quiz.objects.get(pk=id)

    elif token and model_name == "Question":
        model = Question.objects.get(pk=id)

        answers = Answer.objects.filter(question=model)
        for a in answers:
            a.is_confirmed = True
            a.save()

    model.is_confirmed = True
    model.save()

    messages.success(request, f"Confirming {model_name} Successfully!")
    return redirect("home")