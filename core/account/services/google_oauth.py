from google.oauth2 import id_token
from google.auth.transport import requests as google_request
from django.conf import settings


def verify_google_token(token):
    """
    Verify Google ID token and return user info.

    Args:
        id_token_str (str): ID token received from frontend.

    Returns:
        dict: User info from Google.
    Raises:
        ValueError: If the token is invalid.
    """
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            google_request.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        
        if id_info.get('aud') != settings.GOOGLE_CLIENT_ID:
            raise ValueError("Unrecorginized client.")
        return id_info
    except ValueError as e:
        return e
    