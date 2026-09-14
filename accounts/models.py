import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Administrator"
        CONTENT_ADMIN = "CONTENT_ADMIN", "Content Administrator"
        PROJECT_MANAGER = "PROJECT_MANAGER", "Project Manager"
        SALES_OFFICER = "SALES_OFFICER", "Sales Officer"
        SUPPORT_OFFICER = "SUPPORT_OFFICER", "Customer Support Officer"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=Role.choices, db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class RoleAccess(models.Model):
    role = models.CharField(max_length=32, choices=User.Role.choices, unique=True)
    permissions = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.get_role_display()
