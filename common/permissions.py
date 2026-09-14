from rest_framework.permissions import BasePermission, SAFE_METHODS

class RolePermission(BasePermission):
    roles = ()
    permission_key = ""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and getattr(view, "public_read", True):
            return True
        if not request.user.is_authenticated: return False
        if request.user.is_superuser or request.user.role == "SUPER_ADMIN": return True
        try:
            permissions = request.user.__class__._meta.apps.get_model("accounts", "RoleAccess").objects.get(role=request.user.role).permissions
            return "all" in permissions or self.permission_key in permissions
        except Exception:
            return request.user.role in self.roles

class IsContentAdmin(RolePermission):
    roles = ("SUPER_ADMIN", "CONTENT_ADMIN")
    permission_key = "content_management"
class IsProjectManager(RolePermission):
    roles = ("SUPER_ADMIN", "PROJECT_MANAGER")
    permission_key = "project_management"
class IsSalesOfficer(RolePermission):
    roles = ("SUPER_ADMIN", "SALES_OFFICER")
    permission_key = "sales_management"
class IsSupportOfficer(RolePermission):
    roles = ("SUPER_ADMIN", "SUPPORT_OFFICER")
    permission_key = "support_management"
