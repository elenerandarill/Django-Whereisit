from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


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
            print("form.save() 1")
            form.save()
            print("form.save() 2")
            messages.success(request, 'Account created! You may now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong')
            return render(request, 'whereisit_app/register.html', {'title': title, 'form': form})


@login_required
def profile(request):
    title = 'Your Profile.'
    if request.method == 'GET':
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'whereisit_app/profile.html', {'title': title, 'u_form': u_form, 'p_form': p_form})
    else:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Something went wrong.')

