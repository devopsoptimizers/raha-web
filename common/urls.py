from django.urls import path
from .views import health, liveness, readiness
urlpatterns = [path("health/", health, name="health"), path("health/readiness/", readiness, name="readiness"), path("health/liveness/", liveness, name="liveness")]
