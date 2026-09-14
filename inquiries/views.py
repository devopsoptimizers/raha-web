import hashlib, json
from django.core.cache import cache
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from common.mixins import AuditActorMixin
from common.permissions import IsSalesOfficer, IsSupportOfficer
from common.throttles import PublicFormThrottle
from .models import Inquiry, InquiryNote, MeetingRequest, PublicMessage
from .serializers import InquiryAdminSerializer, InquiryNoteSerializer, InquirySerializer, MeetingAdminSerializer, MeetingSerializer, PublicMessageAdminSerializer, PublicMessageSerializer
from .tasks import send_inquiry_confirmation
class PublicCreateStaffViewSet(AuditActorMixin,viewsets.ModelViewSet):
    throttle_classes=[PublicFormThrottle]
    def get_permissions(self): return [AllowAny()] if self.action=="create" else [self.staff_permission()]
    def create(self,request,*args,**kwargs):
        key="submission:"+hashlib.sha256(json.dumps(request.data,sort_keys=True,default=str).encode()).hexdigest()
        if cache.get(key): return Response({"detail":"Duplicate submission."},status=429)
        response=super().create(request,*args,**kwargs); cache.set(key,True,300); return response
class InquiryViewSet(PublicCreateStaffViewSet):
    queryset=Inquiry.objects.select_related("project","apartment_type","assigned_to"); staff_permission=IsSalesOfficer; filterset_fields=("status","assigned_to","project","lead_source"); search_fields=("full_name","phone","email","message","preferred_location","lead_source")
    def get_serializer_class(self): return InquirySerializer if self.action=="create" else InquiryAdminSerializer
    def perform_create(self,serializer):
        obj=serializer.save(); send_inquiry_confirmation(obj.email,str(obj.id))
    @action(detail=True,methods=["patch"])
    def status(self,request,pk=None): return self._patch(request,{"status":request.data.get("status")})
    @action(detail=True,methods=["patch"])
    def assign(self,request,pk=None): return self._patch(request,{"assigned_to":request.data.get("assigned_to")})
    def _patch(self,request,data):
        obj=self.get_object(); s=self.get_serializer(obj,data=data,partial=True); s.is_valid(raise_exception=True); self.perform_update(s); return Response(s.data)
    @action(detail=True,methods=["post"])
    def notes(self,request,pk=None):
        s=InquiryNoteSerializer(data=request.data); s.is_valid(raise_exception=True); s.save(inquiry=self.get_object(),created_by=request.user,updated_by=request.user); return Response(s.data,status=201)
class MeetingViewSet(PublicCreateStaffViewSet):
    queryset=MeetingRequest.objects.select_related("project","assigned_to"); staff_permission=IsSalesOfficer; filterset_fields=("status","meeting_type","assigned_to","project"); search_fields=("customer_name","phone","email","message")
    def get_serializer_class(self): return MeetingSerializer if self.action=="create" else MeetingAdminSerializer
    @action(detail=True,methods=["patch"])
    def status(self,request,pk=None): return self._patch(request,{"status":request.data.get("status")})
    @action(detail=True,methods=["patch"])
    def assign(self,request,pk=None): return self._patch(request,{"assigned_to":request.data.get("assigned_to")})
    def _patch(self,request,data):
        obj=self.get_object(); s=self.get_serializer(obj,data=data,partial=True); s.is_valid(raise_exception=True); self.perform_update(s); return Response(s.data)
class PublicMessageViewSet(PublicCreateStaffViewSet):
    serializer_class=PublicMessageSerializer; staff_permission=IsSupportOfficer; message_kind=None
    filterset_fields=("user_type","is_resolved")
    search_fields=("full_name","phone","email","subject","message")
    def get_queryset(self): return PublicMessage.objects.filter(kind=self.message_kind)
    def get_serializer_class(self): return PublicMessageSerializer if self.action=="create" else PublicMessageAdminSerializer
    def perform_create(self,serializer): serializer.save(kind=self.message_kind)
class ContactViewSet(PublicMessageViewSet): message_kind=PublicMessage.Kind.CONTACT
class FeedbackViewSet(PublicMessageViewSet): message_kind=PublicMessage.Kind.FEEDBACK
class SuggestionViewSet(PublicMessageViewSet): message_kind=PublicMessage.Kind.SUGGESTION
