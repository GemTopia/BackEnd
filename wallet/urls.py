from django.urls import path
from wallet.views import WalletView
#from wallet.views import TransactionView



app_name = 'wallet'
urlpatterns = [
    path("", WalletView.as_view(), name="wallet"),
    #path("transaction/", TransactionView.as_view(), name="transaction"),

]

