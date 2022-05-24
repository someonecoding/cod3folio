from __future__ import absolute_import, unicode_literals
from .models import CustomUser

from profile_django.celery import app

from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token


@app.task
def confirm_email(userpk):
    user = CustomUser.objects.get(pk=userpk)
    
    
    email_subject = 'qwerty'
    email_body = 'http://cod3folio.herokuapp.com' + reverse_lazy('accounts:activate', 
    
    kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
    
    })
    print(email_subject)
    email = EmailMessage(
        email_subject,
        email_body,
        'noreply@scraper.com',
        [user.email]
    )
    email.send(fail_silently=False)
