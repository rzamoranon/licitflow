from django.contrib import admin
from .models import Organization, UserProfile

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "plan", "active", "created_at")
    search_fields = ("name", "rut", "website")
    list_filter = ("active", "plan")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "org", "role", "status", "created_at")
    search_fields = ("user__username", "user__email", "org__name")
    list_filter = ("role", "status", "org")
