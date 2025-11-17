# config/urls.py

from django.contrib import admin
from django.urls import path, include  # <-- Fontos az 'include' import

urlpatterns = [
    # 1. Admin felület (CRUD és Biztonság)
    path('admin/', admin.site.urls),

    # 2. Django Beépített Hitelesítés (accounts/login, accounts/logout)
    # Ezzel oldjuk meg a korábbi 404-es hibát a /accounts/login/ útvonalon.
    path('accounts/', include('django.contrib.auth.urls')),

    # 3. Saját Alkalmazás (A Hallgatói felület főoldala)
    # Ez kapcsolja a http://127.0.0.1:8000/ címet a tananyag app útvonalaihoz.
    path('', include('tananyag.urls')),
]