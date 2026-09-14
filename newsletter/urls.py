from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import NewsletterIssueViewSet, subscribe, subscribers, unsubscribe, verify
router=DefaultRouter(); router.register("newsletter-issues",NewsletterIssueViewSet)
urlpatterns=[path("",include(router.urls)),path("newsletter/subscribe/",subscribe),path("newsletter/verify/",verify),path("newsletter/unsubscribe/",unsubscribe),path("newsletter/subscribers/",subscribers)]
