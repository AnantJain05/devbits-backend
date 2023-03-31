from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=100)
    # email = serializers.CharField(max_length=100)
    # password = serializers.CharField(max_length=100)
    # curamount = serializers.IntegerField()
    # gain = serializers.IntegerField()
    # loss = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'curamount', 'gain', 'loss', 'total_earnings', 'acc_date', 'watchlist')

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'full_name', 'code_name', 'image')

class UsersStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersStock
        fields = ('user', 'id1', 'symbol', 'stock_name', 'quantity', 'avg_price')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('user', 'id1', 'symbol', 'stock_name', 'operation', 'price', 'quantity', 'date')

    # def create_user(self, validate_data):
    #     return User.objects.create(**validate_data)