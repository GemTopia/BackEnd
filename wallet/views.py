from rest_framework.views import APIView
from rest_framework.response import Response
from wallet.serializers import WalletSerializer
from rest_framework import status
from wallet.models import Wallet as walletModel
from wallet.models import Transaction as TransactionModel
from users.models import User
from wallet.serializers import WalletSerializer
from wallet.serializers import TransactionSerializer,TransactionGetSerializer
from users.serializers import UserRegisterSerializer
from game.models import PlayedGame,DailyPlayedGame
from game.serializers import GameSerializer,DailyPlayedGameSerializer
from rest_framework.permissions import IsAuthenticated



class WalletAndTransactionView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        
        userId=request.user.id


        user=User.objects.get(id=userId)
        gemes=PlayedGame.objects.filter(user_id=userId)
        daily_games=DailyPlayedGame.objects.filter(user_id=userId)
        wallets_id=walletModel.objects.filter(user_id=userId)
        transactions=TransactionModel.objects.filter(to_wallet_id__in=wallets_id)


        serialized_games=DailyPlayedGameSerializer(instance=gemes,many=True)
        serialized_daily_game=DailyPlayedGameSerializer(instance=daily_games,many=True)
        serialized_transactions=TransactionGetSerializer(instance=transactions,many=True)
        serialized_gem=UserRegisterSerializer(instance=user,many=False)

        serialized_data={
            'daily_games':serialized_daily_game.data,
            'games':serialized_games.data,
            'transactions':serialized_transactions.data,
            'gemyto':serialized_gem.data['gemyto']
        }
        return Response(serialized_data)



    def post(self,request):
        permission_classes = [IsAuthenticated]
        user_id=request.user.id
        before_gemyto=request.user.gemyto
        wallet_dict={"wallet_address":request.data['to_wallet'],}
        wallet_ser_data = WalletSerializer(data=wallet_dict)

        if float(request.data['value'])>0:
            if float(request.data['value'])<=before_gemyto:
                if wallet_ser_data.is_valid():
                    if not walletModel.objects.filter(user_id=user_id,wallet_address=wallet_ser_data.validated_data["wallet_address"]).exists():
                        wallet_ser_data.validated_data['user_id']=user_id
                        wallet_ser_data.create(wallet_ser_data.validated_data)
                    wallet_id=walletModel.objects.get(user=user_id,wallet_address=request.data['to_wallet']).id
                    transaction_ser_data=TransactionSerializer(data=request.data)
                    if transaction_ser_data.is_valid():
                        transaction_ser_data.validated_data['to_wallet_id']=wallet_id
                        transaction_ser_data.create(transaction_ser_data.validated_data)
                        user = request.user
                        subt:float=before_gemyto-float(request.data['value'])
                        llll={"gemyto":round(subt, 11)}
                        ser_data = UserRegisterSerializer(instance=user, data=llll, partial=True)
                        if ser_data.is_valid():
                            ser_data.save()
                            return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
                        else:

                            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
                        return Response({"status":"ok"}, status=status.HTTP_200_OK)
                    else:
                        return Response(transaction_ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(wallet_ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
            else:

                return Response({"error":"you don't have enough gemyto"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"the amount of gemyto should positive"}, status=status.HTTP_400_BAD_REQUEST)




