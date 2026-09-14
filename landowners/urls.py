from rest_framework.routers import DefaultRouter
from .views import LandownerProposalViewSet
router=DefaultRouter(); router.register("landowner-proposals",LandownerProposalViewSet)
urlpatterns=router.urls
