from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("projects", "0003_project_property_type_relation")]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="latitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=8,
                max_digits=10,
                null=True,
                validators=[MinValueValidator(-90), MaxValueValidator(90)],
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="longitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=8,
                max_digits=11,
                null=True,
                validators=[MinValueValidator(-180), MaxValueValidator(180)],
            ),
        ),
    ]
