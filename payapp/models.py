from django.db import models
from django.contrib.auth.models import User

currencies = (('GBP', 'GBP'), ('USD', 'USD'), ('EUR', 'EUR'))


def convert_currency(currency1, currency2, amount):
    if currency1 == currency2:
        return amount
    if currency1 == 'GBP' and currency2 == 'USD':
        return amount * 1.18
    if currency1 == 'GBP' and currency2 == 'EUR':
        return amount * 1.12
    if currency1 == 'USD' and currency2 == 'GBP':
        return amount * 0.85
    if currency1 == 'USD' and currency2 == 'EUR':
        return amount * 0.95
    if currency1 == 'EUR' and currency2 == 'GBP':
        return amount * 0.89
    if currency1 == 'EUR' and currency2 == 'USD':
        return amount * 1.05


class Account(models.Model):
    balance = models.FloatField()
    currency = models.CharField(max_length=3, choices=currencies)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # initial balance is in GBP
        if self.balance is None:
            initial_balance = 1000
            self.balance = convert_currency('GBP', self.currency, initial_balance)
        super(Account, self).save(*args, **kwargs)


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Transaction(TimeStampedModel):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')
    amount = models.FloatField()
    request = models.BooleanField(default=False)
