import pandas as pd
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_pandas.views import PandasView
from core.utils.renderers import PandasExcelRenderer
from organization.models import UserToOrganization, STATUS_CHECKING, ROLE_WORKER
from oauth.models import User
from . import serializers


class UploadInstanceView(PandasView):
    renderer_classes = (PandasExcelRenderer,)

    def list(self, request, *args, **kwargs):
        data = serializers.genereate_upload_instance()
        response = Response(pd.DataFrame(data))
        return self.update_pandas_headers(response)


class UploadCheckView(CreateAPIView):
    serializer_class = serializers.UploadCheckSerializer


class UploadPerformView(CreateAPIView):
    serializer_class = serializers.UploadPerformSerializer


class WorkerView(ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return User.objects.all()
        users_id = []
        for uto in UserToOrganization.objects.exclude(status=STATUS_CHECKING).filter(user=user):
            if uto.role in [ROLE_WORKER]:
                users_id.append(uto.user_id)
            else:
                users_id = [*users_id, *UserToOrganization.objects.exclude(status=STATUS_CHECKING).filter(org_id=uto.org_id).values_list("user_id", flat=True)]
        return User.objects.filter(id__in=users_id)
    
    def get_serializer_class(self):
        if self.action in ["list"]:
            return serializers.WorkerListSerializer
        elif self.action in ["partial_update"]:
            return serializers.WorkerUpdateSerializer
        elif self.action in ["create"]:
            return serializers.WorkerCreateSerializer
        return serializers.WorkerRetriveSerializer
            