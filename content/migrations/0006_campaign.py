import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import common.validators


class Migration(migrations.Migration):
    dependencies = [("content", "0005_homepage_sections"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="Campaign", fields=[
        ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
        ("is_active", models.BooleanField(db_index=True, default=True)),
        ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
        ("updated_at", models.DateTimeField(auto_now=True)),
        ("title", models.CharField(max_length=180)),
        ("body", models.TextField(max_length=600)),
        ("image", models.ImageField(upload_to="campaigns/", validators=[common.validators.validate_image])),
        ("cta_label", models.CharField(blank=True, max_length=80)),
        ("cta_url", models.CharField(blank=True, max_length=300)),
        ("start_date", models.DateTimeField(db_index=True)),
        ("end_date", models.DateTimeField(db_index=True)),
        ("display_order", models.PositiveIntegerField(default=0)),
        ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(app_label)s_%(class)s_set", to=settings.AUTH_USER_MODEL)),
        ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(app_label)s_%(class)s_set", to=settings.AUTH_USER_MODEL)),
    ], options={"ordering": ["display_order", "-start_date"]})]
