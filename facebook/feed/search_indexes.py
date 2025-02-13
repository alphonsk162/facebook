from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from user.models import UserDetails


@registry.register_document
class UserDetailsDocument(Document):
    full_name = fields.TextField()

    class Index:
        name = "users"  # Name of the Elasticsearch index

    class Django:
        model = UserDetails
        fields = [
            "first_name",
            "last_name",
            "location",
        ]

    def prepare_full_name(self, instance):
        return f"{instance.first_name} {instance.last_name}".strip()
