from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call DRF's default exception handler to get the standard error response
    response = exception_handler(exc, context)

    # If the exception was handled by DRF, customize the response format
    if response is not None:
        response.data = {
            'error': True,
            'status_code': response.status_code,
            'message': response.data
        }
    return response
