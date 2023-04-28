from django.db import models
from django.contrib.auth.models import User
import requests as req
import os
import environ

env = environ.Env()
environ.Env.read_env()

currencies = (('GBP', 'GBP'), ('USD', 'USD'), ('EUR', 'EUR'))


class Account(models.Model):
    balance = models.FloatField()
    currency = models.CharField(max_length=3, choices=currencies)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # initial balance is in GBP
        if self.balance is None:
            initial_balance = 1000
            self.balance = req.get(
                f'{os.environ.get("SERVER_URL", default=env("SERVER_URL"))}/payapp/convert-currency/'
                f'GBP/{self.currency}/{initial_balance}').json()['amount']
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
