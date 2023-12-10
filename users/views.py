from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from store import settings
from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, CustomPasswordResetForm, \
    UserSetNewPasswordForm
from django.urls import reverse, reverse_lazy
from products.models import Baskets
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, \
    PasswordChangeDoneView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from common.views import TitleMixin


# Авторизация
class LoginView(TitleMixin, LoginView):
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    title = 'Store - Авторизация'


# Регистрация
class UserRegisterView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались'
    title = 'Store - Регистрация'


# Профиль

class UserProfileView(TitleMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Store - Профиль'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Baskets.objects.filter(user=self.object)
        return context


# Подтверждение почты


class EmailVerificationView(TitleMixin, TemplateView):
    model = User
    template_name = 'users/email_verification.html'
    title = 'Store| Подтверждение почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(code=code, user=user)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verification = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            HttpResponse(reverse('index'))


class CustomPasswordResetView(PasswordResetView,LoginRequiredMixin):
    template_name = 'reset_pass/form_reset.html'
    success_message = 'Сообщение отправлено на вашу почту'

    success_url = reverse_lazy('users:password_reset_done')
    html_email_template_name = 'reset_pass/mail.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        # Проверка, что пользователь с таким email существует
        if not User.objects.filter(email=email).exists():
            form.add_error('email', 'Пользователь с указанным адресом электронной почты не найден.')
            return self.form_invalid(form)
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "reset_pass/reset_pass_confirm.html"
    success_url = reverse_lazy('users:login')  # Укажите URL для страницы авторизации


class CustomPasswordChangeDoneView(PasswordResetView):
    template_name = 'users/pass_reset_done.html'
