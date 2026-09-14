from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Project
@receiver([post_save,post_delete],sender=Project)
def invalidate_project_cache(**kwargs):
    cache.delete("home:v1")
    cache.set("project-list-version",timezone.now().timestamp(),None)
@receiver(m2m_changed,sender=Project.amenities.through)
def invalidate_project_amenities(**kwargs): invalidate_project_cache()
