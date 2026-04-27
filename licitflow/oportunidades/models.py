from django.db import models

class Tender(models.Model):
    STATUS_CHOICES = (
        ("detectada", "Detectada"),
        ("evaluacion", "En evaluación"),
        ("postulada", "Postulada"),
        ("adjudicada", "Adjudicada"),
        ("perdida", "Perdida"),
        ("cerrada", "Cerrada"),
    )

    org = models.ForeignKey("core.Organization", on_delete=models.CASCADE, related_name="tenders")
    owner = models.ForeignKey("core.UserProfile", null=True, blank=True, on_delete=models.SET_NULL, related_name="owned_tenders")

    title = models.CharField(max_length=255)
    external_id = models.CharField(max_length=100, blank=True)
    organism = models.CharField(max_length=200, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    closes_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="detectada")
    amount_estimated = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=120, blank=True)
    url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("org", "external_id")]

    def __str__(self):
        return self.title
