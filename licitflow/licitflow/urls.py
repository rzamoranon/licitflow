from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Auth + Registro
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("accounts/", include("django.contrib.auth.urls")),

    # páginas públicas / app
    path("", include(("pages.urls", "pages"), namespace="pages")),

    # otras apps
    path("busqueda/", include(("busqueda.urls", "busqueda"), namespace="busqueda")),
    path("oportunidades/", include(("oportunidades.urls", "oportunidades"), namespace="oportunidades")),
    path("documentos/", include(("documentos.urls", "documentos"), namespace="documentos")),
    path("crm/", include(("crm.urls", "crm"), namespace="crm")),

    path("admin/", admin.site.urls),
]