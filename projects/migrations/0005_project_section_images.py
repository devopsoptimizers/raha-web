from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("projects", "0004_expand_coordinate_precision")]

    operations = [
        migrations.AddField(
            model_name="project",
            name="features_image",
            field=models.ImageField(blank=True, upload_to="projects/features/"),
        ),
        migrations.AddField(
            model_name="project",
            name="inquiry_image",
            field=models.ImageField(blank=True, upload_to="projects/inquiries/"),
        ),
    ]
