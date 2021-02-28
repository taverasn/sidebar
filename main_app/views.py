import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account
from django.contrib.auth.models import User

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/dashboard/accounts')
        else:
            error_message = 'Invalid sign up - try again'
    
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def home(request):
    return render(request, 'home.html')

@login_required
def topics_index(request):
    return render(request, 'topics/index.html')

# Account Views

@login_required
def dashboard_index(request):
    return render(request, 'dashboard/index.html')

@login_required
def account_dashboard(request):
    return render(request, 'dashboard/account.html')


class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['first_name', 'last_name', 'email', 'bio']
    success_url = '/topics/'
    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['first_name', 'last_name', 'email', 'bio']
    success_url = '/dashboard/'

class AccountDelete(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = '/'
