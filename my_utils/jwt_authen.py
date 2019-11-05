import datetime
import logging
import time

import jwt
from django.http import JsonResponse
from django.views import View
from requests.api import request
from rest_framework.decorators import permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from my_utils import response_status, cus_exception
from socialapi.settings import JWT_TOKEN_EXPIRATION_DAYS, SECRET_KEY


class JwtAuthen():
    @staticmethod
    def create_jwt(data):
        token = {
            'iat': time.time(),
            'nbf': time.time(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=JWT_TOKEN_EXPIRATION_DAYS),
            'data': data
        }
        return jwt.encode(token, SECRET_KEY)
    
    @staticmethod
    def check_jwt(request):
        try:
            authen_token = request.headers['Authorization'].split()[1]
            token = jwt.decode(authen_token, SECRET_KEY, ['HS256'])
            if(token):
                cur_time = time.time()
                if(token['exp'] > cur_time):
                    return token['data']
        except Exception as e:
            logging.exception(f'Token Error:')
            return None
    
    @staticmethod
    def check_jwt_detail(request):
        try:
            authen_token = request.headers['Authorization'].split()[1]
            token = jwt.decode(authen_token, SECRET_KEY, ['HS256'])
            if(token):
                cur_time = time.time()
                if(token['exp'] > cur_time):
                    if(token['data'].get('email') and (token['data'].get('email') == request.data.get('email'))):
                        return token['data']
                    elif(token['data'].get('fb_id') and (token['data'].get('fb_id') == request.data.get('fb_id'))):
                        return token['data']
                    elif(token['data'].get('uid') and (token['data'].get('uid') == request.data.get('uid'))):
                        return token['data']
                    else:
                        raise cus_exception.TokenInvalid()
        except Exception as e:
            logging.exception(f'Token Error:')
            raise cus_exception.TokenInvalid()

class CheckAuthen(BasePermission):

    def has_permission(self, request, view):
        return bool(JwtAuthen.check_jwt_detail(request))