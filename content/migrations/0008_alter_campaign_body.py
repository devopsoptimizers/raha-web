from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("content", "0007_alter_campaign_image")]
    operations = [migrations.AlterField(model_name="campaign", name="body", field=models.TextField(blank=True, max_length=600))]
