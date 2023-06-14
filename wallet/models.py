from django.db import models
from users.models import User


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallet')
    wallet_address = models.CharField(max_length=35)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'wallet'


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_wallet')
    type = models.CharField(max_length=50)
    value = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'transaction'
