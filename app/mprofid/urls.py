from django.urls import path, include
from .views import (
    dictionary_urls, medclieints, subdivisions, professions
)
from . import workers


urlpatterns = [
    path('', include(dictionary_urls())),
    path('medclients/', medclieints, name='medclients'),
    path('medclients/<int:med_client_id>/subdivisions/', subdivisions, name='subdivisions'),
    path('medclients/<int:med_client_id>/professions/', professions, name='professions'),
    path('worker/<worker_id>/invoice/', workers.InvoiceListCreateView.as_view()),
    path('worker/<worker_id>/invoice/<int:order_id>/', workers.InvoiceDetailView.as_view()),
    path('worker/<worker_id>/invoice/<int:order_id>/direction/', workers.InvoiceDirectionView.as_view()),
    path('worker/<worker_id>/invoice/<int:order_id>/status-history/', workers.InvoiceHistoryStatusView.as_view()),
]
