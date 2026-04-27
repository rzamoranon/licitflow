from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

from .forms import LoginForm


def index(request):
    """Landing pública (no requiere login)."""
    return render(request, "pages/index.html")


def _safe_next_url(request, candidate):
    """
    Devuelve `candidate` sólo si es una URL segura y pertenece al mismo host;
    en caso contrario, retorna None.
    """
    if not candidate:
        return None
    return candidate if url_has_allowed_host_and_scheme(
        url=candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ) else None


def login_view(request):
    """
    Login vía usuario/email + password. Respeta `?next=` si es seguro.
    """
    if request.user.is_authenticated:
        return redirect("pages:home")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        identifier = form.cleaned_data["identifier"]
        password   = form.cleaned_data["password"]
        remember   = form.cleaned_data.get("remember_me")

        user = authenticate(request, username=identifier, password=password)
        if user:
            login(request, user)

            # Manejo de sesión según "Recordarme"
            # - None => edad por defecto (SESSION_COOKIE_AGE)
            # - 0    => expira al cerrar el navegador
            request.session.set_expiry(None if remember else 0)

            # Protege la redirección "next"
            posted_next = request.POST.get("next")
            get_next    = request.GET.get("next")
            next_url    = _safe_next_url(request, posted_next) or _safe_next_url(request, get_next)

            return redirect(next_url or "pages:home")

        messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """Cierra sesión y vuelve al login."""
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("pages:login")


@login_required
def home(request):
    """Dashboard principal (protegido)."""
    perfil = getattr(request.user, "userprofile", None)
    return render(request, "pages/home.html", {
        "perfil": perfil,
        "is_admin": bool(perfil and getattr(perfil, "role", None) in ["APP_ADMIN", "ORG_ADMIN"]),
    })


# --- Stubs de navegación (protegidos) ---
@login_required
def calendar_view(request):
    return HttpResponse("<div style='padding:24px;font-family:Inter,sans-serif'>Calendario — pronto 🚧</div>")

@login_required
def reports_view(request):
    return HttpResponse("<div style='padding:24px;font-family:Inter,sans-serif'>Reportes — pronto 🚧</div>")

@login_required
def settings_view(request):
    return HttpResponse("<div style='padding:24px;font-family:Inter,sans-serif'>Configuración — pronto 🚧</div>")

@login_required
def profile_view(request):
    return HttpResponse("<div style='padding:24px;font-family:Inter,sans-serif'>Perfil — pronto 🚧</div>")

@login_required
def help_view(request):
    return HttpResponse("<div style='padding:24px;font-family:Inter,sans-serif'>Ayuda — pronto 🚧</div>")


# --- Páginas informativas simples de la landing ---
def about(request):       return HttpResponse("Página: Nosotros")
def service(request):     return HttpResponse("Página: Servicios")
def blog(request):        return HttpResponse("Página: Blog")
def feature(request):     return HttpResponse("Página: Características")
def team(request):        return HttpResponse("Página: Equipo")
def testimonial(request): return HttpResponse("Página: Testimonios")
def faq(request):         return HttpResponse("Página: Preguntas Frecuentes")
def contact(request):     return HttpResponse("Página: Contacto")