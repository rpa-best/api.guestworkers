import pandas as pd
from rest_framework.response import Response
from rest_pandas.views import PandasView
from core.utils.renderers import PandasExcelRenderer

from .models import DocType, UPLOAD_KWARGS


class UploadInstanceView(PandasView):
    renderer_classes = (PandasExcelRenderer,)

    def list(self, request, *args, **kwargs):
        data = []
        user = {}
        for _, key, value in UPLOAD_KWARGS:
            user[key] = value
        for doc_type in DocType.objects.filter(main=True):
            user[doc_type.name] = "01.01.2024"
        data.append(user)
        response = Response(pd.DataFrame(data))
        return self.update_pandas_headers(response)


class UploadCheckView():
    pass


class UploadPerformView():
    pass
