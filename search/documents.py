from django_elasticsearch_dsl import DocType, Index
from sde.models import Type

type = Index('types')

@type.doc_type
class TypeDocument(DocType):
    class Meta:
        model = Type
        fields = [
            'name'
        ]
        auto_refresh = False