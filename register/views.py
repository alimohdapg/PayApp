from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import RegisterForm
from payapp.forms import AccountForm


@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('logout_user'))
def register_admin(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_staff = True
            user.save()
            register_form = RegisterForm()
            return render(request, 'register/register_admin.html',
                          {'admin_created': True, 'register_form': register_form})
        else:
            return render(request, 'register/register_admin.html',
                          {'failed_signup': True, 'register_form': register_form})
    else:
        register_form = RegisterForm()
    return render(request, 'register/register_admin.html',
                  {'register_form': register_form})


@transaction.atomic
def register_user(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        account_form = AccountForm(request.POST)
        if register_form.is_valid() and account_form.is_valid():
            user = register_form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            logout(request)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'register/register_user.html',
                          {'failed_signup': True, 'register_form': register_form, 'account_form': account_form})
    else:
        register_form = RegisterForm()
        account_form = AccountForm()
    return render(request, 'register/register_user.html',
                  {'register_form': register_form, 'account_form': account_form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                logout(request)
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'register/login_user.html', {'failed_login': True, 'login_user': form})
    else:
        form = AuthenticationForm()
    return render(request, 'register/login_user.html', {'login_user': form})


@login_required(login_url='/register/login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')
