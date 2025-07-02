from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mprofid.views import OrderDirectionView
from . import views
from .mprofid import InvoiceCreateView, InvoiceDetailView, InvoiceListView

router = DefaultRouter()
router.register("worker", views.WorkerView, "")
router.register("doc-type", views.DocTypeView, "")
router.register(r"worker/(?P<worker_id>\d+)/org", views.WorkerToUserUpdateView, "")
router.register(r"worker/(?P<worker_id>\d+)/doc", views.WorkerDocUpdateView, "")

urlpatterns = [
    path('', include(router.urls)),
    path('upload-instance/', views.UploadInstanceView.as_view()),
    path('upload-check/', views.UploadCheckView.as_view()),
    path('upload-perform/', views.UploadPerformView.as_view()),
    path('worker/<worker_id>/mprofid-invoice/', InvoiceCreateView.as_view()),
    path('worker/<worker_id>/mprofid-invoice/', InvoiceListView.as_view()),
    path('worker/<worker_id>/mprofid-invoice/<int:order_id>/', InvoiceDetailView.as_view()),
    path('worker/<worker_id>/mprofid-invoice/<int:order_id>/direction/', OrderDirectionView.as_view()),
]
