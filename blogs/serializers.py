from rest_framework import serializers
from .models import BlogCategory, BlogPost, Tag
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta: model=BlogCategory; fields="__all__"; read_only_fields=("created_by","updated_by")
class TagSerializer(serializers.ModelSerializer):
    class Meta: model=Tag; fields="__all__"; read_only_fields=("created_by","updated_by")
class BlogPostSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    tag_names = serializers.SlugRelatedField(source="tags", many=True, read_only=True, slug_field="name")
    class Meta: model=BlogPost; fields="__all__"; read_only_fields=("created_by","updated_by","deleted_at","author")
