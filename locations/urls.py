from rest_framework.routers import DefaultRouter
from .views import AreaViewSet, DistrictViewSet, DivisionViewSet

router = DefaultRouter()
router.register("divisions", DivisionViewSet)
router.register("districts", DistrictViewSet)
router.register("areas", AreaViewSet)
urlpatterns = router.urls
