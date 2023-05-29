from rest_framework.generics import ListAPIView
from .models import AlbumDetailPage
from .serializers import AlbumDetailPageSerializer

class AlbumDetailPageAPIView(ListAPIView):
    serializer_class = AlbumDetailPageSerializer

    def get_queryset(self):
        return AlbumDetailPage.objects.filter(is_public=True)
