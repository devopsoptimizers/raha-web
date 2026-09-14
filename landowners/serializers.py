from rest_framework import serializers
from common.captcha import CaptchaSerializerMixin
from .models import LandownerProposal, ProposalDocument
class ProposalDocumentSerializer(serializers.ModelSerializer):
    class Meta: model=ProposalDocument; fields=("id","file","label","created_at")
class LandownerPublicSerializer(CaptchaSerializerMixin,serializers.ModelSerializer):
    website=serializers.CharField(required=False,write_only=True,allow_blank=True)
    class Meta: model=LandownerProposal; exclude=("assigned_to","status","internal_notes","created_by","updated_by")
    def validate_website(self,value):
        if value: raise serializers.ValidationError("Invalid submission.")
        return value
    def create(self,validated_data):
        validated_data.pop("website",None)
        return super().create(validated_data)
    def validate(self,attrs):
        if attrs["district"].division_id != attrs["division"].id: raise serializers.ValidationError({"district":"District does not belong to division."})
        if attrs["area"].district_id != attrs["district"].id: raise serializers.ValidationError({"area":"Area does not belong to district."})
        return attrs
class LandownerAdminSerializer(serializers.ModelSerializer):
    documents=ProposalDocumentSerializer(many=True,read_only=True)
    class Meta: model=LandownerProposal; fields="__all__"; read_only_fields=("created_by","updated_by")
