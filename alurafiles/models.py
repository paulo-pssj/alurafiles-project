from django.contrib.auth.models import User
from django.db import models


class Transactions(models.Model):
    origin_bank = models.CharField(max_length=100, blank=False, null=False)
    origin_agency = models.CharField(max_length=100, blank=False, null=False)
    origin_account = models.CharField(max_length=100, blank=False, null=False)
    destiny_bank = models.CharField(max_length=100, blank=False, null=False)
    destiny_agency = models.CharField(max_length=100, blank=False, null=False)
    destiny_account = models.CharField(max_length=100, blank=False, null=False)
    value_transaction = models.BigIntegerField(blank=False, null=False)
    transaction_date = models.DateField(
        max_length=255, blank=False, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Dates(models.Model):
    transaction_date = models.DateField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
