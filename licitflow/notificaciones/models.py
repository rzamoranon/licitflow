from django.conf import settings
from django.db import models
from django.utils import timezone

# Canales soportados
CHANNEL_CHOICES = (
    ("email", "Email"),
    ("whatsapp", "WhatsApp"),
    ("inapp", "In-App"),
)

# Estados de notificación
STATUS_CHOICES = (
    ("queued", "En cola"),
    ("sent", "Enviada"),
    ("failed", "Fallida"),
    ("read", "Leída"),
)

class NotificationTemplate(models.Model):
    """
    Plantillas reutilizables por canal. Permiten variables tipo {{variable}}.
    Ej: asunto/cuerpo para email; cuerpo para WhatsApp; título/mensaje para in-app.
    """
    name = models.CharField(max_length=120, unique=True)
    channel = models.CharField(max_length=16, choices=CHANNEL_CHOICES)
    subject = models.CharField(max_length=200, blank=True)  # Email/in-app
    body = models.TextField()  # Soporta placeholders
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        unique_together = [("name", "channel")]

    def __str__(self):
        return f"{self.name} [{self.channel}]"


class NotificationPreference(models.Model):
    """
    Preferencias por usuario para canales y ventanas horarias (quiet hours).
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notify_pref")
    email_enabled = models.BooleanField(default=True)
    whatsapp_enabled = models.BooleanField(default=False)
    inapp_enabled = models.BooleanField(default=True)

    # Ventana de silencio (opcional): 0-23 horas locales del usuario
    quiet_hours_start = models.PositiveSmallIntegerField(default=22)  # 22:00
    quiet_hours_end = models.PositiveSmallIntegerField(default=7)     # 07:00

    # Frecuencia de resumen por email (para alertas masivas)
    digest_daily = models.BooleanField(default=True)
    digest_weekly = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quiet_hours_start__gte=0, quiet_hours_start__lte=23),
                name="quiet_hours_start_0_23",
            ),
            models.CheckConstraint(
                check=models.Q(quiet_hours_end__gte=0, quiet_hours_end__lte=23),
                name="quiet_hours_end_0_23",
            ),
        ]

    def __str__(self):
        return f"Prefs {self.user.username}"


class Notification(models.Model):
    """
    Notificación concreta a un usuario. Puede estar vinculada a una organización y a un recurso (generic link).
    """
    org = models.ForeignKey("core.Organization", on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")

    channel = models.CharField(max_length=16, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="queued")

    # Contenido
    title = models.CharField(max_length=200, blank=True)   # para in-app/email subject
    message = models.TextField()                            # cuerpo renderizado
    link_url = models.URLField(blank=True)                  # CTA opcional

    # Direccionamiento específico por canal (override de preferencias o donde enviar)
    to_email = models.EmailField(blank=True)
    to_phone = models.CharField(max_length=40, blank=True)  # para WhatsApp (E.164)

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    queued_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    # Metadatos para trazabilidad (por ejemplo, licitación u oportunidad relacionada)
    related_app = models.CharField(max_length=60, blank=True)   # e.g., "oportunidades"
    related_model = models.CharField(max_length=60, blank=True) # e.g., "Licitacion"
    related_object_id = models.CharField(max_length=64, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["channel", "status"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def mark_sent(self):
        self.status = "sent"
        self.sent_at = timezone.now()
        self.save(update_fields=["status", "sent_at"])

    def mark_failed(self, error: str):
        self.status = "failed"
        self.error_message = (error or "")[:500]
        self.save(update_fields=["status", "error_message"])

    def mark_read(self):
        self.status = "read"
        self.read_at = timezone.now()
        self.save(update_fields=["status", "read_at"])

    def __str__(self):
        return f"[{self.get_channel_display()}] {self.title or self.message[:40]} → {self.user.username}"


class DeliveryLog(models.Model):
    """
    Log detallado por intento de entrega (útil para debug y auditoría).
    """
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="delivery_logs")
    attempt = models.PositiveIntegerField(default=1)
    provider = models.CharField(max_length=60, blank=True)   # ej: "smtp", "twilio", "whatsapp_api"
    payload_snapshot = models.JSONField(default=dict, blank=True)
    success = models.BooleanField(default=False)
    response_code = models.CharField(max_length=60, blank=True)
    response_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        ok = "OK" if self.success else "ERR"
        return f"Delivery {ok} n#{self.notification_id} try:{self.attempt}"
