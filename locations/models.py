from django.db import models
from common.models import TimeStampedUUIDModel

class Division(TimeStampedUUIDModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class District(TimeStampedUUIDModel):
    division = models.ForeignKey(Division, on_delete=models.PROTECT, related_name="districts")
    name = models.CharField(max_length=100)
    class Meta: constraints = [models.UniqueConstraint(fields=["division", "name"], name="unique_district_in_division")]
    def __str__(self): return self.name

class Area(TimeStampedUUIDModel):
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="areas")
    name = models.CharField(max_length=120)
    class Meta: constraints = [models.UniqueConstraint(fields=["district", "name"], name="unique_area_in_district")]
    def __str__(self): return self.name
