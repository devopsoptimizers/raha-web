from django.conf import settings
from django.db import models
from common.models import TimeStampedUUIDModel
from common.validators import validate_bd_phone

class Inquiry(TimeStampedUUIDModel):
    class Status(models.TextChoices): NEW="NEW","New"; CONTACTED="CONTACTED","Contacted"; QUALIFIED="QUALIFIED","Qualified"; SITE_VISIT="SITE_VISIT","Site Visit Scheduled"; NEGOTIATION="NEGOTIATION","Negotiation"; CONVERTED="CONVERTED","Converted"; LOST="LOST","Lost"; CLOSED="CLOSED","Closed"
    full_name=models.CharField(max_length=150); phone=models.CharField(max_length=20,validators=[validate_bd_phone]); email=models.EmailField(blank=True); project=models.ForeignKey("projects.Project",null=True,blank=True,on_delete=models.SET_NULL,related_name="inquiries"); apartment_type=models.ForeignKey("properties.ApartmentType",null=True,blank=True,on_delete=models.SET_NULL,related_name="inquiries"); preferred_location=models.CharField(max_length=150,blank=True); expected_budget=models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True); preferred_contact_method=models.CharField(max_length=30,default="PHONE"); message=models.TextField(blank=True); lead_source=models.CharField(max_length=80,blank=True); assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="assigned_inquiries"); status=models.CharField(max_length=20,choices=Status.choices,default=Status.NEW,db_index=True); follow_up_date=models.DateTimeField(null=True,blank=True,db_index=True); internal_notes=models.TextField(blank=True)
class InquiryNote(TimeStampedUUIDModel):
    inquiry=models.ForeignKey(Inquiry,on_delete=models.CASCADE,related_name="notes"); body=models.TextField()
class MeetingRequest(TimeStampedUUIDModel):
    class Status(models.TextChoices): PENDING="PENDING","Pending"; CONFIRMED="CONFIRMED","Confirmed"; COMPLETED="COMPLETED","Completed"; CANCELLED="CANCELLED","Cancelled"
    customer_name=models.CharField(max_length=150); phone=models.CharField(max_length=20,validators=[validate_bd_phone]); email=models.EmailField(blank=True); project=models.ForeignKey("projects.Project",null=True,blank=True,on_delete=models.SET_NULL,related_name="meetings"); meeting_type=models.CharField(max_length=50); preferred_date=models.DateField(); preferred_time=models.TimeField(); message=models.TextField(blank=True); assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="assigned_meetings"); status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING,db_index=True)
class PublicMessage(TimeStampedUUIDModel):
    class Kind(models.TextChoices): CONTACT="CONTACT","Contact"; FEEDBACK="FEEDBACK","Feedback"; SUGGESTION="SUGGESTION","Suggestion"
    class UserType(models.TextChoices): CLIENT="CLIENT","Client"; LANDOWNER="LANDOWNER","Landowner"
    kind=models.CharField(max_length=20,choices=Kind.choices,db_index=True); user_type=models.CharField(max_length=20,choices=UserType.choices,default=UserType.CLIENT,db_index=True); full_name=models.CharField(max_length=150); phone=models.CharField(max_length=20,blank=True,validators=[validate_bd_phone]); email=models.EmailField(blank=True); subject=models.CharField(max_length=180,blank=True); message=models.TextField(); is_resolved=models.BooleanField(default=False,db_index=True)
