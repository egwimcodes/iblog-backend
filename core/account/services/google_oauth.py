from google.oauth2 import id_token
from google.auth.transport import requests as google_request
from django.conf import settings


def verify_google_token(token):
    """
    Verify Google ID token and return user info.
    """
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            google_request.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        if id_info.get('aud') != settings.GOOGLE_CLIENT_ID:
            raise ValueError("Unrecognized client.")
        return id_info
    except ValueError as e:
        # re-raise instead of returning
        raise e

    