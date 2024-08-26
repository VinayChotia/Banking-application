from django.contrib import admin
from django.urls import path,include
import rest_framework
from .views import *

urlpatterns = [
    path('user/',CreateUser.as_view()),
    path('account/',CreateAccount.as_view()),
    path('deposit/<str:account_number>/', DepositView.as_view(), name='deposit'),
    path('withdraw/<str:account_number>/', WithdrawView.as_view(), name='withdraw'),
    path('transfer/<str:account_number>/', TransferView.as_view(), name='transfer'),
    path('balance/<str:account_number>/', BalanceView.as_view(), name='balance'),
    path('transactions/<str:account_number>/', TransactionHistoryView.as_view(), name='transactions'),
    path('login/',LoginView.as_view(),name = 'Login'),
    path('generate/',PDFView.as_view(),name = 'generate-pdf'),
    path('api-auth/',include('rest_framework.urls')),
    path('kyc-update/<str:account_number>/',KycUpdateView.as_view(),name = 'kyc-update')
]



