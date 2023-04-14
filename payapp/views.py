from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView
from payapp.forms import PaymentForm
from payapp.models import Account, Transaction
import requests as req
import os
import environ

env = environ.Env()
environ.Env.read_env()


# noinspection PyMethodMayBeStatic
class ConvertCurrency(APIView):

    def get(self, request):
        currency1 = request.query_params.get('currency1')
        currency2 = request.query_params.get('currency2')
        amount = float(request.query_params.get('amount'))
        if currency1 == currency2:
            return Response({'amount': amount})
        if currency1 == 'GBP' and currency2 == 'USD':
            return Response({'amount': amount * 1.18})
        if currency1 == 'GBP' and currency2 == 'EUR':
            return Response({'amount': amount * 1.12})
        if currency1 == 'USD' and currency2 == 'GBP':
            return Response({'amount': amount * 0.85})
        if currency1 == 'USD' and currency2 == 'EUR':
            return Response({'amount': amount * 0.95})
        if currency1 == 'EUR' and currency2 == 'GBP':
            return Response({'amount': amount * 0.89})
        if currency1 == 'EUR' and currency2 == 'USD':
            return Response({'amount': amount * 1.05})


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request, 'payapp/home.html')
        account = Account.objects.get(user=request.user)
        if account.currency == 'USD':
            currency_sign = '$'
        elif account.currency == 'EUR':
            currency_sign = '€'
        else:
            currency_sign = '£'
        return render(request, 'payapp/home.html', {'balance': f'{currency_sign}{"{:.2f}".format(account.balance)}'})
    return render(request, 'payapp/home.html')


@user_passes_test(lambda u: not u.is_staff, login_url=reverse_lazy('logout_user'))
@transaction.atomic
@login_required(login_url='/register/login_user')
def send_payment(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            new_transaction = payment_form.save(commit=False)
            sender = request.user.account
            if sender.balance < new_transaction.amount:
                payment_form.add_error('amount', 'Insufficient balance')
                return render(request, 'payapp/send_payment.html', {'payment_form': payment_form})
            receiver_user = User.objects.get(email__exact=payment_form.cleaned_data['recipient_email'])
            if receiver_user.is_staff:
                payment_form.add_error('email', 'Invalid email address')
                return render(request, 'payapp/send_payment.html', {'payment_form': payment_form})
            receiver = receiver_user.account
            sender.balance -= new_transaction.amount
            params = {'currency1': sender.currency, 'currency2': receiver.currency, 'amount': new_transaction.amount}
            receiver.balance -= \
                req.get(f'{os.environ.get("SERVER_URL", default=env("SERVER_URL"))}/payapp/convert-currency',
                        params=params).json()['amount']
            sender.save()
            receiver.save()
            new_transaction.sender = sender
            new_transaction.receiver = receiver
            new_transaction.save()
            return render(request, 'payapp/send_payment.html',
                          {'payment_sent': True, 'payment_form': payment_form})
        else:
            return render(request, 'payapp/send_payment.html', {'payment_form': payment_form})
    else:
        payment_form = PaymentForm()
    return render(request, 'payapp/send_payment.html', {'payment_form': payment_form})


@user_passes_test(lambda u: not u.is_staff, login_url=reverse_lazy('logout_user'))
@transaction.atomic
@login_required(login_url='/register/login_user')
def request_payment(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            new_transaction = payment_form.save(commit=False)
            new_transaction.request = True
            new_transaction.sender = request.user.account
            receiver_user = User.objects.get(email__exact=payment_form.cleaned_data['recipient_email'])
            if receiver_user.is_staff:
                payment_form.add_error('email', 'Invalid email address')
                return render(request, 'payapp/request_payment.html', {'payment_form': payment_form})
            new_transaction.receiver = receiver_user.account
            new_transaction.save()
            return render(request, 'payapp/request_payment.html',
                          {'request_sent': True, 'payment_form': payment_form})
        else:
            return render(request, 'payapp/request_payment.html', {'payment_form': payment_form})
    else:
        payment_form = PaymentForm()
    return render(request, 'payapp/request_payment.html', {'payment_form': payment_form})


@user_passes_test(lambda u: not u.is_staff, login_url=reverse_lazy('logout_user'))
@login_required(login_url='/register/login_user')
def requests(request):
    sent_requests = list(Transaction.objects.filter(sender=request.user.account, request=True).order_by('-modified'))
    received_requests = list(
        Transaction.objects.filter(receiver=request.user.account, request=True).order_by('-modified'))
    return render(request, 'payapp/requests.html',
                  {'sent_requests': sent_requests, 'received_requests': received_requests,
                   'insufficient_balance_id': request.session.get('insufficient_balance_id', -1)})


@user_passes_test(lambda u: not u.is_staff, login_url=reverse_lazy('logout_user'))
@transaction.atomic
@login_required(login_url='/register/login_user')
def delete_request(request):
    new_transaction = Transaction.objects.get(pk=request.GET["request_id"])
    new_transaction.request = False
    new_transaction.save()
    return redirect('requests')


@user_passes_test(lambda u: not u.is_staff, login_url=reverse_lazy('logout_user'))
@transaction.atomic
@login_required(login_url='/register/login_user')
def accept_request(request):
    request_id = request.GET["request_id"]
    new_transaction = Transaction.objects.get(pk=request_id)
    params = {'currency1': new_transaction.sender.currency, 'currency2': new_transaction.receiver.currency,
              'amount': new_transaction.amount}
    converted_amount = \
        req.get(f'{os.environ.get("SERVER_URL", default=env("SERVER_URL"))}/payapp/convert-currency',
                params=params).json()['amount']
    if new_transaction.receiver.balance < converted_amount:
        request.session['insufficient_balance_id'] = request_id
        return redirect('requests')
    new_transaction.receiver.balance -= converted_amount
    new_transaction.sender.balance += new_transaction.amount
    new_transaction.request = False
    new_transaction.sender.save()
    new_transaction.receiver.save()
    new_transaction.save()
    return redirect('requests')


@user_passes_test(lambda u: not u.is_staff, login_url=reverse_lazy('logout_user'))
@login_required(login_url='/register/login_user')
def history(request):
    transaction_history = list(
        Transaction.objects.filter(
            (Q(sender=request.user.account) | Q(receiver=request.user.account)) & Q(request=False)
        ).order_by('-modified'))
    return render(request, 'payapp/history.html', {'transaction_history': transaction_history})


@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('logout_user'))
@login_required(login_url='/register/login_user')
def accounts(request):
    users = list(User.objects.all())
    return render(request, 'payapp/accounts.html', {'users': users})


@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('logout_user'))
@login_required(login_url='/register/login_user')
def transactions(request):
    transaction_history = list(Transaction.objects.filter(request=False).order_by('-modified'))
    return render(request, 'payapp/transactions.html', {'transaction_history': transaction_history})
