from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import UserManager
import datetime

# Create your models here.
class Stock(models.Model):
    full_name = models.CharField(max_length=100)
    code_name = models.CharField(max_length=10)
    image = models.URLField(default='https://storage.forums.net/6479407/images/vagmAzMznjBJGQf_sumV.png')

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    curamount = models.IntegerField(default=0)
    gain = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    total_earnings = models.IntegerField(default=0)
    acc_date = models.DateField(default=datetime.date(2023,1,1))
    # stocks = models.ManyToManyField(UsersStock, blank=True, related_name="stocks")
    watchlist = models.ManyToManyField(Stock, blank=True, related_name="watchlist")
    # transactions = models.ManyToManyField(Transaction, blank=True, related_name="transactions")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

        
class UsersStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id1 = models.CharField(max_length=100, default="")
    symbol = models.CharField(max_length=100, default="")
    stock_name = models.CharField(max_length=100)
    quantity = models.FloatField(default=0)
    avg_price = models.FloatField(default=0)
    # invested = models.IntegerField(default=0)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id1 = models.CharField(max_length=100, default="")
    symbol = models.CharField(max_length=100, default="")
    stock_name = models.CharField(max_length=100)
    operation = models.IntegerField(null=False)
    price = models.FloatField(null=False)
    quantity = models.FloatField(null=False)
    date = models.DateTimeField(null=True)




