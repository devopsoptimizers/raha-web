from rest_framework import serializers
from testimonials.models import Testimonial
from .models import Campaign, ContentBlock, Slider, TeamMember

class SliderSerializer(serializers.ModelSerializer):
    class Meta: model = Slider; fields = "__all__"; read_only_fields = ("created_by", "updated_by")
class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta: model = ContentBlock; fields = "__all__"; read_only_fields = ("created_by", "updated_by")
class CampaignSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta: model = Campaign; fields = "__all__"; read_only_fields = ("created_by", "updated_by")

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        body = attrs.get("body", getattr(self.instance, "body", ""))
        image = attrs.get("image", getattr(self.instance, "image", None))
        if start and end and end <= start:
            raise serializers.ValidationError({"end_date": "End date must be after the start date."})
        if not str(body or "").strip() and not image:
            raise serializers.ValidationError({"body": "Add a campaign image, a description, or both."})
        return attrs
class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta: model = TeamMember; fields = "__all__"; read_only_fields = ("created_by", "updated_by")
class TestimonialSerializer(serializers.ModelSerializer):
    class Meta: model = Testimonial; fields = "__all__"; read_only_fields = ("created_by", "updated_by")
