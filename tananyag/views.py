# tananyag/views.py

from django.shortcuts import render
from .models import Kurzus, Hallgato, HallgatoKurzus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.http import Http404
from .forms import HallgatoProfileForm

# Kurzus Listázó Nézet (Hallgatói felület főoldala)
class KurzusListView(LoginRequiredMixin, ListView):
    model = Kurzus
    template_name = 'tananyag/kurzus_list.html'
    context_object_name = 'kurzusok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🚨 FRISSÍTETT LOGIKA: Lekérdezi a felvett kurzusok ID-it 🚨
        if hasattr(self.request.user, 'hallgato'):
            hallgato = self.request.user.hallgato
            # Lekéri a felvett kurzusok ID-it (a sablonhoz)
            felvett_kurzusok_id = HallgatoKurzus.objects.filter(
                hallgato=hallgato
            ).values_list('kurzus_id', flat=True)

            # Hozzáadja az ID-kat a sablon kontextusához
            context['felvett_kurzusok_id'] = set(felvett_kurzusok_id)
        else:
            context['felvett_kurzusok_id'] = set()  # Üres halmaz, ha nincs hallgató profil

        return context


# Kurzus Felvételi API Nézet (az 5. követelményhez szükséges JS/fetch hívás)
@method_decorator(csrf_exempt, name='dispatch')
class KurzusFelvetelView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Nincs bejelentkezve.'}, status=403)

        if not hasattr(request.user, 'hallgato'):
            return JsonResponse({'error': 'Csak Hallgató vehet fel kurzust (hiányzó Hallgato profil).'}, status=403)

        try:
            data = json.loads(request.body)
            kurzus_id = data.get('kurzus_id')

            kurzus = Kurzus.objects.get(id=kurzus_id)
            hallgato = request.user.hallgato

            # Ellenőrzés, hogy ne lehessen kétszer felvenni
            if HallgatoKurzus.objects.filter(hallgato=hallgato, kurzus=kurzus).exists():
                return JsonResponse({'error': 'Ezt a kurzust már felvette.'}, status=400)

            HallgatoKurzus.objects.create(
                hallgato=hallgato,
                kurzus=kurzus,
                jegy=0
            )

            return JsonResponse({'message': f'{kurzus.nev} kurzus sikeresen felvéve.'})

        except Kurzus.DoesNotExist:
            return JsonResponse({'error': 'A kurzus nem található.'}, status=404)
        except Exception:
            return JsonResponse({'error': 'Hibás kérés vagy belső hiba.'}, status=400)

class HallgatoUpdateView(LoginRequiredMixin, UpdateView):
    """Hallgatói profil szerkesztése. Csak a saját profil módosítható."""
    model = Hallgato
    form_class = HallgatoProfileForm
    template_name = 'tananyag/hallgato_form.html' # Ezt a sablont hozzuk létre
    success_url = reverse_lazy('kurzus_list') # Sikeres mentés után visszairányítás a főoldalra

    # 🔑 BIZTONSÁGI ELLENŐRZÉS: Csak a saját objektum szerkeszthető!
    def get_object(self, queryset=None):
        try:
            # Csak azt a Hallgato objektumot kérjük le, ami az aktuálisan bejelentkezett User-hez tartozik
            return self.request.user.hallgato
        except Hallgato.DoesNotExist:
            raise Http404("Hallgató profil nem található.")