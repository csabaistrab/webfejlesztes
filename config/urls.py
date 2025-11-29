from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # <-- Ezt importálja!

urlpatterns = [
    # 1. Admin felület
    path('admin/', admin.site.urls),

    # 2. 🎯 KONTROLLÁLT BEJELENTKEZÉS ÉS KIJELENTKEZÉS
    # A Django beépített LoginView használata
    path('login/', auth_views.LoginView.as_view(template_name='tananyag/login.html'), name='login'),

    # A Django beépített LogoutView használata (törli a sessiont!)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 3. Saját Alkalmazás
    path('', include('tananyag.urls')),
]