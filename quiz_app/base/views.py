from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import QuizForm, QuestionForm, AnswerForm, Answer_Select_Form
from .models import Quiz, Question, Answer, LeaderBoard
from .helpers import send_forget_password_mail, send_confirm_correctness

from datetime import timedelta


class QuizDetailView(LoginRequiredMixin, DetailView):
    """The class inherits from DetailView to display the quiz details in the templet
    and from LoginRequiredMixin to redirect the user to login if he wants to access
    the quiz without logging in.
    """

    login_url = "sing_in/"
    model = Quiz
    template_name = "base/start_quiz.html"
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        """Function count all confirmed questions belonging to the quiz,
        if their number is less than 3 the user must create several questions.

        Returns:
            question_count (int): number of confirmed questions.
        """
        context = super().get_context_data(**kwargs)
        confirmed_questions = self.object.question_set.filter(is_confirmed=True)
        context["question_count"] = confirmed_questions.count()
        return context


def password_reset(request):
    """The function checks whether the user with the given e-mail exists,
    and if it exists, it sends an e-mail with a link to reset the password using the second function.

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
                return render(request, "base/sing_in.html")

    return render(request, "base/password_reset.html")


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
            return redirect("sing_in")

    return render(request, "base/password_reset_confirm.html")


def sing_up(request):
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
            return render(request, "base/sing_up.html")

        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "User with given emails already exists, use another email address.",
            )
            return render(request, "base/sing_up.html")

        password_1 = request.POST["pass1"]
        password_2 = request.POST["pass2"]

        if password_1 != password_2:
            messages.error(
                request,
                "Verification of your passwords failed because the passwords are different. Try re-entering passwords.",
            )
            return render(request, "base/sing_up.html")

        my_user = User.objects.create_user(username, email, password_1)
        my_user.first_name = first_name
        my_user.last_name = last_name

        my_user.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect("sing_in")

    return render(request, "base/sing_up.html")


def sing_in(request):
    """The function checks the correctness of the login details,
    if correct, logs the user in.

    Args:
        request: user data directory
    """

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]
        print(request.POST)
        user = authenticate(username=username, password=pass1)

        if user:
            login(request, user)
            return redirect("home")

        else:
            messages.error(request, "Bad Credentials!")
            return redirect("sing_in")

    return render(request, "base/sing_in.html")


def sing_out(request):
    """
    Logs out the user.
    """
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect("sing_in")


@login_required
def home(request):
    """A function that displays all quizzes. login is required to view
    quizzes otherwise we will be redirected to the login page
    """

    quizzes = Quiz.objects.filter(is_confirmed=True)
    # Quiz.objects.filter(name='#').delete()
    return render(request, "base/home.html", {"quizzes": quizzes})


@login_required
def create_quiz(request):
    """Function for the first time displays a form thanks to which we will create a quiz,
    then depending on whether we have an admin status, it will immediately create an approved quiz
    or create an unapproved quiz and send an email to each admin in which he will be able to check
    the correctness of the quiz. Login is required.

    Args:
        form (QuizForm): Form with data to create a quiz.

    Returns:
        form (QuizForm): Ready form to create a quiz.
    """

    title = "Create a new quiz!"
    form = QuizForm()

    if request.method == "POST":
        form = QuizForm(request.POST)

        if form.is_valid():
            form.save()

        quiz = Quiz.objects.get(name=request.POST["name"])

        if request.user.is_staff:
            quiz.is_confirmed = True
            quiz.save()

            messages.success(request, "Creating quiz Successfully!")
        else:
            admins = User.objects.filter(is_staff=True)
            admin_emails = [admin.email for admin in admins]
            if send_confirm_correctness(admin_emails, quiz) == len(admins):
                messages.info(
                    request,
                    "Since you are not an administrator, you must wait for an administrator to approve your quiz!",
                )

        return redirect("home")

    context = {"form": form, "title": title}
    return render(request, "base/create.html", context)


@login_required
def create_question(request, quiz_id):
    """The first time function sends a ready form to create a question with 4 answers, then,
    depending on the user's status, they create a confirmed question or send information 
    to the admins. Login is required.

    Args:
        form (QuestionForm): Form with data to create a question.
        quiz_id (int): Id of quizz to which the created questions belong.

    Returns:
        form (QuestionForm): Ready form to create a question.
    """

    title = "Create a new question!"
    form = QuestionForm()

    AnswerFormSet = formset_factory(AnswerForm, extra=4)
    formset = AnswerFormSet()

    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = AnswerFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            quiz = Quiz.objects.get(pk=quiz_id)
            question.quiz = quiz
            question.save()

            for answer_form in formset:
                answer = answer_form.save(commit=False)
                answer.question = question
                if request.user.is_staff:
                    answer.is_confirmed = True
                answer.save()

            if request.user.is_staff:
                question.is_confirmed = True
                question.save()
                messages.success(request, "Creating question Successfully!")
            else:
                admins = User.objects.filter(is_staff=True)
                admin_emails = [admin.email for admin in admins]
                if send_confirm_correctness(admin_emails, question) == len(admins):
                    messages.info(
                        request,
                        "Since you are not an administrator, you must wait for an administrator to approve your question!",
                    )

        else:
            messages.error(request, "Bad Credentials!")

        return redirect(reverse("start_quiz", kwargs={"pk": quiz_id}))

    context = {"form": form, "formset": formset, "title": title}
    return render(request, "base/create.html", context)


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


@login_required
def question(request, quiz_id):
    """The function returns the entire content of the question in the form 
    of forms in which we will be able to send answers, only approved answers
    are returned. Questions and answers are sent in the form of a list of 
    tuples to make it easier to simultaneously unpack them later in the template. Login is required

    Args:
        quiz_id (int): Identifier of the Quiz

    Returns:
        context (dictionary): Dictionary with a list of tuples.
    """
    Current_Quiz = Quiz.objects.get(id=quiz_id)
    Questions = Question.objects.filter(quiz=Current_Quiz).filter(is_confirmed=True)

    Answers = Answer.objects.all().filter(is_confirmed=True)
    AnswerFormSet = formset_factory(Answer_Select_Form, extra=len(Questions))
    formset = AnswerFormSet()

    list = []
    for i, form in enumerate(formset.forms):
        """We create a list in which each cell is a tuple consisting of a question 
        and a form with 4 answers. This facilitates subsequent simultaneous unpacking in a teplatce
        """
        form.fields["answers"].queryset = Answers.filter(question=Questions[i])
        list.append((form, Questions[i]))

    context = {"quiz_id": quiz_id, "list": list}
    return render(request, "base/question.html", context)


@login_required
def summary(request, quiz_id):
    """The function counts the points scored during the quiz on the basis of submitted forms,
    the quiz is multi-choice, i.e. 1 point or zero for each question. The function receives
    the time of solving the quiz calculated on the basis of the script in the template.
    If a user has one of the top 5 results, he is added to the list of top users. Login required.
    Args:
        request.POST[form-{i}-answers] (bool): Information whether a given answer field has been checked.
        request.POST[duration] (string): Duration of the quiz in milliseconds.
        quiz_id (int): Identifier of the Quiz.

    Returns:
        points (int): The number of points scored by the user( also in procentages).
        leaderboard (list): The list of 5 best results.
    """
    points = 0

    Current_Quiz = Quiz.objects.get(id=quiz_id)
    Questions = Question.objects.filter(quiz=Current_Quiz)

    if request.method == "POST":
        for i in range(len(Questions)):
            selected_answers = request.POST.getlist(f"form-{i}-answers")
            all_answers = Answer.objects.filter(question=Questions[i])
            correct_answers = all_answers.filter(is_correct=1)

            for n in all_answers:
                """The user gets a point if the selected answer is in the correct answers
                or if he did not mark the answer and it is incorrect.
                """
                if (str(n.pk) in selected_answers and n in correct_answers) or (
                    str(n.pk) not in selected_answers and n not in correct_answers
                ):
                    points += 1

        username = request.user.username
        duration = str(timedelta(milliseconds=int(request.POST["duration"])))[2:10]
        score = LeaderBoard(
            quiz=Current_Quiz, username=username, score=points, time=duration
        )
        score.save()

    # leaderboard = LeaderBoard.objects.filter(quiz=Current_Quiz).delete()
    leaderboard = LeaderBoard.objects.filter(quiz=Current_Quiz).order_by(
        "-score", "time"
    )[:5]
    if len(leaderboard) > 5:
        """If the length of the list after adding the result obtained a moment ago exceeds 5 people,
        the best 5 are determined and the rest (i.e. objects whose id is not in the leaderborad ) are removed
        """
        LeaderBoard.objects.exclude(pk__in=leaderboard).delete()

    answers_count = len(Answer.objects.filter(question__quiz_id=quiz_id))
    percentages = round((points / answers_count) * 100)

    return render(
        request,
        "base/summary.html",
        {"points": points, "percentages": percentages, "leaderboard": leaderboard},
    )
