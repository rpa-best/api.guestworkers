from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from .api import Api
from .models import WorkerInvoice
from .serializers import WorkerInvoiceShowSerializer


api = Api()

@extend_schema_view(post=extend_schema(tags=['mprofid']), get=extend_schema(tags=['mprofid']))
class InvoiceListCreateView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkerInvoiceShowSerializer

    def get_queryset(self):
        return WorkerInvoice.objects.filter(worker_id=self.kwargs.get('worker_id'))

    def create(self, request, *args, **kwargs):
        worker_id = self.kwargs.get('worker_id')
        response = api.post_order(request.data)
        if not response.ok:
            return Response({"detail": response.json(), "code": "api_error"}, status=403)
        id = response.json().get('id')
        WorkerInvoice.objects.create(id=id, worker_id=worker_id)
        return Response({'id': id})


@extend_schema_view(get=extend_schema(tags=['mprofid']), delete=extend_schema(tags=['mprofid']))
class InvoiceDetailView(RetrieveDestroyAPIView):
    serializer_class = WorkerInvoiceShowSerializer
    lookup_url_kwarg = 'order_id'

    def get_queryset(self):
        return WorkerInvoice.objects.filter(worker_id=self.kwargs.get('worker_id'))

    def perform_destroy(self, instance):
        response = api.delete_order(instance.id)
        if not response.ok:
            return Response({"detail": response.json(), "code": "api_error"}, status=403)


@extend_schema_view(get=extend_schema(tags=['mprofid']))
class InvoiceDirectionView(RetrieveAPIView):
    lookup_url_kwarg = 'order_id'

    def get_queryset(self):
        return WorkerInvoice.objects.filter(worker_id=self.kwargs.get('worker_id'))
    
    def get(self, request, *args, **kwargs):
        invoice: WorkerInvoice = self.get_object()
        response = api.get_direction_order(invoice.id)
        if not response.ok:
            return Response({"detail": response.json(), "code": "api_error"}, status=403)
        r = HttpResponse(response.content, content_type='application/pdf')
        r['Content-Disposition'] = response.headers.get('Content-Disposition', f'attachment; filename="{invoice.worker}-{invoice.pk}.pdf"')
        return r

@extend_schema_view(get=extend_schema(tags=['mprofid']))
class InvoiceHistoryStatusView(RetrieveAPIView):
    lookup_url_kwarg = 'order_id'

    def get_queryset(self):
        return WorkerInvoice.objects.filter(worker_id=self.kwargs.get('worker_id'))
    
    def get(self, request, *args, **kwargs):
        invoice = self.get_object()
        response = api.get_order_status_history(invoice.id)
        if not response.ok:
            return Response({"detail": response.text, "code": "api_error"}, status=403)
        return Response(response.json())
