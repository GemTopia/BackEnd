from rest_framework import serializers
from wallet.models import Wallet, Transaction
from django.utils import timezone


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('wallet_address',)

    def create(self, validated_data):
        return Wallet.objects.create(**validated_data, )

    def delete(self, validated_data):
        the_wallet = Wallet.objects.filter(wallet_address=validated_data['wallet_address'],
                                           user_id=validated_data['user_id'], deleted_at=None).first()
        the_wallet.deleted_at = timezone.now()
        the_wallet.save()
        return


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('wallet_id', 'value')

        def create(self, validated_data):
            return Transaction.objects.create(**validated_data)
