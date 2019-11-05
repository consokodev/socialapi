from rest_framework.response import Response
from my_utils import response_status

def response_fail():
    return Response({
        'ReponseCode': response_status.FAIL.code,
        'ReponseMessage': response_status.FAIL.message
    })

def response_success():
    return Response({
        'ReponseCode': response_status.SUCCESS.code,
        'ReponseMessage': response_status.SUCCESS.message
    })