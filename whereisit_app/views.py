from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SearchForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Item
import datetime


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


# Items.
class ItemListView(ListView):
    model = Item
    template_name = 'whereisit_app/home.html'
    context_object_name = 'items'
    ordering = ['name']


class ItemDetailView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        item = self.object
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        if item.when_borrowed:
            context['days_passed'] = timezone.now() - item.when_borrowed
            return context


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['name', 'image', 'category', 'description', 'location', 'is_borrowed', 'who_borrowed', 'when_borrowed']

    def form_valid(self, form):
        # https://stackoverflow.com/questions/18246326/how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
        item = form.save()
        item.users.add(self.request.user)
        item.save()
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'image', 'category', 'description', 'location', 'is_borrowed', 'who_borrowed', 'when_borrowed']
    template_name_suffix = '_update_form'


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/'


@login_required
def search(request):
    title = 'search results'
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            word = form.data['search_q']
            print(f'xxxxxxxxxxxxxxxxxx {word}')
            search1 = Item.objects.filter(name__icontains=word)
            search2 = Item.objects.filter(category__icontains=word)
            search3 = Item.objects.filter(location__icontains=word)
            print(f'xxxxxxxx{search1}, {search2}, {search3}')

            search = {}

            if search1:
                for item in search1:
                    search[item.id] = item
            if search2:
                for item in search2:
                    search[item.id] = item
            if search3:
                for item in search3:
                    search[item.id] = item

            results = search.values()

            context = {
                'title': title,
                'word': word,
                'results': results,
            }
            return render(request, 'whereisit_app/search_result.html', context=context)
