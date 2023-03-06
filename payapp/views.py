from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'payapp/home.html')


def send_payment(request):
    return None


def request_payment(request):
    return None


def requests(request):
    return None


def history(request):
    return None


def accounts(request):
    return None


def transactions(request):
    return None
