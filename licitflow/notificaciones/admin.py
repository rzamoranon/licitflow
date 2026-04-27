from django.contrib import admin
from .models import (
    NotificationTemplate,
    NotificationPreference,
    Notification,
    DeliveryLog,
)

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "channel", "is_active", "created_at")
    list_filter = ("channel", "is_active")
    search_fields = ("name", "subject")

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "email_enabled",
        "whatsapp_enabled",
        "inapp_enabled",
        "digest_daily",
        "digest_weekly",
        "updated_at",
    )
    search_fields = ("user__username", "user__email")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "channel", "status", "title", "created_at", "sent_at", "read_at")
    list_filter = ("channel", "status", "created_at")
    search_fields = ("title", "message", "user__username", "to_email", "to_phone")
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "queued_at", "sent_at", "read_at")

@admin.register(DeliveryLog)
class DeliveryLogAdmin(admin.ModelAdmin):
    list_display = ("notification", "attempt", "provider", "success", "response_code", "created_at")
    list_filter = ("provider", "success")
    search_fields = ("response_message",)
