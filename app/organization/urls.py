from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("org", views.OrganizationView, "")
router.register(r"org/(?P<inn>\d+)/docs", views.OrganizationDocView, "")
router.register(r"org/(?P<inn>\d+)/table", views.OrganizationTableView, "")

urlpatterns = [
    path("", include(router.urls)),
    path("doc/<inn>/", views.DocumentView.as_view()),
    path("doc-type/", views.DocumentTypeView.as_view()),
    path("info/<inn>/", views.OrganizationApiView.as_view()),
]