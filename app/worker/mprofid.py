from mprofid.views import OrderCreateView, OrderDetailView, OrderListView


class InvoiceCreateView(OrderCreateView):

    def create(self, request, *args, **kwargs):
        request.data.update(worker=self.kwargs.get('worker_id'))
        return super().create(request, *args, **kwargs)


class InvoiceListView(OrderListView):

    def get_queryset(self):
        return self.queryset.filter(worker_id=self.kwargs.get('worker_id'))


class InvoiceDetailView(OrderDetailView):
    pass
