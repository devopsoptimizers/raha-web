import secrets
from django.db import models
from common.models import TimeStampedUUIDModel
class Subscriber(TimeStampedUUIDModel):
    email=models.EmailField(unique=True); is_verified=models.BooleanField(default=False,db_index=True); verification_token=models.CharField(max_length=64,unique=True,default=secrets.token_urlsafe); unsubscribed_at=models.DateTimeField(null=True,blank=True)

class NewsletterIssue(TimeStampedUUIDModel):
    title=models.CharField(max_length=180)
    issue_number=models.CharField(max_length=40)
    publication_date=models.DateField()
    cover_image=models.ImageField(upload_to="newsletter/covers/")
    pdf=models.FileField(upload_to="newsletter/issues/")
    display_order=models.PositiveIntegerField(default=0)
    class Meta: ordering=("display_order", "-publication_date")
    def __str__(self): return self.title
