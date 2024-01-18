from rest_pandas import PandasExcelRenderer as _PandasExcelRenderer


class PandasExcelRenderer(_PandasExcelRenderer):
    def get_pandas_kwargs(self, data, renderer_context):
        return {
            "index": False
        }
