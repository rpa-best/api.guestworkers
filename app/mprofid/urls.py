from django.urls import path, include
from .views import (
    dictionary_urls, medclieints, subdivisions, professions
)


urlpatterns = [
    path('', include(dictionary_urls())),
    # path('order/', OrderCreateView.as_view(), name='order-create'),
    # path('order/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    # path('order/<int:order_id>/direction/', OrderDirectionView.as_view(), name='order-update'),
    path('medclients/', medclieints, name='medclients'),
    path('medclients/<int:med_client_id>/subdivisions/', subdivisions, name='subdivisions'),
    path('medclients/<int:med_client_id>/professions/', professions, name='professions'),
]
