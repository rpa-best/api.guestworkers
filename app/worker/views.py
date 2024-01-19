import pandas as pd
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_pandas.views import PandasView
from core.utils.renderers import PandasExcelRenderer
from organization.models import ROLE_OWNER, ROLE_CLIENT, UserToOrganization
from organization.permissions import has_permission
from organization.serializers import WorkerToOrganizationUpdateSerializer
from oauth.models import User
from . import serializers, models, filters


class UploadInstanceView(PandasView):
    renderer_classes = (PandasExcelRenderer,)

    def list(self, request, *args, **kwargs):
        data = serializers.genereate_upload_instance()
        response = Response(pd.DataFrame(data))
        return self.update_pandas_headers(response)


class UploadCheckView(CreateAPIView):
    serializer_class = serializers.UploadCheckSerializer

    def check_permissions(self, request):
        return has_permission(None, request.user, [ROLE_OWNER, ROLE_CLIENT])


class UploadPerformView(CreateAPIView):
    serializer_class = serializers.UploadPerformSerializer

    def check_permissions(self, request):
        return has_permission(None, request.user, [ROLE_OWNER, ROLE_CLIENT])


class DocTypeView(ReadOnlyModelViewSet):
    serializer_class = serializers.DocTypeSerializer
    queryset = models.DocType.objects.all()
    pagination_class = None
    filterset_class = filters.DocTypeFilter
    search_fields = ["name"]


class WorkerView(ModelViewSet):
    http_method_names = ["get", "head", "patch", "post", "delete"]
    filterset_class = filters.WorkerFilter
    search_fields = ["first_name", "last_name", "surname", "passport"]

    def get_queryset(self):
        user = self.request.user
        return User.objects.get_users(user)
    
    def get_serializer_class(self):
        if self.action in ["list"]:
            return serializers.WorkerListSerializer
        elif self.action in ["partial_update"]:
            return serializers.WorkerUpdateSerializer
        elif self.action in ["create"]:
            return serializers.WorkerCreateSerializer
        return serializers.WorkerRetriveSerializer
    
    def check_permissions(self, request):
        super().check_permissions(request)
        if self.action in ["create"] and not has_permission(None, request.user, [ROLE_OWNER, ROLE_CLIENT]):
            self.permission_denied(request)


class WorkerToUserUpdateView(ModelViewSet):
    http_method_names = ["get", "head", "patch"]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "partial_update":
            return WorkerToOrganizationUpdateSerializer
        return serializers.WorkerToOrganizationSerializer

    def get_queryset(self):
        return UserToOrganization.objects.filter(user__in=User.objects.get_users(self.request.user, self.request.method == "PATCH")).distinct("id")
    
    def update(self, request, *args, **kwargs):
        request.data.update(user=self.kwargs.get("worker_id"))
        return super().update(request, *args, **kwargs)
    

class WorkerDocUpdateView(ModelViewSet):
    http_method_names = ["get", "head", "patch", "post"]
    pagination_class = None
    filterset_class = filters.WorkerDocFilter

    def get_serializer_class(self):
        if self.action in ["partial_update", "create"]:
            return serializers.WorkerDocUpdateSerializer
        return serializers.WorkerDocShowSerializer
    
    def get_queryset(self):
        return models.WorkerDoc.objects.filter(user__in=User.objects.get_users(self.request.user, self.request.method == "PATCH")).distinct("id")
    
    def update(self, request, *args, **kwargs):
        request.data.update(user=self.kwargs.get("worker_id"))
        return super().update(request, *args, **kwargs)
