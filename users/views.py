from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.urls import reverse, reverse_lazy
from products.models import  Baskets
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from common.views import TitleMixin

# Авторизация
class LoginView(TitleMixin,LoginView):
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    title ='Store - Авторизация'


# Регистрация
class UserRegisterView(TitleMixin,SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались'
    title = 'Store - Регистрация'


# Профиль

class UserProfileView(TitleMixin,UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Store - Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile',args=(self.object.id))

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
        email_verifications = EmailVerification.objects.filter(code=code,user = user)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verification = True
            user.save()
            return super(EmailVerificationView,self).get(request,*args,**kwargs)
        else:
            reverse('index')

