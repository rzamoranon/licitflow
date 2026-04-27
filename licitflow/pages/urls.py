from django.urls import path
from django.views.generic import RedirectView 
from . import views

app_name = "pages"

urlpatterns = [
    # Páginas públicas (landing)
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("testimonial/", views.testimonial, name="testimonial"),
    path("team/", views.team, name="team"),
    path("feature/", views.feature, name="feature"),
    path("blog/", views.blog, name="blog"),
    path("service/", views.service, name="service"),
    path("about/", views.about, name="about"),
    path("", views.index, name="index"),  # landing pública

    # Auth
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("ingresar/", RedirectView.as_view(pattern_name="pages:login", permanent=False), name="ingresar"),  # alias legacy

    # Dashboard y secciones protegidas
    path("home/", views.home, name="home"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("reports/", views.reports_view, name="reports"),
    path("settings/", views.settings_view, name="settings"),
    path("profile/", views.profile_view, name="profile"),
    path("help/", views.help_view, name="help"),
]