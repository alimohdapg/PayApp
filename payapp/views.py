from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import render, redirect
from payapp.forms import PaymentForm
from payapp.models import Account, convert_currency, Transaction


def home(request):
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        if account.currency == 'USD':
            currency_sign = '$'
        elif account.currency == 'EUR':
            currency_sign = '€'
        else:
            currency_sign = '£'
        return render(request, 'payapp/home.html', {'balance': f'{currency_sign}{account.balance}'})
    return render(request, 'payapp/home.html')


@login_required(login_url='/register/login_user')
def send_payment(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            transaction = payment_form.save(commit=False)
            sender = request.user.account
            if sender.balance < transaction.amount:
                PaymentForm.add_error('amount', 'Insufficient balance')
                return render(request, 'payapp/send_payment.html', {'payment_form': payment_form})
            receiver = User.objects.get(email__exact=payment_form.cleaned_data['recipient_email']).account
            sender.balance -= transaction.amount
            receiver.balance += convert_currency(sender.currency, receiver.currency, transaction.amount)
            sender.save()
            receiver.save()
            transaction.sender = sender
            transaction.receiver = receiver
            transaction.save()
            return render(request, 'payapp/send_payment.html',
                          {'payment_sent': True, 'payment_form': payment_form})
        else:
            return render(request, 'payapp/send_payment.html', {'payment_form': payment_form})
    else:
        payment_form = PaymentForm()
    return render(request, 'payapp/send_payment.html', {'payment_form': payment_form})


@login_required(login_url='/register/login_user')
def request_payment(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            transaction = payment_form.save(commit=False)
            transaction.request = True
            transaction.sender = request.user.account
            transaction.receiver = User.objects.get(email__exact=payment_form.cleaned_data['recipient_email']).account
            transaction.save()
            return render(request, 'payapp/request_payment.html',
                          {'request_sent': True, 'payment_form': payment_form})
        else:
            return render(request, 'payapp/request_payment.html', {'payment_form': payment_form})
    else:
        payment_form = PaymentForm()
    return render(request, 'payapp/request_payment.html', {'payment_form': payment_form})


@login_required(login_url='/register/login_user')
def requests(request):
    sent_requests = list(Transaction.objects.filter(sender=request.user.account, request=True))
    received_requests = list(Transaction.objects.filter(receiver=request.user.account, request=True))
    return render(request, 'payapp/requests.html',
                  {'sent_requests': sent_requests, 'received_requests': received_requests,
                   'insufficient_balance_id': int(request.session['insufficient_balance_id']) if
                   request.session['insufficient_balance_id'] is not None else None})


def delete_request(request):
    transaction = Transaction.objects.get(pk=request.GET["request_id"])
    transaction.request = False
    transaction.save()
    return redirect('requests')


def accept_request(request):
    request_id = request.GET["request_id"]
    transaction = Transaction.objects.get(pk=request_id)
    converted_amount = convert_currency(transaction.sender.currency, transaction.receiver.currency, transaction.amount)
    if transaction.receiver.balance < converted_amount:
        request.session['insufficient_balance_id'] = request_id
        return redirect('requests')
    transaction.receiver.balance -= converted_amount
    transaction.sender.balance += transaction.amount
    transaction.request = False
    transaction.sender.save()
    transaction.receiver.save()
    transaction.save()
    return redirect('requests')


@login_required(login_url='/register/login_user')
def history(request):
    return None


@login_required(login_url='/register/login_user')
def accounts(request):
    return None


@login_required(login_url='/register/login_user')
def transactions(request):
    return None
