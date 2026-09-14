from django.conf import settings
from django.db import models
from common.models import TimeStampedUUIDModel
class AuditLog(TimeStampedUUIDModel):
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,related_name="audit_events"); method=models.CharField(max_length=10); path=models.CharField(max_length=500,db_index=True); status_code=models.PositiveSmallIntegerField(); ip_address=models.GenericIPAddressField(null=True); user_agent=models.CharField(max_length=500,blank=True); metadata=models.JSONField(default=dict,blank=True)
    class Meta: ordering=["-created_at"]; indexes=[models.Index(fields=["actor","created_at"])]
