from django.contrib import admin
from django.urls import path, include

handler404 = 'pages.views.page_not_found'  # 404 personalizada

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls', namespace='pages')),
]