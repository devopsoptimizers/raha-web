from rest_framework import generics
from rest_framework.permissions import AllowAny
from common.permissions import IsContentAdmin
from .models import SiteSettings
from .serializers import PublicSettingsSerializer, SettingsSerializer
class SettingsMixin:
    def get_object(self): return SiteSettings.objects.first()
class PublicSettingsView(SettingsMixin,generics.RetrieveAPIView): permission_classes=[AllowAny]; serializer_class=PublicSettingsSerializer
class SettingsView(SettingsMixin,generics.RetrieveUpdateAPIView): permission_classes=[IsContentAdmin]; serializer_class=SettingsSerializer
