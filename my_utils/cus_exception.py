from rest_framework.exceptions import APIException
from rest_framework import status
from my_utils import response_status



class ValidationFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('Invalid input.')
    default_code = 'invalid'

    def __init__(self, message=None, detail=None, code=None):

        self.detail = {
            'ReponseCode': response_status.FAIL.code,
            'ReponseMessage': message
        }


class TokenInvalid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('Invalid input.')
    default_code = 'invalid'

    def __init__(self, message=None, detail=None, code=None):

        self.detail = {
            'ReponseCode': response_status.FAIL.code,
            'ReponseMessage': "Token invalid"
        }