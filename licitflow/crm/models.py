
from django.conf import settings
from django.db import models
from django.utils import timezone


class PipelineStage(models.Model):
    """Etapas del pipeline comercial (Detectada, En evaluación, Postulada, Adjudicada, Perdida)."""

    name = models.CharField(max_length=60, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Orden ascendente en el pipeline")
    probability = models.PositiveSmallIntegerField(
        default=0,
        help_text="Probabilidad estimada de éxito (0-100)",
    )
    is_won = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "Etapa de Pipeline"
        verbose_name_plural = "Etapas de Pipeline"

    def __str__(self) -> str:  # pragma: no cover
        status = " (ganada)" if self.is_won else (" (cerrada)" if self.is_closed else "")
        return f"{self.order}. {self.name}{status}"


CURRENCY_CHOICES = (
    ("CLP", "CLP"),
    ("UF", "UF"),
)


class CRMDeal(models.Model):
    """Negocio/Oportunidad vinculada a una licitación.

    Nota: si ya existe un modelo `oportunidades.Licitacion`, luego podemos
    cambiar `licitacion_external_id`/`licitacion_url` por una FK.
    """

    title = models.CharField(max_length=255)
    licitacion_external_id = models.CharField(
        max_length=64,
        blank=True,
        help_text="ID externo de la licitación (por ejemplo, código de Mercado Público)",
    )
    licitacion_url = models.URLField(blank=True)

    organization = models.ForeignKey(
        "core.Organization", on_delete=models.SET_NULL, null=True, blank=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="owned_deals",
    )
    stage = models.ForeignKey(PipelineStage, on_delete=models.PROTECT, related_name="deals")

    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="CLP")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "-id")
        indexes = [
            models.Index(fields=["licitacion_external_id"]),
            models.Index(fields=["stage", "updated_at"]),
        ]
        verbose_name = "Negocio (Deal)"
        verbose_name_plural = "Negocios (Deals)"

    def __str__(self) -> str:  # pragma: no cover
        return self.title


ROLE_CHOICES = (
    ("OWNER", "Owner"),
    ("COLLAB", "Colaborador"),
)


class CRMParticipant(models.Model):
    """Participantes del negocio con roles (propietario/colaborador)."""

    deal = models.ForeignKey(CRMDeal, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="COLLAB")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("deal", "user")
        verbose_name = "Participante de Deal"
        verbose_name_plural = "Participantes de Deal"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user} → {self.deal} ({self.role})"


TASK_STATUS = (
    ("todo", "Por hacer"),
    ("doing", "En progreso"),
    ("done", "Terminada"),
)


class CRMTask(models.Model):
    """Tareas asociadas a un negocio (seguimientos, llamadas, entrega docs, etc.)."""

    deal = models.ForeignKey(CRMDeal, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=TASK_STATUS, default="todo")

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="assigned_crm_tasks",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="created_crm_tasks",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("status", "due_at", "-created_at")
        verbose_name = "Tarea CRM"
        verbose_name_plural = "Tareas CRM"

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class CRMNote(models.Model):
    """Notas libres por negocio (minutas, acuerdos, contexto)."""

    deal = models.ForeignKey(CRMDeal, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Nota CRM"
        verbose_name_plural = "Notas CRM"

    def __str__(self) -> str:  # pragma: no cover
        return f"Nota de {self.author} en {self.deal}"
