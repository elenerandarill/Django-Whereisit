from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def home(request):
    title = "Home"
    return render(request, 'whereisit_app/home.html', {'title': title})


def register(request):
    title = 'Register'
    if request.method == 'GET':
        form = UserRegisterForm()
        return render(request, 'whereisit_app/register.html', {'title': title, 'form': form})
    else:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You may now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong')
            return render(request, 'whereisit_app/register.html', {'title': title, 'form': form})


def login(request):
    title = 'Log In'
    return render(request, 'whereisit_app/login.html', {'title': title})
