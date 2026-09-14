from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from common.models import SoftDeleteModel, TimeStampedUUIDModel
from common.validators import validate_image, validate_pdf

class PropertyType(TimeStampedUUIDModel):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True)
    description = models.CharField(max_length=300, blank=True)
    class Meta: ordering = ["name"]
    def __str__(self): return self.name

class Project(SoftDeleteModel):
    class Status(models.TextChoices):
        UPCOMING = "UPCOMING", "Upcoming"
        ONGOING = "ONGOING", "Ongoing"
        READY = "READY", "Ready"
        HANDED_OVER = "HANDED_OVER", "Handed Over"
    class Publication(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    code = models.CharField(max_length=50, unique=True)
    short_description = models.CharField(max_length=500)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, db_index=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name="projects")
    division = models.ForeignKey("locations.Division", on_delete=models.PROTECT, related_name="projects")
    district = models.ForeignKey("locations.District", on_delete=models.PROTECT, related_name="projects")
    area = models.ForeignKey("locations.Area", on_delete=models.PROTECT, related_name="projects")
    address = models.TextField()
    google_maps_url = models.URLField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    land_size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    road_width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    buildings = models.PositiveSmallIntegerField(default=1)
    floors = models.PositiveSmallIntegerField(default=1)
    basements = models.PositiveSmallIntegerField(default=0)
    apartment_count = models.PositiveIntegerField(default=0)
    apartments_per_floor = models.PositiveSmallIntegerField(default=0)
    min_apartment_size = models.PositiveIntegerField(null=True, blank=True)
    max_apartment_size = models.PositiveIntegerField(null=True, blank=True)
    min_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default="BDT")
    construction_start_date = models.DateField(null=True, blank=True)
    expected_handover_date = models.DateField(null=True, blank=True, db_index=True)
    actual_handover_date = models.DateField(null=True, blank=True)
    featured_image = models.ImageField(upload_to="projects/featured/", validators=[validate_image])
    hero_banner = models.ImageField(upload_to="projects/heroes/", blank=True, validators=[validate_image])
    features_label = models.CharField(max_length=80, default="Features")
    features_title = models.CharField(max_length=160, default="What You Get")
    features_image = models.ImageField(upload_to="projects/features/", blank=True, validators=[validate_image])
    inquiry_title = models.CharField(max_length=160, default="Ask About the property")
    inquiry_description = models.TextField(blank=True)
    inquiry_image = models.ImageField(upload_to="projects/inquiries/", blank=True, validators=[validate_image])
    brochure = models.FileField(upload_to="projects/brochures/", blank=True, validators=[validate_pdf])
    video_url = models.URLField(blank=True)
    virtual_tour_url = models.URLField(blank=True)
    amenities = models.ManyToManyField("amenities.Amenity", blank=True, related_name="projects")
    is_featured = models.BooleanField(default=False, db_index=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)
    publication_status = models.CharField(max_length=20, choices=Publication.choices, default=Publication.DRAFT, db_index=True)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=170, blank=True)
    seo_keywords = models.CharField(max_length=300, blank=True)
    class Meta:
        ordering = ["display_order", "-created_at"]
        indexes = [models.Index(fields=["status", "publication_status"]), models.Index(fields=["area", "property_type"], name="projects_pr_area_pt_idx")]
        constraints = [models.CheckConstraint(condition=models.Q(min_price__isnull=True) | models.Q(max_price__isnull=True) | models.Q(min_price__lte=models.F("max_price")), name="project_price_range_valid")]
    def __str__(self): return self.name

class ConstructionProgress(TimeStampedUUIDModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="progress_updates")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completion_percentage = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    progress_date = models.DateField(db_index=True)
    video_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=False, db_index=True)
    class Meta: ordering = ["-progress_date"]
