from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

class OAuth2PassThruAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Raise any exceptions as directed by the middleware
        if hasattr(request, "oauth2_exception"):
            raise request.oauth2_exception

        # Authenticate user in case of a valid token
        if hasattr(request, "oauth2_token"):
            return (request.user, request.oauth2_token)

        return None

    def authenticate_header(self, request):
        return 'Bearer realm="api"'