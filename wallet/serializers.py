from wallet.models import Wallet, Transaction
from game.models import DailyPlayedGame
from rest_framework import serializers


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('wallet_address',)

    def create(self, validated_data):
        return Wallet.objects.create(**validated_data, )


class TransactionGetSerializer(serializers.ModelSerializer):
    wallet_address = serializers.CharField(source='to_wallet.wallet_address')

    class Meta:
        model = Transaction
        fields = ('wallet_address', 'from_wallet', 'value', 'created_at',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('to_wallet_id', 'from_wallet', 'value', 'created_at',)

        def create(self, validated_data):
            return Transaction.objects.create(**validated_data)


class WalletGamesSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(source='game.name')
    cover_image = serializers.CharField(source='game.cover_image')

    class Meta:
        model = DailyPlayedGame
        fields = ('id', 'game_gemyto', 'cover_image', 'game_name')
