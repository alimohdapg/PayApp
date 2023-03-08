from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    currency = (('GBP', 'GBP'), ('USD', 'USD'), ('EUR', 'EUR'))

    balance = models.FloatField()
    currency = models.CharField(max_length=3, choices=currency)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # initial balance is in GBP
        initial_balance = 1000
        if self.balance is None:
            if self.currency == 'USD':
                self.balance = initial_balance * 1.18
            elif self.currency == 'EUR':
                self.balance = initial_balance * 1.12
            else:
                self.balance = initial_balance
        super(Account, self).save(*args, **kwargs)
