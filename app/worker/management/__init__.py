
def create_default_doc_types(**kwargs):
    from ..models import DocType, DEFAULT_DOC_TYPES

    for doc in DEFAULT_DOC_TYPES:
        DocType.objects.get_or_create(doc, main=True, slug=doc.get("slug"))