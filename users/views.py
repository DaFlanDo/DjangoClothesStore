from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from users.models import User
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.urls import reverse
from django.contrib import auth, messages
from products.models import Product, Baskets
from django.contrib.auth.decorators import login_required

# Авторизация
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html',context)


# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            messages.success(request, 'Вы успешно зарегистрировались,выполните вход')
            form.save()
            return redirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {'form': form}

    return render(request, 'users/register.html', context)


# Профиль
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance= request.user,data = request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            return redirect(reverse('users:profile'))
    form = UserProfileForm(instance=request.user)
    context = {'title': 'Store', 'form': form,'baskets': Baskets.objects.filter(user=request.user)}
    return render(request, 'users/profile.html', context)


# Выход
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))
