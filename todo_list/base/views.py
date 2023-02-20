from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import UserRegisterForm, UserLoginForm, CreateTaskForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages



def home_page(request):
    if request.user.is_authenticated:
        tasks = Task.objects.all().filter(user=request.user, done=False)
        unfinished = tasks.count()
        context = {'tasks': tasks, 'count': unfinished}
    else:
        context = {}
    return render(request, 'base/home.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back {username}')
                return redirect('home')
            else:
                messages.error(request, 'Login failed. Invalid username or password')
        else:
            messages.error(request, 'Login failed. Invalid username or password')
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
            return redirect('login')
        else:
            messages.error(request, form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'base/register.html', {'form': form})


def create_task(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if task:  # is it necessary? idk
                task.user_id = request.user.pk
                task.save()
                messages.success(request, 'The task has been created')
                return redirect('create')
            else:
                messages.error(request, 'couldn\'t upload the task to the database')
                return redirect('create')
        else:
            messages.error(request, 'Form is invalid. Cannot create the task')
    else:
        form = CreateTaskForm()
    return render(request, 'base/create_task.html', {'form': form})


def delete_task(request, task_id):
    if request.method == 'POST' and request.user.is_authenticated:
        obj = get_object_or_404(Task, pk=task_id, user_id=request.user.pk)
        if obj.done:
            res = 'stat'
        else:
            res = 'home'
        obj.delete()
        return redirect(f'{res}')

    return HttpResponseNotFound('Page not found')


def is_done(request, task_id):
    if request.method == 'POST' and request.user.is_authenticated:
        obj = get_object_or_404(Task, pk=task_id, user_id=request.user.pk)
        obj.done = True
        obj.save()
    return redirect('home')


def update_task(request, task_id):
    if not request.user.is_authenticated:
        return HttpResponseNotFound('Page not fount')
    obj = get_object_or_404(Task.objects.select_related('user'), pk=task_id, user_id=request.user.pk)
    if request.method == 'POST':
        form = CreateTaskForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = CreateTaskForm(instance=obj)
    context = {'form': form}
    return render(request, 'base/update_task.html', context)


def view_task(request, task_id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Task.objects.select_related('user'), pk=task_id, user_id=request.user.pk)
        context = {'task': obj}
        return render(request, 'base/view_task.html', context)
    return render(request, 'base/home.html')


def statistics(request):
    if request.user.is_authenticated:
        tasks_done = Task.objects.select_related('user').filter(user_id=request.user.pk, done=True)
        total_done = tasks_done.count()
        return render(request, 'base/statistics.html', {'done': tasks_done, 'total_done': total_done})

    return render(request, 'base/statistics.html')
