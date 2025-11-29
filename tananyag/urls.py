# tananyag/urls.py

from django.urls import path
# A beépített Django belépés/kijelentkezés nézetei (views)
from django.contrib.auth import views as auth_views
from .views import KurzusListView, KurzusFelvetelView
from . import views

urlpatterns = [
    # 1. Főoldal: A kurzusok listája (http://127.0.0.1:8000/)
    # A nézetet védi a LoginRequiredMixin, ezért a felhasználó először a login-ra irányítódik!
    path('', KurzusListView.as_view(), name='kurzus_list'),

    # 2. Belépés/Bejelentkezés (3. és 4. követelmény)
    # A template_name='tananyag/login.html' biztosítja a stílusos bejelentkező oldalt
    path('login/', auth_views.LoginView.as_view(template_name='tananyag/login.html'), name='login'),

    # 3. Kijelentkezés
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 4. Kurzus felvétel API (5. követelmény: JavaScript)
    path('kurzus-felvetel/', KurzusFelvetelView.as_view(), name='kurzus_felvetel_api'),

    path('profil/szerkesztes/', views.HallgatoUpdateView.as_view(), name='hallgato_edit'),
]