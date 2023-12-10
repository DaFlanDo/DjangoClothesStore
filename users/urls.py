from django.urls import path
from users.views import LoginView, UserRegisterView, UserProfileView, EmailVerificationView, \
    CustomPasswordResetConfirmView, PasswordResetView, CustomPasswordResetView, CustomPasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetDoneView

app_name = 'users'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='EmailVerif'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/done/', CustomPasswordChangeDoneView.as_view(), name='password_reset_done'),



]
