from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, JobViewSet
router=DefaultRouter(); router.register("jobs",JobViewSet,basename="job"); router.register("job-applications",JobApplicationViewSet)
urlpatterns=router.urls
