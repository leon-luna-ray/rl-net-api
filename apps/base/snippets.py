"""Register Collection snippet."""
from wagtail.snippets.models import register_snippet
from wagtail.models import Collection

# Register Collections as Snippets so we can use the SnippetChooserPanel to select a collection
register_snippet(Collection)