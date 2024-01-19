from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("worker", views.WorkerView, "")
router.register("doc-type", views.DocTypeView, "")
urlpatterns = [
    path('', include(router.urls)),
    path('worker/<worker_id>/org/', views.WorkerToUserUpdateView.as_view()),
    path('worker/<worker_id>/docs/', views.WorkerDocUpdateView.as_view()),
    path('upload-instance/', views.UploadInstanceView.as_view()),
    path('upload-check/', views.UploadCheckView.as_view()),
    path('upload-perform/', views.UploadPerformView.as_view())
]
