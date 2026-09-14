from django.db import migrations, models
import common.validators


class Migration(migrations.Migration):
    dependencies = [("content", "0006_campaign")]
    operations = [migrations.AlterField(model_name="campaign", name="image", field=models.ImageField(blank=True, upload_to="campaigns/", validators=[common.validators.validate_image]))]
