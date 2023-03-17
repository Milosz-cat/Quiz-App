from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import formset_factory
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import QuizForm, QuestionForm, AnswerForm, Answer_Select_Form
from .models import Quiz, Question, Answer, LeaderBoard
from reset.helpers import send_confirm_correctness

from datetime import timedelta


class QuizDetailView(LoginRequiredMixin, DetailView):
    """The class inherits from DetailView to display the quiz details in the templete
    and from LoginRequiredMixin to redirect the user to login if he wants to access
    the quiz without logging in.
    """

    login_url = "/sign_in/"
    model = Quiz
    template_name = "quiz/start_quiz.html"
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
    return render(request, "quiz/create.html", context)


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
    return render(request, "quiz/create.html", context)

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
    return render(request, "quiz/question.html", context)


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
        "quiz/summary.html",
        {"points": points, "percentages": percentages, "leaderboard": leaderboard},
    )

