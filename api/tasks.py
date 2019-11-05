from celery.app import shared_task
from celery.decorators import task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from socialapi import celery_app

@task(name="email_reset_pass")
def email_reset_pass(email, reset_pass):
    html_content = render_to_string(
        'mails/reset_pass.html',
        {'username': email, 'password': reset_pass}
    )
    text_content = strip_tags(html_content)
    subject = 'Восстановление аккаунта - plamber.com.ua'

    # send_mail(subject, "message", "consoko@ymail.com" ,[email])
    email = EmailMultiAlternatives(subject, text_content, to=[email])
    email.attach_alternative(html_content, 'text/html')
    email.send()

