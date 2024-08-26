from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'user_type', 'kyc_status',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            user_type=validated_data.get('user_type'),
            kyc_status=validated_data.get('kyc_status', False),
            # account_number = validated_data.get('account_number')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_number', 'account_active_status', 'account_type', 'account_kyc', 'balance','bank_name']
        read_only_fields = ['user'] 
      

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'account', 'transaction_type', 'amount', 'timestamp', 'balance_after', 'target_account',]

class TransferSerializer(serializers.Serializer):
    source_account = serializers.CharField(max_length=12)
    target_account = serializers.CharField(max_length=12)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    # bank_name = serializers.CharField(max_length = 100)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

class LoginSerializerToken(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is inactive.")
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Both fields are required.")

        data["user"] = user
        return data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")

class DepositSerializer(serializers.ModelSerializer):
    model = Transaction
    fields = ['deposit']

class KycUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['kyc_status']

    def update(self, instance, validated_data):
        kyc_status = validated_data.get('kyc_status', instance.kyc_status)
        instance.kyc_status = kyc_status
        instance.save()

        accounts = Account.objects.filter(user=instance)
        accounts.update(account_kyc=kyc_status)

        return instance




