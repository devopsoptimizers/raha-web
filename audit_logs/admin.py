from django.contrib import admin
from .models import AuditLog
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display=("created_at","actor","method","path","status_code"); list_filter=("method","status_code"); search_fields=("path","actor__email"); readonly_fields=[f.name for f in AuditLog._meta.fields]
    def has_add_permission(self,request): return False
    def has_delete_permission(self,request,obj=None): return False
