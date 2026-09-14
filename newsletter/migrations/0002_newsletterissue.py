import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies=[("newsletter","0001_initial")]
    operations=[migrations.CreateModel(name="NewsletterIssue",fields=[
        ("id",models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),
        ("is_active",models.BooleanField(db_index=True,default=True)),
        ("created_at",models.DateTimeField(auto_now_add=True,db_index=True)),
        ("updated_at",models.DateTimeField(auto_now=True)),
        ("title",models.CharField(max_length=180)),
        ("issue_number",models.CharField(max_length=40)),
        ("publication_date",models.DateField()),
        ("cover_image",models.ImageField(upload_to="newsletter/covers/")),
        ("pdf",models.FileField(upload_to="newsletter/issues/")),
        ("display_order",models.PositiveIntegerField(default=0)),
        ("created_by",models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name="created_newsletter_newsletterissue_set",to=settings.AUTH_USER_MODEL)),
        ("updated_by",models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name="updated_newsletter_newsletterissue_set",to=settings.AUTH_USER_MODEL)),
    ],options={"ordering":("display_order","-publication_date")})]
