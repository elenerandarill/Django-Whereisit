from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SearchForm
from .models import Profile, Item, GroupOfUsers, User
from .basic_setup import basic_setup


def home(request):
    return render(request, 'whereisit_app/home.html')


def register(request):
    # Provides basic data for database.
    all_groups = GroupOfUsers.objects.all()
    if len(all_groups) == 0:
        basic_setup()

    if request.method == 'GET':
        form = UserRegisterForm()
        return render(request, 'whereisit_app/register.html', {'form': form})
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
            return render(request, 'whereisit_app/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'GET':
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'whereisit_app/profile.html', {'u_form': u_form, 'p_form': p_form})
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
    # This is send over to the form.
    context_object_name = 'items'
    ordering = ['name']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            groups = self.request.user.u_groups.all()
            return Item.objects.distinct().filter(groups__in=groups)


class ItemDetailView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        item = self.object
        context = super().get_context_data(**kwargs)
        if item.when_borrowed:
            context['days_passed'] = timezone.now() - item.when_borrowed
        return context


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['name', 'image', 'category', 'description', 'is_borrowed', 'who_borrowed', 'when_borrowed', 'groups', 'location']


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'image', 'category', 'description', 'is_borrowed', 'who_borrowed', 'when_borrowed', 'groups', 'location']
    # uses a template_name_suffix of '_form', so we change that.
    template_name_suffix = '_update_form'


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/'


def map_location(request):
    return render(request, 'whereisit_app/map.html')


@login_required
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            word = form.data['search_q']
            results = []

            search1 = Item.objects.filter(name__icontains=word)
            if search1:
                for item in search1:
                    results.append(item)

            search2 = Item.objects.filter(category__icontains=word)
            if search2:
                for item in search2:
                    if item not in results:
                        results.append(item)

            context = {
                'word': word,
                'results': results,
            }
            return render(request, 'whereisit_app/search_result.html', context=context)
