from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("org", views.OrganizationView, "")

urlpatterns = [
    path("", include(router.urls)),
    path("info/<inn>/", views.OrganizationApiView.as_view()),
]