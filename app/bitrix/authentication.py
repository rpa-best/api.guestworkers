from rest_framework.authentication import TokenAuthentication as _TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TokenAuthentication(_TokenAuthentication):

    def authenticate(self, request):
        token = request.data.get("auth", {}).get("application_token")

        if not token:
            return super().authenticate(request)

        return self.authenticate_credentials(token)