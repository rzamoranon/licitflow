from django.db import models
from django.conf import settings

ROLE_CHOICES = (
    ("APP_ADMIN", "App Admin"),
    ("ORG_ADMIN", "Org Admin"),
    ("ORG_USER", "Org User"),
)

STATUS_CHOICES = (
    ("active", "Activo"),
    ("invited", "Invitado"),
    ("suspended", "Suspendido"),
)

class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    rut = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="owned_org"
    )
    plan = models.CharField(max_length=30, default="free")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, related_name="members")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="ORG_USER")
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="direct_reports"
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="active")
    phone = models.CharField(max_length=30, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_org_admin(self):
        return self.role == "ORG_ADMIN"

    def __str__(self):
        return f"{self.user.username} ({self.role})"
