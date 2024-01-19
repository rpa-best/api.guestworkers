import pandas as pd
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_pandas.views import PandasView
from core.utils.renderers import PandasExcelRenderer
from . import serializers


class UploadInstanceView(PandasView):
    renderer_classes = (PandasExcelRenderer,)

    def list(self, request, *args, **kwargs):
        data = serializers.genereate_upload_instance()
        response = Response(pd.DataFrame(data))
        return self.update_pandas_headers(response)


class UploadCheckView(CreateAPIView):
    serializer_class = serializers.UploadCheckSerializer


class UploadPerformView():
    serializer_class = serializers.UploadPerformSerializer
