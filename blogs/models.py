from django.db import models
from common.models import SoftDeleteModel, TimeStampedUUIDModel
from common.validators import validate_image

class BlogCategory(TimeStampedUUIDModel):
    name=models.CharField(max_length=100, unique=True); slug=models.SlugField(max_length=120, unique=True)
    def __str__(self): return self.name
class Tag(TimeStampedUUIDModel):
    name=models.CharField(max_length=60, unique=True); slug=models.SlugField(max_length=70, unique=True)
    def __str__(self): return self.name
class BlogPost(SoftDeleteModel):
    title=models.CharField(max_length=220); slug=models.SlugField(max_length=240, unique=True)
    excerpt=models.CharField(max_length=500); content=models.TextField()
    category=models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name="posts")
    tags=models.ManyToManyField(Tag, blank=True, related_name="posts")
    featured_image=models.ImageField(upload_to="blogs/", validators=[validate_image])
    author=models.ForeignKey("accounts.User", null=True, on_delete=models.SET_NULL, related_name="blog_posts")
    published_at=models.DateTimeField(null=True, blank=True, db_index=True)
    is_featured=models.BooleanField(default=False, db_index=True); is_published=models.BooleanField(default=False, db_index=True)
    seo_title=models.CharField(max_length=70, blank=True); seo_description=models.CharField(max_length=170, blank=True); seo_keywords=models.CharField(max_length=300, blank=True)
    class Meta: ordering=["-published_at", "-created_at"]
