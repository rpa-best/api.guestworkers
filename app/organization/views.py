from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from .serializers import OrganizationSerializer, OrganizationShortSerializer
from .models import Organization
from .validators import inn_check_api_validator


class OrganizationView(ModelViewSet):
    serializer_class = OrganizationSerializer
    pagination_class = None
    lookup_url_kwarg = "inn"
    lookup_field = "inn"
    http_method_names = ["get", "head", "post", "patch", "delete"]

    def get_queryset(self):
        return Organization.get_orgs(self.request.user, self.action in ["create", "partial_update", "update"])
    
    def update(self, request, *args, **kwargs):
        request.data.update(inn=self.kwargs.get("inn"))
        return super().update(request, *args, **kwargs)


class OrganizationApiView(ListAPIView):
    pagination_class = None
    serializer_class = OrganizationShortSerializer

    def list(self, request, *args, **kwargs):
        org_data = inn_check_api_validator(self.kwargs.get("inn"), True)
        return Response([{
            "inn": org.get("i"),
            "name": org.get('c'),
            "ogrn": org.get('o'),
            "address": org.get('a'),
            "kpp": org.get('p'),
        } for org in org_data])
