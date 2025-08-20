from django.urls import path
from .views import BitrixWebHook


urlpatterns = [
    path("webhook/", BitrixWebHook.as_view(), name="bitrix_webhook"),
]