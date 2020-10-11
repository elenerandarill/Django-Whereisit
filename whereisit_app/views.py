from random import randint

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SearchForm
from .models import Profile, Item, GroupOfUsers, User
import datetime


def home(request):
    title = "Home"
    return render(request, 'whereisit_app/home.html', {'title': title})


def register(request):
    title = 'Register'

    ######## hack
    print("check init needed")
    all_groups = GroupOfUsers.objects.all()
    if len(all_groups) == 0:
        print("init!!!!!!")
        rodzice = GroupOfUsers.objects.create(name='Rodzice')
        rodzice.save()
        dzieci = GroupOfUsers.objects.create(name='Dzieci')
        dzieci.save()

        user1 = User.objects.create(username='elener', email='elener@wp.pl', is_superuser=True)
        user1.set_password('testing666')
        user1.u_groups.add(rodzice)
        user1.u_groups.add(dzieci)
        user1.save()
        user2 = User.objects.create(username='norbi', email='norbi@wp.pl')
        user2.set_password('testing666')
        user2.u_groups.add(rodzice)
        user2.save()
        user3 = User.objects.create(username='ala', email='ala@wp.pl')
        user3.set_password('testing666')
        user3.u_groups.add(dzieci)
        user3.save()

        parasolka = Item.objects.create(name='Parasolka', category='Other', location='Korytarz')
        parasolka.groups.add(rodzice)
        parasolka.save()
        misio = Item.objects.create(name='Miś', category='Toys', location='Dzieciecy')
        misio.groups.add(dzieci)
        misio.save()
        pilka = Item.objects.create(name='Piłka', category='Other', location='Goscinny')
        pilka.groups.add(rodzice)
        pilka.groups.add(dzieci)
        pilka.save()
    # all_items = Item.objects.all()
    # if len(all_items) == 0:

    #############

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
    test1 = request.user.groups
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
    # This is send over to the form.
    context_object_name = 'items'
    ordering = ['name']

    def get_queryset(self):
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
    fields = ['name', 'image', 'category', 'description', 'location', 'is_borrowed', 'who_borrowed', 'when_borrowed', 'groups']

    # def form_valid(self, form):
    #     # https://stackoverflow.com/questions/18246326/how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
    #     item = form.save()
    #     # Saving current user into the Item info.
    #     item.groups(self.request.user.u_groups.all())
    #     item.save()
    #     return super().form_valid(form)     # ?


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'image', 'category', 'description', 'location', 'is_borrowed', 'who_borrowed', 'when_borrowed']
    # uses a template_name_suffix of '_form', so we change that.
    template_name_suffix = '_update_form'


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/'


def map_location(request):
    title = 'Map'
    return render(request, 'whereisit_app/map.html', {'title': title})


# Not working yet.
@login_required
def search(request):
    title = 'search results'
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            word = form.data['search_q']
            search1 = Item.objects.filter(name__icontains=word)
            search2 = Item.objects.filter(category__icontains=word)
            search3 = Item.objects.filter(location__icontains=word)

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
