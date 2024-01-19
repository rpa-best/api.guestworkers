from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("worker", views.WorkerView, "")

urlpatterns = [
    path("", include(router.urls)),
    path('upload-instance/', views.UploadInstanceView.as_view()),
    path('upload-check/', views.UploadCheckView.as_view()),
    path('upload-perform/', views.UploadPerformView.as_view())
]
