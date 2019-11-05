from datetime import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import User
from my_utils.check_fields import check_required_fields
from my_utils.jwt_authen import CheckAuthen
from my_utils import response_status
from my_utils.response_utils import response_fail
from scmodels.serializers.user_serializers import GetUserProfileSerializer

# Create your views here.

class ListUser(APIView):
    permission_classes = [CheckAuthen]

    def get(self, request, *args, **kwargs):
        required_fields = ["last_uid", "limit", "uid"]
        check_required_fields(required_fields, self.kwargs)

        limit = self.kwargs.get("limit")
        last_uid = 0 if self.kwargs.get("last_uid") == "0" else self.kwargs.get("last_uid")
        check_point = datetime.now()
        if(last_uid):
            try:
                user = User.objects.get(uid=last_uid)
                check_point = user.created_at
            except Exception as e:
                return response_fail()
        
        query_ret = User.objects.collect_list_users(check_point, limit)
        responseData = GetUserProfileSerializer(query_ret, many=True).data
        return Response({
            "responseCode": response_status.SUCCESS.code,
            "responseMessage": response_status.SUCCESS.message,
            "responseData": responseData,
        })