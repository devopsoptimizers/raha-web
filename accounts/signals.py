from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from .models import User

ROLE_APP_LABELS={
    User.Role.CONTENT_ADMIN:{"content","blogs","testimonials","settings_app","media_gallery"},
    User.Role.PROJECT_MANAGER:{"projects","properties","locations","amenities","media_gallery"},
    User.Role.SALES_OFFICER:{"inquiries","landowners"},
    User.Role.SUPPORT_OFFICER:{"inquiries"},
}
@receiver(post_migrate)
def ensure_role_groups(**kwargs):
    for role,labels in ROLE_APP_LABELS.items():
        group,_=Group.objects.get_or_create(name=role); group.permissions.set(Permission.objects.filter(content_type__app_label__in=labels))
@receiver(post_save,sender=User)
def synchronize_user_group(sender,instance,**kwargs):
    if instance.role:
        group,_=Group.objects.get_or_create(name=instance.role); instance.groups.set([group])
