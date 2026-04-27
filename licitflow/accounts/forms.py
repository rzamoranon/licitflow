from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Company, validate_rut


class RegisterAccountForm(forms.Form):
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name  = forms.CharField(label="Apellido", max_length=150)
    phone      = forms.CharField(label="Teléfono", max_length=20)
    email      = forms.EmailField(label="Correo Electrónico")
    password1  = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2  = forms.CharField(label="Repite la contraseña", widget=forms.PasswordInput)
    terms      = forms.BooleanField(label="Acepto los Términos y Condiciones")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned


class RegisterCompanyForm(forms.Form):
    company_name = forms.CharField(label="Nombre de la empresa", max_length=200)
    company_rut  = forms.CharField(label="RUT Empresa", max_length=12)

    def clean_company_rut(self):
        rut = self.cleaned_data["company_rut"]
        validate_rut(rut)
        if Company.objects.filter(rut__iexact=rut).exists():
            raise ValidationError("Este RUT ya está registrado.")
        return rut