from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request
from .api import Api


def dictionary_urls():
    api = Api()
    dictionaries = {
        "medCenters": api.get_medcenters,
        "services": api.get_services,
        "parts": api.get_parts,
        "med": api.get_med,
        "status": api.get_status,
        "survey": api.get_survey,
        "pay-types": api.get_paytypes,
        "hazards": api.get_hazards,
        "hazards377": api.get_hazards377,
    }

    @extend_schema(tags=['mprofid'])
    @api_view(['GET'])
    def method(request: Request):
        name = request._request.path.split('/')[-2]
        response = dictionaries[name]()
        if not response.ok:
            return Response({'detail': response.text, 'code': 'api_error'}, 404)
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
