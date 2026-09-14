from django.db import migrations, models

def seed_roles(apps, schema_editor):
    RoleAccess = apps.get_model("accounts", "RoleAccess")
    defaults = {
        "SUPER_ADMIN": ["all"],
        "CONTENT_ADMIN": ["content_management"],
        "PROJECT_MANAGER": ["project_management"],
        "SALES_OFFICER": ["sales_management"],
        "SUPPORT_OFFICER": ["support_management"],
    }
    for role, permissions in defaults.items(): RoleAccess.objects.create(role=role, permissions=permissions)

class Migration(migrations.Migration):
    dependencies = [("accounts", "0001_initial")]
    operations = [
        migrations.CreateModel(name="RoleAccess", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("role", models.CharField(choices=[("SUPER_ADMIN", "Super Administrator"), ("CONTENT_ADMIN", "Content Administrator"), ("PROJECT_MANAGER", "Project Manager"), ("SALES_OFFICER", "Sales Officer"), ("SUPPORT_OFFICER", "Customer Support Officer")], max_length=32, unique=True)), ("permissions", models.JSONField(blank=True, default=list)), ("updated_at", models.DateTimeField(auto_now=True))]),
        migrations.RunPython(seed_roles, migrations.RunPython.noop),
    ]
