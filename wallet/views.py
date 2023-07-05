from rest_framework.views import APIView
from rest_framework.response import Response
from wallet.serializers import WalletSerializer
from rest_framework import status
from wallet.models import Wallet as walletModel
from wallet.models import Transaction as TransactionModel
from users.models import User
from wallet.serializers import WalletSerializer
from wallet.serializers import TransactionSerializer
from users.serializers import UserRegisterSerializer
#from web3 import Web3
#from wallet import token_info



class WalletView(APIView):


    def get(self, request):
        userId=request.user.id
        wallets=walletModel.objects.filter(user_id=userId,deleted_at=None)
        wallets_id=walletModel.objects.filter(user_id=userId,deleted_at=None)
        transactions=TransactionModel.objects.filter(wallet_id__in=wallets_id)
        user=User.objects.get(id=userId)
        serialized_wallets=WalletSerializer(instance=wallets,many=True)
        serialized_transactions=TransactionSerializer(instance=transactions,many=True)
        serialized_gem=UserRegisterSerializer(instance=user,many=False)
        serialized_data={
            'wallets':serialized_wallets.data,
            'transactions':serialized_transactions.data,
            'gem':serialized_gem.data['total_gemyto']
        }

        return Response(serialized_data)

    def post(self,request):
        ser_data = WalletSerializer(data=request.POST)
        userId=request.user.id
        num_of_wallets=walletModel.objects.filter(user_id=userId,deleted_at=None)
        if len(num_of_wallets)<3:
            if ser_data.is_valid():
                ser_data.validated_data['user_id']=userId
                ser_data.create(ser_data.validated_data)
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

""" class TransactionView(APIView):
    def post(self,request):
        ser_data = WalletSerializer(data=request.POST)
        user_id=request.user.id
        if ser_data.is_valid():
                ser_data.validated_data['user_id']=user_id
                ser_data.validated_data['tyoe']='get'
                if(Web3.is_checksum_address(ser_data.validated_data['wallet_address'])):
                    w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/YOUR-PROJECT-ID'))
                    erc20 = w3.eth.contract(address=ser_data.validated_data['wallet_address'], abi=token_info.ABI)
                    account = Account.privateKeyToAccount(token_info.PRIVATE_KET)
                    nonce = w3.eth.getTransactionCount(account.address)
                    erc20.functions.signTransaction
                    tx = erc20.functions.transfer(to_address, ser_data.validated_data['value']).buildTransaction({
                    'from': account.address,
                    'gas': 100000,
                    'gasPrice': w3.toWei('1', 'gwei'),
                    'nonce': nonce,})
                    signed_tx = account.signTransaction(tx)
                    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
                    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                    if receipt.status == 0x1:
                        ser_data.objects.create(ser_data.validated_data)
                    else:
                        raise ValueError('transaction failed')

                else:
                    raise ValueError('your wallet address is not valid')
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)  """
""" tx_hash = w3.eth.send_transaction({
    "from": acct2.address,
    "value": 3333333333,
    "to": some_address
}) """