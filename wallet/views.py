from rest_framework.views import APIView
from rest_framework.response import Response
from wallet.serializers import WalletSerializer
from rest_framework import status
from wallet.models import Wallet as walletModel
from wallet.models import Transaction as TransactionModel
from users.models import User
from django.http import JsonResponse



class WalletView(APIView):
    def get(self, request):
        userId=request.user.id
        wallets=walletModel.objects.filter(user_id=userId,deleted_at=None).values_list('wallet_address', flat=True)
        wallets_id=walletModel.objects.filter(user_id=userId,deleted_at=None).values_list('id', flat=True)
        transactions=TransactionModel.objects.filter(wallet_id__in=wallets_id)
        gem=User.objects.filter(id=userId).values_list('total_gemyto', flat=True)

        return JsonResponse({
            'gem': list(gem),
            'wallets': list(wallets),
            'transactions': list(transactions.values())
        })

    def post(self,request):
        ser_data = WalletSerializer(data=request.POST)
        user_id=request.user.id
        num_of_wallets=walletModel.objects.filter(user_id=user_id,deleted_at=null)
        if len(num_of_wallets)<=3:
            if ser_data.is_valid():
                ser_data.validated_data['user_id']=user_id
                ser_data.create(ser_data.validated_data,user_id)
                return Response(ser_data.validated_data['wallet_address'], status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValueError("you  can have 3 wallets or less")

    def delete(self,request):
        ser_data = WalletSerializer(data=request.POST)
        user_id=request.user.id
        if ser_data.is_valid():
            ser_data.validated_data['user_id']=user_id
            ser_data.delete(ser_data.validated_data)
            return Response('sucssussfully deleted', status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionView(APIView):
    def post(self,request):
        pass
    

    def put(self,request):
        pass

    def delete(self,request):
        pass
