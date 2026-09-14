from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("projects", "0005_project_section_images")]

    operations = [
        migrations.AddField(
            model_name="project",
            name="features_label",
            field=models.CharField(default="Features", max_length=80),
        ),
        migrations.AddField(
            model_name="project",
            name="features_title",
            field=models.CharField(default="What You Get", max_length=160),
        ),
        migrations.AddField(
            model_name="project",
            name="inquiry_title",
            field=models.CharField(default="Ask About the property", max_length=160),
        ),
        migrations.AddField(
            model_name="project",
            name="inquiry_description",
            field=models.TextField(blank=True),
        ),
    ]
