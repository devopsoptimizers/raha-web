from django.db import models
from common.models import TimeStampedUUIDModel
from common.validators import validate_image

class Slider(TimeStampedUUIDModel):
    title = models.CharField(max_length=180)
    subtitle = models.CharField(max_length=300, blank=True)
    desktop_image = models.ImageField(upload_to="sliders/desktop/", validators=[validate_image])
    mobile_image = models.ImageField(upload_to="sliders/mobile/", blank=True, validators=[validate_image])
    button_label = models.CharField(max_length=80, blank=True)
    button_url = models.CharField(max_length=300, blank=True)
    video_url = models.URLField(blank=True)
    google_maps_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    class Meta: ordering = ["display_order"]

class ContentBlock(TimeStampedUUIDModel):
    class Type(models.TextChoices):
        ABOUT="ABOUT", "About"; ACHIEVEMENT="ACHIEVEMENT", "Achievement"; STATISTIC="STATISTIC", "Statistic"; PROMOTION="PROMOTION", "Promotion"; BUYER="BUYER", "Buyer"; LANDOWNER="LANDOWNER", "Landowner"; CTA="CTA", "Call to action"; HEADER="HEADER", "Header"; FOOTER="FOOTER", "Footer"; PRIVACY="PRIVACY", "Privacy policy"; TERMS="TERMS", "Terms and conditions"
    block_type = models.CharField(max_length=20, choices=Type.choices, db_index=True)
    key = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="content/", blank=True, validators=[validate_image])
    payload = models.JSONField(default=dict, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False, db_index=True)
    class Meta: ordering = ["block_type", "display_order"]

class Campaign(TimeStampedUUIDModel):
    title = models.CharField(max_length=180)
    body = models.TextField(max_length=600, blank=True)
    image = models.ImageField(upload_to="campaigns/", blank=True, validators=[validate_image])
    cta_label = models.CharField(max_length=80, blank=True)
    cta_url = models.CharField(max_length=300, blank=True)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-start_date"]

    def __str__(self):
        return self.title

class TeamMember(TimeStampedUUIDModel):
    full_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=120)
    department = models.CharField(max_length=120, blank=True)
    biography = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="team/", validators=[validate_image])
    email = models.EmailField(blank=True); phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["display_order", "full_name"]
