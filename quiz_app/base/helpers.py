from django.core.mail import send_mail
import uuid
from django.conf import settings

def send_forget_password_mail(email, pk):
    
    token= str(uuid.uuid4())
    id=pk
    subject = "Reset your password for Django Quiz"
    massage = f'To reset your password, click the following link: http://127.0.0.1:8000/password_reset_confirm/{id}/{token}/'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, massage, from_email, recipient_list)
    
    return True