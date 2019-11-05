from my_utils import cus_exception

def check_required_fields(required_fields, request_data):
    for item in required_fields:
        if item not in request_data:
            raise cus_exception.ValidationFailed(f'Lack of {item} field')

    if(len(required_fields) != len(request_data)):
        raise cus_exception.ValidationFailed(f'You have unexpected fields')