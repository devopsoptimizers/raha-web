from rest_framework import serializers
from .models import SiteSettings
class PublicSettingsSerializer(serializers.ModelSerializer):
    class Meta: model=SiteSettings; exclude=("created_by","updated_by","google_analytics_id","google_tag_manager_id","facebook_pixel_id")
class SettingsSerializer(serializers.ModelSerializer):
    class Meta: model=SiteSettings; fields="__all__"; read_only_fields=("created_by","updated_by")
