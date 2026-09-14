from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("settings_app", "0002_contact_page_content")]

    operations = [
        migrations.AddField(model_name="sitesettings", name="footer_explore_title", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="footer_contact_title", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="footer_copyright_text", field=models.CharField(blank=True, max_length=250)),
        migrations.AddField(model_name="sitesettings", name="footer_link_1_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="footer_link_1_url", field=models.CharField(blank=True, max_length=300)),
        migrations.AddField(model_name="sitesettings", name="footer_link_2_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="footer_link_2_url", field=models.CharField(blank=True, max_length=300)),
        migrations.AddField(model_name="sitesettings", name="footer_link_3_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="footer_link_3_url", field=models.CharField(blank=True, max_length=300)),
        migrations.AddField(model_name="sitesettings", name="footer_link_4_label", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="sitesettings", name="footer_link_4_url", field=models.CharField(blank=True, max_length=300)),
    ]
