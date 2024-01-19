from django.urls import path
from .views import AuthView, RefreshTokenView, VerifyTokenView, ChangePasswordView, ChangePasswordPerformView, ChangePasswordVerifyView, CreateUserLegalView, AccountView


urlpatterns = [
    path('auth/', AuthView.as_view()),
    path('refresh-token/', RefreshTokenView.as_view()),
    path('token-verify/', VerifyTokenView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('change-password-verify/', ChangePasswordVerifyView.as_view()),
    path('change-password-perform/', ChangePasswordPerformView.as_view()),
    path('create-legal/', CreateUserLegalView.as_view()),
    path('me/', AccountView.as_view())
]
