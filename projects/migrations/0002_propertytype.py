import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.text import slugify


def seed_property_types(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    PropertyType = apps.get_model("projects", "PropertyType")
    for name in Project.objects.exclude(property_type="").values_list("property_type", flat=True).distinct():
        base = slugify(name)[:60] or "property-type"
        slug = base
        number = 2
        while PropertyType.objects.filter(slug=slug).exists():
            slug = f"{base[:55]}-{number}"
            number += 1
        PropertyType.objects.get_or_create(name=name, defaults={"slug": slug})


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="PropertyType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=60, unique=True)),
                ("slug", models.SlugField(max_length=70, unique=True)),
                ("description", models.CharField(blank=True, max_length=300)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(app_label)s_%(class)s_set", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(app_label)s_%(class)s_set", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.RunPython(seed_property_types, migrations.RunPython.noop),
    ]
