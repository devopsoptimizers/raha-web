from django.db import models
from common.models import SoftDeleteModel, TimeStampedUUIDModel
from common.validators import validate_image

class ApartmentType(TimeStampedUUIDModel):
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="apartment_types")
    name = models.CharField(max_length=100)
    size_sqft = models.PositiveIntegerField(db_index=True)
    bedrooms = models.PositiveSmallIntegerField(db_index=True)
    bathrooms = models.PositiveSmallIntegerField()
    balconies = models.PositiveSmallIntegerField(default=0)
    has_drawing_room = models.BooleanField(default=True)
    has_dining_room = models.BooleanField(default=True)
    has_kitchen = models.BooleanField(default=True)
    has_servant_room = models.BooleanField(default=False)
    parking_allocation = models.PositiveSmallIntegerField(default=0)
    facing = models.CharField(max_length=50, blank=True)
    floor_plan = models.ImageField(upload_to="floor_plans/", blank=True, validators=[validate_image])
    starting_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    class Meta: constraints = [models.UniqueConstraint(fields=["project", "name"], name="unique_apartment_type_project")]

class Unit(SoftDeleteModel):
    class Availability(models.TextChoices):
        AVAILABLE="AVAILABLE", "Available"; RESERVED="RESERVED", "Reserved"; BOOKED="BOOKED", "Booked"; SOLD="SOLD", "Sold"; UNAVAILABLE="UNAVAILABLE", "Unavailable"
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="units")
    apartment_type = models.ForeignKey(ApartmentType, on_delete=models.PROTECT, related_name="units")
    building = models.CharField(max_length=50)
    floor_number = models.IntegerField()
    unit_number = models.CharField(max_length=30)
    size_sqft = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    booking_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    availability = models.CharField(max_length=20, choices=Availability.choices, default=Availability.AVAILABLE, db_index=True)
    parking_number = models.CharField(max_length=50, blank=True)
    handover_status = models.CharField(max_length=50, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["project", "building", "floor_number", "unit_number"], name="unique_project_building_floor_unit")]
        indexes = [models.Index(fields=["project", "availability"])]
