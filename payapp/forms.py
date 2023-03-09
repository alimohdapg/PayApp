from django import forms
from django.contrib.auth.models import User

from payapp.models import Account, Transaction


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['currency']


class PaymentForm(forms.ModelForm):
    recipient_email = forms.EmailField(label='To Email')

    def clean_recipient_email(self):
        recipient_email = self.cleaned_data['recipient_email']
        if User.objects.filter(email=recipient_email).exists():
            return recipient_email
        else:
            raise forms.ValidationError("Email is not associated with a registered user.")

    class Meta:
        model = Transaction
        fields = ['amount']
