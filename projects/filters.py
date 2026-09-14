import django_filters
from .models import Project

class ProjectFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(field_name="area__name", lookup_expr="iexact")
    property_type = django_filters.CharFilter(field_name="property_type__name", lookup_expr="iexact")
    min_price = django_filters.NumberFilter(field_name="min_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="max_price", lookup_expr="lte")
    min_size = django_filters.NumberFilter(field_name="max_apartment_size", lookup_expr="gte")
    max_size = django_filters.NumberFilter(field_name="min_apartment_size", lookup_expr="lte")
    bedrooms = django_filters.NumberFilter(field_name="apartment_types__bedrooms")
    handover_before = django_filters.DateFilter(field_name="expected_handover_date", lookup_expr="lte")
    class Meta:
        model = Project
        fields = ("status", "property_type", "division", "district", "area", "location", "is_featured")
