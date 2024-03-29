from django.core.mail import send_mail
from django.conf import settings
import uuid


def send_forget_password_mail(email, pk):
    """The function sends an e-mail containing a link to reset the password,
    a token is generated for security reasons.

    Args:
        email (string): User email address
        pk (_type_): Identifier of the model

    Returns:
        send_mail (function): Function returns number of successfully sent emails.
    """
    token = str(uuid.uuid4())
    subject = "Reset your password for Django Quiz"
    massage = f"To reset your password, click the following link: http://127.0.0.1:8000/password_reset_confirm/{pk}/{token}/"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [
        email,
    ]

    return send_mail(subject, massage, from_email, recipient_list)


def send_confirm_correctness(admin_emails, model):
    """The function sends a message to each admin presenting a quiz or a question with answers,
    if the admin finds it correct, after clicking the link, the status of the given object will
    be changed to confirmed ,a token is generated for security reasons.

    Args:
        admin_emails (list of string): Admins email addresses
        model (Quiz or Question): An object of a given type

    Returns:
        send_mail (function): Function returns number of successfully sent emails.
    """
    token = str(uuid.uuid4())
    id = model.pk
    subject = (
        f"Confirm the correctness of the {model._meta.object_name} for Django Quiz"
    )

    if str(model._meta.object_name) == "Quiz":
        massage = f"Quiz name: \n {model.name} \n Quiz description: \n{model.description} \n\n If the {model._meta.object_name} is correct and you want to add it to the database, click on the following link: http://127.0.0.1:8000/confirm_correctness/{model._meta.object_name}/{id}/{token}/"

    elif str(model._meta.object_name) == "Question":
        massage = f" Question: \n {model.text} \n\n Answers: \n"
        
        answers = model.answer_set.all()

        for answer in answers:
            if answer.is_correct:
                massage += f"\u25CF {answer} (Correct answer) \n"
            else:
                massage += f"\u25CF {answer} \n"
        massage += f"\nIf the {model._meta.object_name} is correct and you want to add it to the database, click on the following link: http://127.0.0.1:8000/confirm_correctness/{model._meta.object_name}/{id}/{token}/"

    from_email = settings.EMAIL_HOST_USER
    recipient_list = admin_emails

    return send_mail(subject, massage, from_email, recipient_list)
