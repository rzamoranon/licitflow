from django.db import models

class SavedSearch(models.Model):
    class Visibility(models.TextChoices):
        PRIVATE = "private", "Privada"
        TEAM = "team", "Equipo"
        ORG = "org", "Organización"

    org = models.ForeignKey("core.Organization", on_delete=models.CASCADE, related_name="saved_searches")
    owner = models.ForeignKey("core.UserProfile", on_delete=models.CASCADE, related_name="saved_searches")
    name = models.CharField(max_length=120)
    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.PRIVATE)
    filters = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("owner", "name")]

class Alert(models.Model):
    saved_search = models.ForeignKey(SavedSearch, on_delete=models.CASCADE, related_name="alerts")
    frequency = models.CharField(max_length=20, default="daily")
    channels = models.JSONField(default=list)
    active = models.BooleanField(default=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)

class SearchLog(models.Model):
    org = models.ForeignKey("core.Organization", on_delete=models.CASCADE, related_name="search_logs")
    user = models.ForeignKey("core.UserProfile", null=True, on_delete=models.SET_NULL, related_name="search_logs")
    filters = models.JSONField()
    total = models.IntegerField()
    took_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
