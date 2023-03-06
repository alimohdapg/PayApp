from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegisterForm


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password1'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'])
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'register/register_user.html', {'failed_signup': True, 'register_user': form})
    else:
        form = RegisterForm()
    return render(request, 'register/register_user.html', {'register_user': form})


def login_user(request):
    return None


def logout_user(request):
    return None
