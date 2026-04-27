from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import re

def validate_rut(value: str):
    """Valida RUT chileno con DV (K permitido)."""
    rut = value.replace(".", "").replace("-", "").upper()
    if not re.match(r"^\d{7,8}[0-9K]$", rut):
        raise ValidationError("RUT no tiene el formato correcto.")
    cuerpo, dv = rut[:-1], rut[-1]
    suma, factor = 0, 2
    for c in reversed(cuerpo):
        suma += int(c) * factor
        factor = 2 if factor == 7 else factor + 1
    resto = suma % 11
    dv_calc = "0" if (11 - resto) == 11 else "K" if (11 - resto) == 10 else str(11 - resto)
    if dv != dv_calc:
        raise ValidationError("RUT no válido.")

class Company(models.Model):
    name = models.CharField("Razón social", max_length=200)
    rut = models.CharField("RUT Empresa", max_length=12, unique=True, validators=[validate_rut])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rut})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField("Teléfono", max_length=20)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    terms_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_username()
