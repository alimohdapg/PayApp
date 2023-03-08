from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'payapp/home.html')


@login_required(login_url='/register/login_user')
def send_payment(request):
    return None


@login_required(login_url='/register/login_user')
def request_payment(request):
    return None


@login_required(login_url='/register/login_user')
def requests(request):
    return None


@login_required(login_url='/register/login_user')
def history(request):
    return None


@login_required(login_url='/register/login_user')
def accounts(request):
    return None


@login_required(login_url='/register/login_user')
def transactions(request):
    return None
