from django.shortcuts import render


def home(request):
    title = "Home"
    return render(request, 'whereisit_app/home.html', {'title': title})


def register(request):
    title = 'Register'
    return render(request, 'whereisit_app/register.html', {'title': title})


def login(request):
    title = 'Log In'
    return render(request, 'whereisit_app/login.html', {'title': title})
