from django.conf import settings
from django.db import models
from common.models import TimeStampedUUIDModel
from common.validators import validate_bd_phone, validate_upload

def validate_document(value): validate_upload(value,extensions={"pdf","jpg","jpeg","png"},max_mb=10)
class LandownerProposal(TimeStampedUUIDModel):
    class Status(models.TextChoices): NEW="NEW","New"; REVIEWING="REVIEWING","Reviewing"; CONTACTED="CONTACTED","Contacted"; APPROVED="APPROVED","Approved"; REJECTED="REJECTED","Rejected"; CLOSED="CLOSED","Closed"
    owner_name=models.CharField(max_length=150); phone=models.CharField(max_length=20,validators=[validate_bd_phone]); email=models.EmailField(blank=True); land_address=models.TextField(); division=models.ForeignKey("locations.Division",on_delete=models.PROTECT); district=models.ForeignKey("locations.District",on_delete=models.PROTECT); area=models.ForeignKey("locations.Area",on_delete=models.PROTECT); land_size=models.DecimalField(max_digits=12,decimal_places=2); road_width=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True); ownership_type=models.CharField(max_length=80); number_of_owners=models.PositiveSmallIntegerField(default=1); google_maps_url=models.URLField(blank=True); latitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True); longitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True); message=models.TextField(blank=True); assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="landowner_proposals"); status=models.CharField(max_length=20,choices=Status.choices,default=Status.NEW,db_index=True); internal_notes=models.TextField(blank=True)
class ProposalDocument(TimeStampedUUIDModel):
    proposal=models.ForeignKey(LandownerProposal,on_delete=models.CASCADE,related_name="documents"); file=models.FileField(upload_to="landowners/",validators=[validate_document]); label=models.CharField(max_length=100,blank=True)
