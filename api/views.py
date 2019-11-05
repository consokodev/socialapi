import json
import random
import string
from pprint import pprint

import facebook
import jwt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User, UserOTP
from scmodels.serializers.user_serializers import (GetUserProfileSerializer,
                             UpdateUserProfileSerializer,
                             UserResetPassSerializer, UserSerializer
                            )
from my_utils.check_fields import check_required_fields
from my_utils import response_status
from my_utils.jwt_authen import CheckAuthen, JwtAuthen
from my_utils.log_module import logger_socialapi
from my_utils.response_utils import response_fail, response_success
from socialapi.settings import SECRET_KEY
from api.tasks import email_reset_pass


class CreateUser(APIView):

    def post(self, request, *args, **kwargs):
        required_fields = ["email", "password"]
        check_required_fields(required_fields, request.data)
        
        user_serializer = UserSerializer(data=request.data)

        if(user_serializer.is_valid()):
            try:
                email = user_serializer.validated_data.get("email")
                User.objects.get(email=email)
                return Response({
                    'ResponseCode': response_status.USER_EXISTED.code,
                    'ResponseMessage': response_status.USER_EXISTED.message
                })
            except ObjectDoesNotExist as e:
                user = user_serializer.save()
                logger_socialapi.info(f'SUCCESS: Created User {user.email}')
                responseData = dict(GetUserProfileSerializer(user).data)
                return Response({
                    "responseCode": response_status.SUCCESS.code,
                    "responseMessage": response_status.SUCCESS.message,
                    "token": JwtAuthen.create_jwt(responseData),
                    "responseData": responseData,
                })
            except Exception as e:
                logger_socialapi.exception(f'Error: Register Failed')
                return response_fail()
        elif(user_serializer.errors):
            return Response({
                'ResponseCode': response_status.FAIL.code,
                'ResponseMessage': user_serializer.errors
            })


class LoginUserFace(APIView):

    def post(self, request, *args, **kwargs):
        required_fields = ["fb_id", "access_token"]
        check_required_fields(required_fields, request.data)
        
        try:
            fb_id = request.data.get('fb_id')
            access_token = request.data.get('access_token')
            profile = facebook.GraphAPI(access_token=access_token).get_object('me', fields='email,name,gender,birthday')
        except Exception as e:
            logger_socialapi.exception(f'Error: Register Facebook Failed')
            return response_fail()
        if(fb_id == profile.get('id')):
            fb_id, email, name = profile.get('id'), profile.get('email'), profile.get('name')
            try:
                user = User.objects.get(fb_id=fb_id)
                if(hasattr(user, 'is_banned') and user.is_banned == 1):
                    return Response({
                    "responseCode": response_status.USER_BANNED.code,
                    "responseMessage": response_status.USER_BANNED.message 
                })
                # elif(hasattr(user, 'is_activated') and user.is_activated == 0):
                #     return Response({
                #         "responseCode": response_status.USER_INACTIVATE.code,
                #         "responseMessage": response_status.USER_INACTIVATE.message 
                #     })
                responseData = dict(GetUserProfileSerializer(user).data)
            except ObjectDoesNotExist as e:
                logger_socialapi.info(f'Register user {fb_id}')
                user = User.objects.create(fb_id=fb_id, email=email, fullname=name)
                responseData = dict(GetUserProfileSerializer(user).data)
            except Exception as e:
                logger_socialapi.exception(f'Error: Register Failed {fb_id}')
                return response_fail()
            return Response({
                "responseCode": response_status.SUCCESS.code,
                "responseMessage": response_status.SUCCESS.message,
                "token": JwtAuthen.create_jwt(responseData),
                "responseData": responseData,
                })
        else:
            logger_socialapi.exception(f'Error: Register Failed {fb_id}')
            return response_fail()


# User login if sucess, then return jwt vs user data
class LoginUser(APIView):

    def post(self, request, *args, **kwargs):
        required_fields = ["email", "password"]
        check_required_fields(required_fields, request.data)
        
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = User.objects.get(email=email, password=password)
            if(hasattr(user, 'is_banned') and user.is_banned == 1):
                return Response({
                    "responseCode": response_status.USER_BANNED.code,
                    "responseMessage": response_status.USER_BANNED.message 
                })
            # elif(hasattr(user, 'is_activated') and user.is_activated == 0):
            #     return Response({
            #         "responseCode": response_status.USER_INACTIVATE.code,
            #         "responseMessage": response_status.USER_INACTIVATE.message 
            #     })
            else:
                responseData = dict(GetUserProfileSerializer(user).data)
                return Response({
                    "responseCode": response_status.SUCCESS.code,
                    "responseMessage": response_status.SUCCESS.message,
                    "token": JwtAuthen.create_jwt(responseData),
                    "responseData": responseData,
                })
        except ObjectDoesNotExist as e:
            return Response(
                {
                    "responseCode": response_status.USER_LOGIN_FAILED.code,
                    "responseMessage": response_status.USER_LOGIN_FAILED.message,
                }
            )


class UpdateUser(APIView):
    permission_classes = [CheckAuthen]

    def put(self, request, *args, **kwargs):
        required_fields = ["uid", "fullname", "gender", "birthday"]
        check_required_fields(required_fields, request.data)

        uid = request.data.get("uid")
        try:
            user = User.objects.get(uid=uid)
            user_serializer = UpdateUserProfileSerializer(user, data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            responseData = dict(user_serializer.data)
            return Response({
                "responseCode": response_status.SUCCESS.code,
                "responseMessage": response_status.SUCCESS.message,
                "responseData": responseData,
            })
        except ObjectDoesNotExist as e:
            return Response({
                "ResponseCode": response_status.USER_NOT_EXISTED.code,
                "ResponseMessage": response_status.USER_NOT_EXISTED.message
            })
        except Exception as e:
            return response_fail()
        

class LogoutUser(APIView):

    def get(self, request, *args, **kwargs):
        return response_success()

class UserResetPass(APIView):

    def post(self, request, *args, **kwargs):
        required_fields = ["email"]
        check_required_fields(required_fields, request.data)
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            otp_code_reset_pass = ''.join(random.choices(string.digits, k = 4))
            user_otp = UserResetPassSerializer(data={"uid": str(user.uid),"email": email, "otp_code_reset_pass": otp_code_reset_pass})
            user_otp.is_valid(raise_exception=True)
            user_otp.save()
            #email_reset_pass.delay(email, otp_code_reset_pass)
            return response_success()
        except ObjectDoesNotExist as e:
            return Response({
                "ResponseCode": response_status.USER_NOT_EXISTED.code,
                "ResponseMessage": response_status.USER_NOT_EXISTED.message
            })
        except Exception as e:
            return response_fail()


class HelloView(APIView):
    permission_classes = [CheckAuthen]

    def get(self, request):
        return Response('Huraaaaa')
