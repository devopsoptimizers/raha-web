from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("settings_app", "0003_footer_content")]

    operations = [
        migrations.AddField(model_name="sitesettings", name="contact_map_button_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="contact_name_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="contact_phone_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="contact_email_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="contact_user_type_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="contact_client_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="contact_landowner_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="contact_message_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="contact_submit_label", field=models.CharField(blank=True, max_length=80)),
    ]
