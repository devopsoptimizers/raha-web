from rest_framework import viewsets
from common.mixins import AuditActorMixin
from common.permissions import IsProjectManager
from .models import Area, District, Division
from .serializers import AreaSerializer, DistrictSerializer, DivisionSerializer

class DivisionViewSet(AuditActorMixin, viewsets.ModelViewSet):
    queryset = Division.objects.all().order_by("name")
    serializer_class = DivisionSerializer
    permission_classes = [IsProjectManager]
    search_fields = ("name",)

class DistrictViewSet(AuditActorMixin, viewsets.ModelViewSet):
    queryset = District.objects.select_related("division").order_by("name")
    serializer_class = DistrictSerializer
    permission_classes = [IsProjectManager]
    filterset_fields = ("division", "is_active")
    search_fields = ("name",)

class AreaViewSet(AuditActorMixin, viewsets.ModelViewSet):
    queryset = Area.objects.select_related("district", "district__division").order_by("name")
    serializer_class = AreaSerializer
    permission_classes = [IsProjectManager]
    filterset_fields = ("district", "district__division", "is_active")
    search_fields = ("name",)
