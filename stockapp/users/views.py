from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import *
from .utils import google_get_access_token, google_get_user_info
from urllib import parse
import requests
import html, json
from datetime import datetime
from django.http import HttpResponseRedirect

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class GoogleCallbackHandler(APIView):
    def post(self, request):
        # HttpResponseRedirect(redirect_to='http://localhost:3000.com')
        # x = requests.get(googleAuthUrl, headers=headers)
        # print(html.unescape(x.text))
        # print(request.query_params['code'])
        print(request.data.get("data"))
        auth_code = request.data.get("data").get("auth_code", None)
        print(auth_code)
        

        if(auth_code):
            print("hi1")
            access_token = google_get_access_token(auth_code)
            print("hi2")
            userdata = google_get_user_info(access_token)

            data = {
                'auth_code': auth_code,
                'access_token': access_token
            }

            user_email = userdata['email']
            user_name = userdata['name']
            print(user_email)
           
            # now check if this user exists. if exists, use simplejwt to return an access and refresh token for his account
            # if user does not exist, create a user with that email, and take him to profile completion page
            try:
                is_user= User.objects.get(email=user_email)

            #     # create tokens and send
            except:
                # KYProfile.objects.create(email=user_email,full_name=user_name)
                # is_user= KYProfile.objects.get(email=user_email)
                # is_user.set_password('new_password')
                # is_user.save()
                return Response({"msg": "User does not exist! Create an account first!", "data": userdata})

            print(is_user)
            dct=get_tokens_for_user(is_user)
            print(dct)
            userdata['refresh']=dct['refresh']
            userdata['access']=dct['access']
            print("sending response", dct)
            return Response(dct)
        else:
            print("Shri error here!!")
            return Response({'msg':'no code'}, status=status.HTTP_400_BAD_REQUEST)
        

class EmailRegistration(APIView):  # registration with email
    permission_classes = [AllowAny]
    def post(self ,request):
        # print("POST\n", request.data)
        email = request.data.get('email', None)
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        #print(password)
        now = datetime.now()
        check_email = User.objects.filter(email=email)
        if not len(check_email):
                user = User.objects.create(email=email,
                                           username=username,
                                           is_active=False,
                                           curamount=1000000,
                                           gain=0,
                                           loss=0,
                                           acc_date=now)
                # print("HERE")
                # if not settings.PROD:
                #     kyprofile.is_active = True
                user.set_password(password)
                user.is_active=True
                user.save()
                
                return Response({'msg':"Thank You for registering. You can now login to your account!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': "Email already in use"}, status=status.HTTP_226_IM_USED)
