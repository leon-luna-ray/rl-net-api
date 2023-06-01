from rest_framework import serializers
from rest_framework.response import Response
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.serializers import PageSerializer
from wagtail.core.models import Page


class BasePageSerializer(PageSerializer):
    preview_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'slug',
            'seo_title',
            'seo_description',
            'preview_thumbnail',
        )

    def get_preview_thumbnail(self, page):
        if page.has_unpublished_changes:
            # Return the preview thumbnail if there are unpublished changes
            return page.get_latest_revision().preview.get_rendition('fill-400x400').url
        else:
            # Return the live thumbnail if there are no unpublished changes
            return page.specific.get_sitemap_image().url


class BasePageDetailView(PagesAPIViewSet):
    base_serializer_class = BasePageSerializer

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
