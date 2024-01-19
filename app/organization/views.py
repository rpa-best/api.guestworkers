from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from .serializers import OrganizationSerializer
from .models import Organization
from .validators import inn_check_api_validator


class OrganizationView(ModelViewSet):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.get_orgs(self.request.user, self.action in ["create", "partial_update", "update"])


class OrganizationApiView(RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        org_data = inn_check_api_validator(self.kwargs.get("inn"))
        return Response({
            "inn": self.kwargs.get("inn"),
            "name": org_data.get('c'),
            "ogrn": org_data.get('o'),
            "address": org_data.get('a'),
            "kpp": org_data.get('p'),
        })
