from django.utils.encoding import force_str
from rest_framework import filters


class OrderingFilter(filters.OrderingFilter):
    def get_schema_operation_parameters(self, view):
        try:
            ordering_params = [
                term[0] for term in self.get_valid_fields(view.get_queryset(), view, {'request': view.request})
            ]
        except AssertionError:
            ordering_params = []
        return [
            {
                'name': self.ordering_param,
                'required': False,
                'in': 'query',
                'description': f'{force_str(self.ordering_description)}. (Params: {", ".join(ordering_params)})',
                'schema': {
                    'type': 'string',
                },
            },
        ]