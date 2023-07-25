from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallet')
    wallet_address = models.CharField(max_length=42)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['created_at']
        db_table = 'wallet'


class Transaction(models.Model):
    to_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_wallet')
    from_wallet=models.CharField(max_length=42)
    value = models.FloatField(validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['created_at']
        db_table = 'transaction'
