from django.db import models

class Document(models.Model):
    org = models.ForeignKey("core.Organization", on_delete=models.CASCADE, related_name="documents")
    owner = models.ForeignKey("core.UserProfile", on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="docs/%Y/%m/")
    version = models.PositiveIntegerField(default=1)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} v{self.version}"

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="versions")
    file = models.FileField(upload_to="docs/%Y/%m/")
    version = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("document", "version")]
        ordering = ["-version"]
