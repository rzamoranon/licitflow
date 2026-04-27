from django import forms

class LoginForm(forms.Form):
    identifier = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Usuario o email",
            "autocomplete": "username",
        })
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Contraseña",
            "autocomplete": "current-password",
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
