from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("settings_app", "0001_initial")]

    operations = [
        migrations.AddField(model_name="sitesettings", name="contact_hero_label", field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name="sitesettings", name="contact_hero_title", field=models.CharField(blank=True, max_length=160)),
        migrations.AddField(model_name="sitesettings", name="contact_hero_image", field=models.ImageField(blank=True, upload_to="settings/contact/")),
        migrations.AddField(model_name="sitesettings", name="contact_details_label", field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name="sitesettings", name="contact_details_title", field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name="sitesettings", name="contact_form_label", field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name="sitesettings", name="contact_form_title", field=models.CharField(blank=True, max_length=160)),
        migrations.AddField(model_name="sitesettings", name="contact_image_label", field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name="sitesettings", name="contact_image_title", field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name="sitesettings", name="contact_form_image", field=models.ImageField(blank=True, upload_to="settings/contact/")),
        migrations.AddField(model_name="sitesettings", name="contact_map_embed_url", field=models.URLField(blank=True)),
    ]
