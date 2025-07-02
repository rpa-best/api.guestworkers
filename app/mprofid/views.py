from django.urls import path
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveAPIView, RetrieveDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request
from .models import Order
from .serializers import OrderCreateSerializer, OrderShowSerializer
from .api import Api


@extend_schema_view(post=extend_schema(tags=['mprofid']))
class OrderCreateView(CreateAPIView):
    serializer_class = OrderCreateSerializer


@extend_schema_view(get=extend_schema(tags=['mprofid']))
class OrderListView(ListAPIView):
    serializer_class = OrderShowSerializer
    queryset = Order.objects.all()


@extend_schema_view(get=extend_schema(tags=['mprofid']), delete=extend_schema(tags=['mprofid']))
class OrderDetailView(RetrieveDestroyAPIView):

    def get(self, request, *args, **kwargs):
        response = Api().get_order(self.kwargs.get('order_id'))
        if not response.ok:
            return Response({"detail": response.text, "code": "api_error"}, status=403)
        return Response(response.json())


@extend_schema_view(get=extend_schema(tags=['mprofid']))
class OrderDirectionView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        response = Api().get_direction_order(self.kwargs.get('order_id'))
        if not response.ok:
            return Response({"detail": response.text, "code": "api_error"}, status=403)
        return Response(response.content, content_type='application/pdf')


def dictionary_urls():
    api = Api()
    dictionaries = {
        "services": api.get_services,
        "parts": api.get_parts,
        "med": api.get_med,
        "status": api.get_status,
        "survey": api.get_survey,
        "pay-types": api.get_paytypes,
        "hazards": api.get_hazards,
        "conclusion-status": api.get_conclusion_status,
    }

    @extend_schema(tags=['mprofid'])
    @api_view(['GET'])
    def method(request: Request):
        name = request._request.path.split('/')[-2]
        response = dictionaries[name]()
        if response.status_code == 404:
            return Response({'error': 'Not Found'}, 404)
        return Response(response.json(), response.status_code)

    return [
        path(f'dictionary/{name}/', method) for name in dictionaries.keys()
    ]


@extend_schema(tags=['mprofid'])
@api_view(['GET'])
def medclieints(request):
    api = Api()
    response = api.get_medclients()
    return Response(response.json(), response.status_code)


@extend_schema(tags=['mprofid'])
@api_view(['GET'])
def subdivisions(request, med_client_id):
    api = Api()
    response = api.get_subdivisions(med_client_id)
    return Response(response.json(), response.status_code)


@extend_schema(tags=['mprofid'])
@api_view(['GET'])
def professions(request, med_client_id):
    api = Api()
    response = api.get_professions(med_client_id)
    return Response(response.json(), response.status_code)
