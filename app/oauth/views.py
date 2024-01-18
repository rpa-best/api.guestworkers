from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenViewBase
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import ChangePasswordSerializer, ChangePasswordPerformSerializer, ChangePasswordVerifySerializer


class AuthView(TokenObtainPairView):
    pass

class RefreshTokenView(TokenRefreshView):
    pass


class ChangePasswordView(TokenViewBase):
    serializer_class = ChangePasswordSerializer


class ChangePasswordVerifyView(TokenViewBase):
    serializer_class = ChangePasswordVerifySerializer


class ChangePasswordPerformView(TokenViewBase):
    serializer_class = ChangePasswordPerformSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
