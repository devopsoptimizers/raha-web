from django.utils import timezone
from rest_framework import serializers
from common.captcha import CaptchaSerializerMixin
from .models import Inquiry, InquiryNote, MeetingRequest, PublicMessage
class PublicFormSerializer(CaptchaSerializerMixin,serializers.ModelSerializer):
    website=serializers.CharField(required=False,write_only=True,allow_blank=True)
    def validate_website(self,value):
        if value: raise serializers.ValidationError("Invalid submission.")
        return value
    def create(self,validated_data):
        validated_data.pop("website",None)
        return super().create(validated_data)
class InquirySerializer(PublicFormSerializer):
    class Meta: model=Inquiry; fields="__all__"; read_only_fields=("created_by","updated_by","assigned_to","status","internal_notes")
    def validate(self,attrs):
        at=attrs.get("apartment_type"); project=attrs.get("project")
        if at and project and at.project_id != project.id: raise serializers.ValidationError({"apartment_type":"Apartment type does not belong to project."})
        return attrs
class InquiryAdminSerializer(serializers.ModelSerializer):
    class Meta: model=Inquiry; fields="__all__"; read_only_fields=("created_by","updated_by")
class InquiryNoteSerializer(serializers.ModelSerializer):
    class Meta: model=InquiryNote; fields="__all__"; read_only_fields=("created_by","updated_by","inquiry")
class MeetingSerializer(PublicFormSerializer):
    class Meta: model=MeetingRequest; fields="__all__"; read_only_fields=("created_by","updated_by","assigned_to","status")
    def validate_preferred_date(self,value):
        if value < timezone.localdate(): raise serializers.ValidationError("Meeting date cannot be in the past.")
        return value
class MeetingAdminSerializer(serializers.ModelSerializer):
    class Meta: model=MeetingRequest; fields="__all__"; read_only_fields=("created_by","updated_by")
class PublicMessageSerializer(PublicFormSerializer):
    class Meta: model=PublicMessage; fields="__all__"; read_only_fields=("created_by","updated_by","kind","is_resolved")
class PublicMessageAdminSerializer(serializers.ModelSerializer):
    class Meta: model=PublicMessage; fields="__all__"; read_only_fields=("created_by","updated_by","kind")
