import uuid
from django.conf import settings
from django.db import models

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class TimeStampedUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_%(app_label)s_%(class)s_set")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="updated_%(app_label)s_%(class)s_set")

    class Meta:
        abstract = True

class SoftDeleteModel(TimeStampedUUIDModel):
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    objects = ActiveManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save(update_fields=["deleted_at", "is_active", "updated_at"])

    class Meta:
        abstract = True
