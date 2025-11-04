# tananyag/views.py
from django.shortcuts import render
from .models import Kurzus
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

# Minden bejelentkezett felhasználó láthatja
class KurzusListView(LoginRequiredMixin, ListView):
    model = Kurzus  # Melyik modellt listázzuk
    template_name = 'tananyag/kurzus_list.html'  # Melyik sablont használjuk
    context_object_name = 'kurzusok'  # Milyen néven érhető el a sablonban