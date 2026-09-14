from django.db import models
from common.models import TimeStampedUUIDModel
from common.validators import validate_image

class GalleryItem(TimeStampedUUIDModel):
    class Kind(models.TextChoices):
        EXTERIOR="EXTERIOR", "Exterior"; INTERIOR="INTERIOR", "Interior"; CONSTRUCTION="CONSTRUCTION", "Construction"; ARCHITECTURAL="ARCHITECTURAL", "Architectural"; FLOOR_PLAN="FLOOR_PLAN", "Floor plan"; VIDEO="VIDEO", "Video"; VIRTUAL_TOUR="VIRTUAL_TOUR", "Virtual tour"
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="gallery_items")
    kind = models.CharField(max_length=20, choices=Kind.choices, db_index=True)
    image = models.ImageField(upload_to="gallery/", blank=True, validators=[validate_image])
    url = models.URLField(blank=True)
    caption = models.CharField(max_length=250, blank=True)
    alt_text = models.CharField(max_length=180, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["display_order", "created_at"]

class ProgressImage(TimeStampedUUIDModel):
    progress = models.ForeignKey("projects.ConstructionProgress", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="progress/", validators=[validate_image])
    alt_text = models.CharField(max_length=180, blank=True)
