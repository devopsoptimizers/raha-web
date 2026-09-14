from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("careers", "0001_initial")]

    operations = [
        migrations.AddField(model_name="jobapplication", name="years_of_experience", field=models.CharField(default="", max_length=100), preserve_default=False),
        migrations.AddField(model_name="jobapplication", name="previous_organization", field=models.CharField(default="", max_length=180), preserve_default=False),
        migrations.AddField(model_name="jobapplication", name="education_degree", field=models.CharField(default="", max_length=180), preserve_default=False),
        migrations.AddField(model_name="jobapplication", name="education_institution", field=models.CharField(default="", max_length=220), preserve_default=False),
        migrations.AlterField(model_name="jobapplication", name="cover_letter", field=models.TextField()),
    ]
