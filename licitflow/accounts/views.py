from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings

from .forms import RegisterAccountForm, RegisterCompanyForm
from .models import Company

def register_account(request):
    if request.method == "POST":
        form = RegisterAccountForm(request.POST)
        if form.is_valid():
            request.session["reg"] = {
                "first_name": form.cleaned_data["first_name"],
                "last_name":  form.cleaned_data["last_name"],
                "phone":      form.cleaned_data["phone"],
                "email":      form.cleaned_data["email"].lower(),
                "password":   form.cleaned_data["password1"],
                "terms":      form.cleaned_data["terms"],
            }
            return redirect("accounts:register_company")
    else:
        form = RegisterAccountForm()
    return render(request, "accounts/register_step1.html", {"form": form})

def register_company(request):
    if "reg" not in request.session:
        return redirect("accounts:register_account")

    if request.method == "POST":
        form = RegisterCompanyForm(request.POST)
        if form.is_valid():
            data = request.session.pop("reg")
            user = User.objects.create_user(
                username=data["email"], email=data["email"],
                first_name=data["first_name"], last_name=data["last_name"],
                password=data["password"]
            )
            company = Company.objects.create(
                name=form.cleaned_data["company_name"],
                rut=form.cleaned_data["company_rut"]
            )
            # asegurar perfil
            from accounts.models import UserProfile
            if not hasattr(user, "profile"):
                UserProfile.objects.create(user=user, phone=data["phone"], company=company, terms_accepted=data["terms"])
            else:
                user.profile.phone = data["phone"]
                user.profile.company = company
                user.profile.terms_accepted = data["terms"]
                user.profile.save()

            user = authenticate(request, username=data["email"], password=data["password"])
            if user:
                login(request, user)

            try:
                subject = "¡Bienvenido a LicitFlow!"
                html = render_to_string("emails/welcome.html", {"user": user, "request": request})
                send_mail(
                    subject,
                    "Bienvenido a LicitFlow.",
                    getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@licitflow.com"),
                    [user.email],
                    html_message=html,
                    fail_silently=True,
                )
            except Exception:
                pass

            request.session["show_welcome_modal"] = True
            messages.success(request, "Tu cuenta fue creada correctamente. ¡Bienvenido!")
            return redirect("pages:home")
    else:
        form = RegisterCompanyForm()
    return render(request, "accounts/register_step2.html", {"form": form})


def register_account_public(request):
    from .forms import RegisterAccountForm
    if request.method == "POST":
        form = RegisterAccountForm(request.POST)
        if form.is_valid():
            request.session["reg"] = {
                "first_name": form.cleaned_data["first_name"],
                "last_name":  form.cleaned_data["last_name"],
                "phone":      form.cleaned_data["phone"],
                "email":      form.cleaned_data["email"].lower(),
                "password":   form.cleaned_data["password1"],
                "terms":      form.cleaned_data["terms"],
            }
            from django.shortcuts import redirect
            return redirect("accounts:register_company_public")
    else:
        form = RegisterAccountForm()
    from django.shortcuts import render
    return render(request, "accounts/register_public_step1.html", {"form": form})

def register_company_public(request):
    from django.shortcuts import redirect, render
    from django.contrib import messages
    from django.contrib.auth import authenticate, login
    from django.contrib.auth.models import User
    from django.template.loader import render_to_string
    from django.core.mail import send_mail
    from django.conf import settings
    from .forms import RegisterCompanyForm
    from .models import Company, UserProfile
    if "reg" not in request.session:
        return redirect("accounts:register_account_public")
    if request.method == "POST":
        form = RegisterCompanyForm(request.POST)
        if form.is_valid():
            data = request.session.pop("reg")
            user = User.objects.create_user(
                username=data["email"], email=data["email"],
                first_name=data["first_name"], last_name=data["last_name"],
                password=data["password"]
            )
            company = Company.objects.create(
                name=form.cleaned_data["company_name"],
                rut=form.cleaned_data["company_rut"]
            )
            UserProfile.objects.update_or_create(
                user=user,
                defaults={"phone": data["phone"], "company": company, "terms_accepted": data["terms"]}
            )
            u = authenticate(request, username=data["email"], password=data["password"])
            if u: login(request, u)
            try:
                subject = "¡Bienvenido a LicitFlow!"
                html = render_to_string("emails/welcome.html", {"user": user, "request": request})
                send_mail(subject, "Bienvenido a LicitFlow.",
                          getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@licitflow.com"),
                          [user.email], html_message=html, fail_silently=True)
            except Exception:
                pass
            request.session['show_welcome_modal'] = True
            messages.success(request, "Tu cuenta fue creada correctamente. ¡Bienvenido!")
            return redirect("pages:home")
    else:
        form = RegisterCompanyForm()
    return render(request, "accounts/register_public_step2.html", {"form": form})
