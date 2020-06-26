from django.shortcuts import render


def home(request):
    title = "Home"
    return render(request, 'whereisit_app/home.html', {'title': title})
