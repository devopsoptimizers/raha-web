from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiTypes, extend_schema
from common.mixins import AuditActorMixin
from common.permissions import IsContentAdmin
from projects.models import Project
from projects.serializers import ProjectListSerializer
from testimonials.models import Testimonial
from .models import Campaign, ContentBlock, Slider, TeamMember
from .serializers import CampaignSerializer, ContentBlockSerializer, SliderSerializer, TeamMemberSerializer, TestimonialSerializer

class ContentViewSet(AuditActorMixin, viewsets.ModelViewSet):
    permission_classes = [IsContentAdmin]
    def perform_create(self, serializer):
        super().perform_create(serializer); cache.delete("homepage:v1")
    def perform_update(self, serializer):
        super().perform_update(serializer); cache.delete("homepage:v1")
    def perform_destroy(self, instance):
        super().perform_destroy(instance); cache.delete("homepage:v1")
class SliderViewSet(ContentViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    search_fields = ("title", "subtitle", "button_label")
    @action(detail=False, methods=["post"])
    def reorder(self, request):
        for item in request.data.get("items", []): Slider.objects.filter(pk=item["id"]).update(display_order=item["display_order"])
        cache.delete("homepage:v1"); return Response(status=status.HTTP_204_NO_CONTENT)
class ContentBlockViewSet(ContentViewSet): queryset = ContentBlock.objects.all(); serializer_class = ContentBlockSerializer; filterset_fields = ("block_type", "is_published")
class CampaignViewSet(ContentViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    filterset_fields = ("is_active",)
    search_fields = ("title", "body")
class TeamMemberViewSet(ContentViewSet): queryset = TeamMember.objects.all(); serializer_class = TeamMemberSerializer; filterset_fields = ("department", "is_active")
class TestimonialViewSet(ContentViewSet):
    queryset = Testimonial.objects.select_related("project")
    serializer_class = TestimonialSerializer
    filterset_fields = ("project", "is_featured", "is_published")
    search_fields = ("customer_name", "customer_type", "title", "description", "project__name")

@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(["GET"])
@permission_classes([AllowAny])
def home(request):
    now = timezone.now()
    sliders = Slider.objects.filter(is_active=True).filter(Q(start_date__isnull=True)|Q(start_date__lte=now)).filter(Q(end_date__isnull=True)|Q(end_date__gte=now))
    campaigns = Campaign.objects.filter(is_active=True, start_date__lte=now, end_date__gte=now).order_by("display_order", "-start_date")[:1]
    data = {"sliders": SliderSerializer(sliders, many=True, context={"request": request}).data, "campaigns": CampaignSerializer(campaigns, many=True, context={"request": request}).data, "featured_projects": ProjectListSerializer(Project.objects.filter(publication_status=Project.Publication.PUBLISHED, is_featured=True).select_related("area")[:8], many=True, context={"request": request}).data, "content": ContentBlockSerializer(ContentBlock.objects.filter(is_published=True, is_active=True), many=True, context={"request": request}).data, "team_members": TeamMemberSerializer(TeamMember.objects.filter(is_active=True), many=True, context={"request": request}).data, "testimonials": TestimonialSerializer(Testimonial.objects.filter(is_published=True, is_featured=True).select_related("project")[:8], many=True, context={"request": request}).data}
    return Response(data)
