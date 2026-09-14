from rest_framework.routers import DefaultRouter
from .views import BlogCategoryViewSet, BlogPostViewSet, TagViewSet
router=DefaultRouter(); router.register("blogs",BlogPostViewSet,basename="blog"); router.register("blog-categories",BlogCategoryViewSet); router.register("blog-tags",TagViewSet)
urlpatterns=router.urls
