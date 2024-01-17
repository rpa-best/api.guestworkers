from rest_framework import parsers


class MultiPartParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        data.data._mutable = True
        data.files._mutable = True
        return data
    