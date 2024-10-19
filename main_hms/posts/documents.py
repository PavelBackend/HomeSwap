from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Posts


@registry.register_document
class PostDocument(Document):
    class Index:
        name = 'posts'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Posts

        fields = [
            'title',
            'content'
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Configure how the index should be refreshed after an update.
        # See Elasticsearch documentation for supported options:
        # https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-refresh.html
        # This per-Document setting overrides settings.ELASTICSEARCH_DSL_AUTO_REFRESH.
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000