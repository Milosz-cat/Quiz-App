from django.core.mail import send_mail
from django.conf import settings
import uuid

def send_forget_password_mail(email, pk):
    
    token= str(uuid.uuid4())
    subject = "Reset your password for Django Quiz"
    massage = f'To reset your password, click the following link: http://127.0.0.1:8000/password_reset_confirm/{pk}/{token}/'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    
    return send_mail(subject, massage, from_email, recipient_list)


def send_confirm_correctness(admin_emails, model_name, id):

    token= str(uuid.uuid4())
    subject = f"Confirm the correctness of the {model_name} for Django Quiz"
    massage = f'If the {model_name} is correct and You want to add it to the database, click on the following link: http://127.0.0.1:8000/confirm_correctness/{model_name}/{id}/{token}/'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = admin_emails
    
    return send_mail(subject, massage, from_email, recipient_list)
