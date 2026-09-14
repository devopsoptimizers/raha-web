from django.db import migrations, models
import django.db.models.deletion


def connect_property_types(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    PropertyType = apps.get_model("projects", "PropertyType")
    for project in Project.objects.all().iterator():
        name = project.property_type.strip() or "Unspecified"
        property_type = PropertyType.objects.filter(name__iexact=name).first()
        if not property_type:
            from django.utils.text import slugify
            base = slugify(name)[:60] or "unspecified"
            slug = base
            suffix = 2
            while PropertyType.objects.filter(slug=slug).exists():
                slug = f"{base[:55]}-{suffix}"
                suffix += 1
            property_type = PropertyType.objects.create(name=name, slug=slug)
        project.property_type_relation = property_type
        project.save(update_fields=["property_type_relation"])


class Migration(migrations.Migration):
    atomic = False
    dependencies = [("projects", "0002_propertytype")]
    operations = [
        migrations.AddField(
            model_name="project",
            name="property_type_relation",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="migrating_projects", to="projects.propertytype"),
        ),
        migrations.RunPython(connect_property_types, migrations.RunPython.noop),
        migrations.RemoveIndex(model_name="project", name="projects_pr_area_id_6d0089_idx"),
        migrations.RemoveField(model_name="project", name="property_type"),
        migrations.RenameField(model_name="project", old_name="property_type_relation", new_name="property_type"),
        migrations.AlterField(
            model_name="project",
            name="property_type",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="projects", to="projects.propertytype"),
        ),
        migrations.AddIndex(model_name="project", index=models.Index(fields=["area", "property_type"], name="projects_pr_area_pt_idx")),
    ]
