from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets=UserAdmin.fieldsets+(("Role and contact",{"fields":("role","phone")}),)
    add_fieldsets=UserAdmin.add_fieldsets+(("Role and contact",{"fields":("email","role","phone")}),)
    list_display=("email","username","role","is_active","last_login"); list_filter=("role","is_active","is_staff")
