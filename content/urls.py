from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, ContentBlockViewSet, SliderViewSet, TeamMemberViewSet, TestimonialViewSet, home
router=DefaultRouter(); router.register("sliders", SliderViewSet); router.register("campaigns", CampaignViewSet); router.register("content-blocks", ContentBlockViewSet); router.register("team-members", TeamMemberViewSet); router.register("testimonials", TestimonialViewSet)
urlpatterns=[path("home/", home)] + router.urls
