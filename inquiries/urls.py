from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, FeedbackViewSet, InquiryViewSet, MeetingViewSet, SuggestionViewSet
router=DefaultRouter(); router.register("inquiries",InquiryViewSet); router.register("meeting-requests",MeetingViewSet); router.register("contact-messages",ContactViewSet,basename="contact-message"); router.register("feedback",FeedbackViewSet,basename="feedback"); router.register("suggestions",SuggestionViewSet,basename="suggestion")
urlpatterns=router.urls
