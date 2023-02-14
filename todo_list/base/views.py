from django.shortcuts import render, redirect
from .models import Task
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def home_page(request):
    if request.user.is_authenticated:
        tasks = Task.objects.all().filter(user=request.user)
        context = {'tasks': tasks}
    else:
        context = {}
    return render(request, 'base/home.html', context)


def user_login(request):
    # if request.method == 'POST':
    #     form = UserLoginForm(data=request.POST)
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'Login failed')
    # else:
    #     form = UserLoginForm()
    # return render(request, 'base/login.html', {'form': form})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {username}')
            return redirect('home')
        else:
            messages.error(request, 'Login failed')
    form = UserLoginForm()
    return render(request, 'base/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You've successfully registered")
            return redirect(request, 'login')
        else:
            messages.error(request, 'Registration failed')
    else:
        form = UserRegisterForm()
    return render(request, 'base/register.html', {'form': form})
