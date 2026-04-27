from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('signup/', views.register_account_public, name='register_account_public'),
    path('signup/company/', views.register_company_public, name='register_company_public'),
    path("registrar/", views.register_account, name="register_account"),
    path("registrar/empresa/", views.register_company, name="register_company"),
]
