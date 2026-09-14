from django.db import migrations, models
import common.validators


class Migration(migrations.Migration):
    dependencies = [("testimonials", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="testimonial",
            name="video_thumbnail",
            field=models.ImageField(blank=True, upload_to="testimonials/thumbnails/", validators=[common.validators.validate_image]),
        ),
    ]
