from django.db import models
import uuid
from django.db import transaction
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import decimal
import datetime
from datetime import timedelta

class Account(models.Model):
    SAVINGS = 'savings'
    CURRENT = 'current'
    SALARY = 'salary'
    
    ACCOUNT_TYPE_CHOICES = [
        (SAVINGS, 'Savings'), 
        (CURRENT, 'Current'),
        (SALARY, 'Salary'),
    ]
    
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='accounts',null=True,blank=True)
    account_number = models.CharField(max_length=12, unique=True)
    account_holder_name = models.CharField(max_length=255)
    account_active_status = models.BooleanField(default=False)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    account_kyc = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    time_created = models.DateTimeField(auto_now_add=True)
    bank_name = models.CharField(max_length=200,blank=True)
    
    def __str__(self):
        return f"{self.account_holder_name} ({self.account_number})"
    

    @transaction.atomic
    def deposit(self, amount):
        self.balance += decimal.Decimal(amount)
        self.save()
        Transaction.create_transaction(self, Transaction.DEPOSIT, amount)
        return self.balance
    
    def inactive(self,account_active_status,time_created):
        
        if timezone.now-time_created> timedelta(days=1*30):
            account_active_status = False
    @transaction.atomic
    def withdraw(self, amount):
        if not self.account_kyc and amount > 1000:  
            raise ValueError("Cannot Withdraw! Please update Kyc.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= decimal.Decimal(amount)
        self.save()
        Transaction.create_transaction(self, Transaction.WITHDRAWAL, amount)
        return self.balance
    
    @transaction.atomic
    def transfer(self, amount, target_account):
        if not self.account_kyc and amount > 1000:  
            raise ValueError("Cannot transfer! Please Update Kyc.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")

        
        self.balance -= decimal.Decimal(amount)
        self.save()
        Transaction.create_transaction(self, Transaction.TRANSFER, amount, target_account)
        
        target_account.balance += decimal.Decimal(amount)
        target_account.save()
        Transaction.create_transaction(target_account, Transaction.DEPOSIT, amount, self)

        return self.balance


class User(AbstractUser):
    LOCAL = 'local'
    NRI = 'nri'
    
    USER_TYPE_CHOICES = [
        (LOCAL, 'Local'),
        (NRI, 'NRI'),
    ]
    
    user_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    kyc_status = models.BooleanField(default=False)
    account = models.ForeignKey('account',on_delete=models.CASCADE,blank=True,null=True,related_name='accounts')
    

    def __str__(self):
        return self.username
    

class Transaction(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer'),
    ]

    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    target_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='incoming_transfers')

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-timestamp']
    @transaction.atomic
    @staticmethod
    def create_transaction(account, transaction_type, amount, target_account=None):
        balance_after = account.balance
        transaction = Transaction.objects.create(
            account=account,
            transaction_type=transaction_type,
            amount=amount,
            balance_after=balance_after,
            target_account=target_account,
        )
        return transaction



