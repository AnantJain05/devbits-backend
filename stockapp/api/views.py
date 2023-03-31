from django.shortcuts import render
import io
from users.models import *
from users.serializers import *
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io, json
from datetime import datetime

# Create your views here.
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request):
    if request.method == "GET":
        # json_data = request.body
        # stream = io.BytesIO(json_data)
        # python_data = JSONParser().parse(stream)
        id = request.data.get('id')
        if id is not None:
            user = User.objects.get(id = id)
            serializer = UserSerializer(user)
            # json_data = JSONRenderer().render(serializer.data)
            return Response(serializer.data)
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request, format=None):
    print(request.user)
    serializer = UserSerializer(request.user)
    print(serializer)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        # json_data = request.body
        # stream = io.BytesIO(json_data)
        # python_data = JSONParser().parse(stream)
        now = datetime.now()
        data = request.data
        data["acc_date"]=now
        print(data)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'})
        return Response(serializer.errors)
            # res = {'msg': 'Data Created'}
            # json_data = JSONRenderer().render(res)
            # return HttpResponse(json_data, content_type="application/json")
        # json_data = JSONRenderer().render(serializer.errors)
        # return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
@api_view(['POST'])
def add_stock(request):
     if request.method == 'POST':
          serializer = StockSerializer(data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response({'msg':'Stock Added'})
          return Response(serializer.errors)

@api_view(['GET'])
def get_stock(request, id):
    if request.method == "GET":
        # id = request.data.get('id')
        # print(request.GET)
        print(id)
        print(request.data)
        stock = Stock.objects.get(id=id)
        # print("hihi", stock)
        serializer = StockSerializer(stock)
        return Response(serializer.data)
        # serializer = StockSerializer(data = stock)
        # return Response(serializer.data)
        
     
@csrf_exempt
@api_view(['POST'])
def buy_stock(request):
    if request.method == 'POST':
        user = request.user
        id = request.data.get('id')
        symbol = request.data.get('symbol')
        stockname = request.data.get('stockname')
        quantity = request.data.get('quantity')
        quantity = float(quantity)
        price = request.data.get('price')
        now = datetime.now()
        invested = price*quantity
        if user.curamount>=invested:
            user.curamount -= invested
            user.save()
            users_stock_list = UsersStock.objects.filter(stock_name = stockname, user = user)
            if len(users_stock_list)==0 :
                usersStock = UsersStock(user=user, id1=id, symbol=symbol, stock_name=stockname, quantity=quantity, avg_price=price)
                usersStock.save()
            else:
                usersStock = users_stock_list[0]
                newquant = usersStock.quantity + quantity
                usersStock.avg_price = (usersStock.avg_price*usersStock.quantity + invested)/newquant
                usersStock.quantity += quantity
                # usersStock.invested += invested
                usersStock.save()
            transaction = Transaction(user=user, id1=id, symbol=symbol, stock_name=stockname, operation=0, price=price, quantity=quantity, date=now)
            transaction.save()
            return Response({'msg': "Stocks Bought"})
        else:
            return Response({'msg': "Insufficient Balance"})

@csrf_exempt
@api_view(['POST'])
def sell_stock(request):
    if request.method == 'POST':
        user = request.user
        id = request.data.get('id')
        symbol = request.data.get('symbol')
        stockname = request.data.get('stockname')
        quantity = request.data.get('quantity')
        quantity = float(quantity)
        price = request.data.get('price')
        now=datetime.now()
        users_stock_list = UsersStock.objects.filter(stock_name = stockname, user = user)
        if len(users_stock_list)!=0:
            usersStock = users_stock_list[0]
            if usersStock.quantity >= quantity:
                user.curamount += quantity*price
                if usersStock.avg_price > price:
                    user.loss += quantity*(usersStock.avg_price-price)
                else:
                    user.gain += quantity*(price-usersStock.avg_price)
                
                user.total_earnings = user.gain-user.loss
                user.save()
                usersStock.quantity -= quantity
                if usersStock.quantity==0:
                    usersStock.delete()
                else :
                    usersStock.save()
                transaction = Transaction(user=user, id1=id, symbol=symbol, stock_name=stockname, operation=1, price=price, quantity=quantity, date=now)
                transaction.save()
                return Response({'msg': 'Stocks Sold'})
            else:
                return Response({'msg': "ERROR!! You don't have enough stocks to sell"})
        else:
            return Response({'msg': 'Invalid Request'}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
def get_users_stock(request):
    if request.method == "GET":
        user = request.user
        stock_list = UsersStock.objects.filter(user = user)
        serializer = UsersStockSerializer(stock_list, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def get_users_transaction(request):
    if request.method == "GET":
        user = request.user
        transaction_list = Transaction.objects.filter(user = user)
        transaction_list = transaction_list.order_by('-date').values()
        # transaction_list = transaction_list.sort(key=lambda data:  datetime.strptime(data.date, "%m-%Y"))
        print(transaction_list)
        serializer = TransactionSerializer(transaction_list, many=True)
        return Response(transaction_list)
    
@csrf_exempt
@api_view(['POST'])
def add_in_watchlist(request):
    if request.method == "POST":
        user = request.user
        # watchlist = user.watchlist
        code = request.data.get("code")
        stock = Stock.objects.get(code_name=code)
        user.watchlist.add(stock)
        user.save()
        return Response({'msg': 'Stock added in watchlist'})
    
@csrf_exempt
@api_view(['POST'])
def remove_from_watchlist(request):
    if request.method == "POST":
        user = request.user
        # watchlist = user.watchlist
        code = request.data.get("code")
        stock = Stock.objects.get(code_name=code)
        user.watchlist.remove(stock)
        user.save()
        return Response({'msg': 'Stock removed from watchlist'})
    
@api_view(['GET'])
def get_watchlist(request):
    if request.method=="GET":
        user=request.user
        watchlist = user.watchlist
        lst = []
        for stock in watchlist.all():
            serializer = StockSerializer(stock)
            lst.append(serializer.data)
        return Response(lst)
