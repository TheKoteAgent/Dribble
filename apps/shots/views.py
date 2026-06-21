from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Shot
from .serializers import ShotSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ShotsPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 50


class ShotViewSet(viewsets.ModelViewSet):
    queryset = Shot.objects.all().select_related('author').prefetch_related('tags')
    serializer_class = ShotSerializer
    pagination_class = ShotsPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Фільтрація та Пошук
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        tags_param = self.request.query_params.get('tags')
        if tags_param:
            tags_list = [t.strip().lower() for t in tags_param.split(',') if t.strip()]
            for tag_name in tags_list:
                queryset = queryset.filter(tags__name=tag_name)

        return queryset