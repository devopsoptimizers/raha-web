from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("inquiries", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="publicmessage",
            name="user_type",
            field=models.CharField(
                choices=[("CLIENT", "Client"), ("LANDOWNER", "Landowner")],
                db_index=True,
                default="CLIENT",
                max_length=20,
            ),
        ),
    ]
