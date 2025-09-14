from rest_framework.views import exception_handler
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        # Handle JWT errors
        if "detail" in response.data:
            response.data = {"message": response.data["detail"]}

        # Handle serializer validation errors
        elif "non_field_errors" in response.data:
            response.data = {"message": response.data["non_field_errors"][0]}

    return response
