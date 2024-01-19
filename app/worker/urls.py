from django.urls import path

from . import views

urlpatterns = [
    path('upload-instance/', views.UploadInstanceView.as_view()),
    path('upload-check/', views.UploadCheckView.as_view()),
    path('upload-perform/', )
]
