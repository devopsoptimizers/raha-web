from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("content", "0001_initial")]
    operations = [
        migrations.AddField(model_name="slider", name="video_url", field=models.URLField(blank=True)),
        migrations.AddField(model_name="slider", name="google_maps_url", field=models.URLField(blank=True)),
    ]
