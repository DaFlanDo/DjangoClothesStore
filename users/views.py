from django.shortcuts import render, redirect
from users.models import User
from users.forms import UserLoginForm,UserRegisterForm
from django.urls import reverse
from django.contrib import auth


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
    form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html',context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {'form': form}

    return render(request, 'users/register.html',context)
def logout(request):
    auth.logout(request)
    return redirect(reverse('users:login'))