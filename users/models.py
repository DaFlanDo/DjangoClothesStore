from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.template.loader import render_to_string
import uuid

from django.urls import reverse
from django.utils.timezone import now


# Добавление модели кастомного пользвателя


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    email = models.EmailField("email address", blank=True, unique=True)
    is_verification = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    on_created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Email верификация для {self.user}'

    def send_verification_code(self):
        link = reverse('users:EmailVerif', kwargs={'email': self.user.email, 'code': self.code})
        verif_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'To confirm mail in the service Store for {self.user.username}'
        message = f'To confirm mail in service Store go to link {verif_link}'
        print(self.user.email)

        send_mail(
            subject=subject,
            message = '',
            html_message= render_to_string('users/Mail.html',{'verif_link':verif_link,'username':self.user.username}),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False


