from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from common.mixins import AuditActorMixin
from common.permissions import IsContentAdmin
from .models import BlogCategory, BlogPost, Tag
from .serializers import BlogCategorySerializer, BlogPostSerializer, TagSerializer
class BlogPostViewSet(AuditActorMixin, viewsets.ModelViewSet):
    serializer_class=BlogPostSerializer; permission_classes=[IsContentAdmin]; filterset_fields=("category","tags","is_featured","is_published"); search_fields=("title","excerpt","content"); ordering_fields=("published_at","created_at")
    def get_queryset(self):
        qs=BlogPost.objects.select_related("category","author").prefetch_related("tags")
        return qs if self.request.user.is_authenticated else qs.filter(is_published=True, is_active=True)
    def perform_create(self, serializer): serializer.save(author=self.request.user, created_by=self.request.user, updated_by=self.request.user)
    @action(detail=False, url_path="slug/(?P<slug>[-a-zA-Z0-9_]+)")
    def by_slug(self, request, slug=None): return Response(self.get_serializer(self.get_queryset().get(slug=slug)).data)
    @action(detail=True)
    def related(self, request, pk=None):
        post=self.get_object(); qs=self.get_queryset().filter(category=post.category).exclude(pk=post.pk)[:4]; return Response(self.get_serializer(qs,many=True).data)
class BlogCategoryViewSet(AuditActorMixin, viewsets.ModelViewSet): queryset=BlogCategory.objects.all(); serializer_class=BlogCategorySerializer; permission_classes=[IsContentAdmin]; search_fields=("name","slug")
class TagViewSet(AuditActorMixin, viewsets.ModelViewSet): queryset=Tag.objects.all(); serializer_class=TagSerializer; permission_classes=[IsContentAdmin]; search_fields=("name","slug")
