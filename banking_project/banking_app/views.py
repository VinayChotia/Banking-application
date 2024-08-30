from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from .serializers import *
from django.contrib.auth import login,logout
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken,Token
from django.views.decorators.debug import sensitive_variables


class CreateUser(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    # queryset = User.objects.all()
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)



class CreateAccount(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    

    def perform_create(self, serializer):
        user = self.request.user
        print('*********')
        serializer.save(
            user=user,
            account_holder_name=user.username
        )




class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)
            amount = request.data.get('amount')
            if amount is None or float(amount) <= 0:
                return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
            account.deposit(float(amount))
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)
            amount = request.data.get('amount')
            if amount is None or float(amount) <= 0:
                return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
            account.withdraw(float(amount))
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            print(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TransferViewone(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        
        source_account_number = serializer.validated_data['source_account']
        target_account_number = serializer.validated_data['target_account']
        amount = serializer.validated_data['amount']

        
        source_account = get_object_or_404(Account, account_number=source_account_number)
        target_account = get_object_or_404(Account, account_number=target_account_number)
        try:
            new_balance = source_account.transfer(amount, target_account)
            return Response({
                "detail": "Transfer successful.",
                "new_balance": str(new_balance)
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TransferViewTwo(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        source_account_number = serializer.validated_data['source_account']
        target_account_number = serializer.validated_data['target_account']
        amount = serializer.validated_data['amount']
        
        source_account = get_object_or_404(Account, account_number=source_account_number, user=request.user)
        target_account = get_object_or_404(Account, account_number=target_account_number)
        
        try:
            new_balance = source_account.transfer(amount, target_account)
            return Response({
                "detail": "Transfer successful.",
                "new_balance": str(new_balance)
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TransferView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        source_account_number = serializer.validated_data['source_account']
        target_account_number = serializer.validated_data['target_account']
        amount = serializer.validated_data['amount']
        # current_user = request.user
        
        source_account = get_object_or_404(Account, account_number=source_account_number,user = request.user)
        target_account = get_object_or_404(Account, account_number=target_account_number)
        if source_account.bank_name==target_account.bank_name:
            try:
                
                new_balance = source_account.transfer(amount, target_account)

                
                recent_transactions = Transaction.objects.filter(account=source_account).order_by('-timestamp')[:5]
                transactions_data = [
                    {
                        "transaction_id": transaction.transaction_id,
                        "transaction_type": transaction.transaction_type,
                        "amount": str(transaction.amount),
                        "timestamp": transaction.timestamp.strftime('%Y-%m-%d %H:%M'),
                        "balance_after": str(transaction.balance_after),
                        "target_account": transaction.target_account.account_number if transaction.target_account else None
                    }
                    for transaction in recent_transactions
                ]

                return Response({
                    "detail": "Transfer successful.",
                    "new_balance": str(new_balance),
                    "recent_transactions": transactions_data
                }, status=status.HTTP_200_OK)
            except ValueError as e:
                Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            
            return Response({"detail":str("Different Banks!! Unable to transfer")},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

        
class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

class TransactionHistoryView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)
            transactions = account.transactions.all()[:10]
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        


# class LoginViewToken(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         login(request, user)
#         if user:
            # token,created = Token.objects.get_or_create(user=user)
        # return Response({'token':token.key}, status=status.HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        print('vinay')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_200_OK)


def logout_view(request):
    logout(request)

#chatgpt method

#to use the sensitive_variables decorator we have to change apiview to ViewSet
class PDFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        try:
            account = Account.objects.get(user = request.user)
            name = account.account_holder_name
        except Account.DoesNotExist:
            return HttpResponse("Account not found", status=404)

        transactions = account.transactions.all().order_by('-timestamp')[:10]
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="transaction_report_{account.account_number}.pdf"'

        # Create the PDF object
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Add a title
        p.setFont("Helvetica-Bold", 14)
        p.drawString(250, height - 40, "Transaction Report")
        p.setFont("Helvetica",12)
        p.drawString(50, height - 60, f"Account Holder: {account.user}")
        p.drawString(50, height - 80, f"Account Number: {account.account_number}")
        p.drawString(50, height - 100, f"Account Type: {account.get_account_type_display()}")
        p.drawString(50, height - 120, f"Account Balance: {account.balance}")

        # Table headers
        p.drawString(50, height - 160, "Date")
        p.drawString(200, height - 160, "Type")
        p.drawString(300, height - 160, "Amount")
        p.drawString(400, height - 160, "Balance After")

        # Add transactions to the PDF
        y = height - 180
        for transaction in transactions:
            p.drawString(50, y, transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            p.drawString(200, y, transaction.get_transaction_type_display())
            p.drawString(300, y, f"{transaction.amount}")
            p.drawString(400, y, f"{transaction.balance_after}")
            y -= 20

        # Close the PDF object
        p.showPage()
        p.save()

        return response
    
class KycUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KycUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

