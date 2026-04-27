from django.urls import path
from . import views

app_name = "oportunidades"

urlpatterns = [
    path("", views.index, name="index"),
]