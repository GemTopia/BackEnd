from django.urls import path
from wallet.views import WalletAndTransactionView

app_name = 'wallet'
urlpatterns = [
    path("", WalletAndTransactionView.as_view(), name="wallet"),

]

