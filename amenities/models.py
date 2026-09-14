from django.db import models
from common.models import TimeStampedUUIDModel
from common.validators import validate_image

class Amenity(TimeStampedUUIDModel):
    name = models.CharField(max_length=120, unique=True)
    icon = models.ImageField(upload_to="amenities/", blank=True, validators=[validate_image])
    description = models.CharField(max_length=300, blank=True)
    def __str__(self): return self.name
