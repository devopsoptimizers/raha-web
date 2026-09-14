from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from common.models import TimeStampedUUIDModel
from common.validators import validate_image

class Testimonial(TimeStampedUUIDModel):
    customer_name = models.CharField(max_length=150)
    customer_type = models.CharField(max_length=80, blank=True)
    project = models.ForeignKey("projects.Project", null=True, blank=True, on_delete=models.SET_NULL, related_name="testimonials")
    title = models.CharField(max_length=180, blank=True)
    description = models.TextField()
    customer_image = models.ImageField(upload_to="testimonials/", blank=True, validators=[validate_image])
    video_url = models.URLField(blank=True)
    video_thumbnail = models.ImageField(upload_to="testimonials/thumbnails/", blank=True, validators=[validate_image])
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_featured = models.BooleanField(default=False, db_index=True)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False, db_index=True)
    class Meta: ordering = ["display_order", "-created_at"]
