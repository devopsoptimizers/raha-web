from rest_framework import serializers
from .models import Area, District, Division

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by")

class DistrictSerializer(serializers.ModelSerializer):
    division_name = serializers.CharField(source="division.name", read_only=True)
    class Meta:
        model = District
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by")

class AreaSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source="district.name", read_only=True)
    division = serializers.UUIDField(source="district.division_id", read_only=True)
    class Meta:
        model = Area
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by")
