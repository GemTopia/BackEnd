from wallet.serializers import TransactionSerializer, TransactionGetSerializer
from wallet.serializers import WalletSerializer,WalletGamesSerializer
from game.serializers import GameSerializer, DailyPlayedGameSerializer
from wallet.models import Transaction as TransactionModel
from users.serializers import UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated
from wallet.models import Wallet as walletModel
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.models import User


class WalletAndTransactionView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = {
        'wallet': WalletSerializer,
        'played': GameSerializer,
        'daily_played': DailyPlayedGameSerializer,
        'gemyto': UserRegisterSerializer,
        'transactions': TransactionGetSerializer,
    }

    def get(self, request):
        userId = request.user.id
        user = User.objects.get(id=userId)

        daily_played_games = user.user_daily_games.all()
        daily_games = [daily_played_game for daily_played_game in daily_played_games]
        serialized_daily_game = WalletGamesSerializer(instance=daily_games, many=True)

        played_games = user.user_games.all()
        games = [played_game for played_game in played_games]
        serialized_games = WalletGamesSerializer(instance=games, many=True)

        wallets_id = walletModel.objects.filter(user_id=userId)
        transactions = TransactionModel.objects.filter(to_wallet_id__in=wallets_id)
        serialized_transactions = TransactionGetSerializer(instance=transactions, many=True)

        serialized_gem = UserRegisterSerializer(instance=user, many=False)

        serialized_data = {
            'daily_played': serialized_daily_game.data,
            'played': serialized_games.data,
            'transactions': serialized_transactions.data,
            'gemyto': serialized_gem.data['gemyto']
        }
        return Response(serialized_data)

    def post(self, request):
        permission_classes = [IsAuthenticated]
        user_id = request.user.id
        before_gemyto = request.user.gemyto
        wallet_dict = {"wallet_address": request.data['to_wallet'], }
        wallet_ser_data = WalletSerializer(data=wallet_dict)

        if float(request.data['value']) > 0:
            if float(request.data['value']) <= before_gemyto:
                if wallet_ser_data.is_valid():
                    if not walletModel.objects.filter(user_id=user_id, wallet_address=wallet_ser_data.validated_data[
                        "wallet_address"]).exists():
                        wallet_ser_data.validated_data['user_id'] = user_id
                        wallet_ser_data.create(wallet_ser_data.validated_data)
                    wallet_id = walletModel.objects.get(user=user_id, wallet_address=request.data['to_wallet']).id
                    transaction_ser_data = TransactionSerializer(data=request.data)
                    if transaction_ser_data.is_valid():
                        transaction_ser_data.validated_data['to_wallet_id'] = wallet_id
                        transaction_ser_data.create(transaction_ser_data.validated_data)
                        user = request.user
                        subt: float = before_gemyto - float(request.data['value'])
                        llll = {"gemyto": round(subt, 11)}
                        ser_data = UserRegisterSerializer(instance=user, data=llll, partial=True)
                        if ser_data.is_valid():
                            ser_data.save()
                            return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
                        else:

                            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
                        return Response({"status": "ok"}, status=status.HTTP_200_OK)
                    else:
                        return Response(transaction_ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(wallet_ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
            else:

                return Response({"error": "you don't have enough gemyto"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "the amount of gemyto should positive"}, status=status.HTTP_400_BAD_REQUEST)
