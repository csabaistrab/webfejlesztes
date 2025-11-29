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


# 1. Kurzus Listázó Nézet (Hallgatói felület főoldala)
class KurzusListView(LoginRequiredMixin, ListView):
    model = Kurzus
    template_name = 'tananyag/kurzus_list.html'
    context_object_name = 'kurzusok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ellenőrzi, hogy a Hallgato profil létezik-e (a HallgatoKurzus model lekérdezése miatt)
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


# 2. Kurzus Felvételi API Nézet
@method_decorator(csrf_exempt, name='dispatch')
class KurzusFelvetelView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # 🎯 JAVÍTÁS: Automatikusan létrehozza a Hallgato profilt, ha az hiányzik.
        # Ez megoldja a "hiányzó Hallgato profil" hibát az új felhasználóknál.
        if not hasattr(request.user, 'hallgato'):
            try:
                Hallgato.objects.create(
                    felhasznalo=request.user,
                    # Kezdeti név beállítása a felhasználónévre
                    nev=request.user.username
                )
            except Exception as e:
                return JsonResponse({'error': f'Hiba a Hallgató profil létrehozásakor: {str(e)}'}, status=500)

        try:
            data = json.loads(request.body)
            kurzus_id = data.get('kurzus_id')

            kurzus = Kurzus.objects.get(id=kurzus_id)
            # Biztonságosan elérjük a most már létező Hallgato objektumot
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
        except json.JSONDecodeError:
            # A 'JSONDecodeError' hiba megoldásához (Unexpected token <)
            # Kérem, győződjön meg róla, hogy a kurzus_list.html-ben lévő JavaScript KÜLDI a CSRF tokent!
            return JsonResponse({'error': 'Érvénytelen adatok. Lehet, hogy a CSRF token hiányzik vagy hibás.'},
                                status=400)
        except Exception:
            return JsonResponse({'error': 'Hibás kérés vagy belső hiba.'}, status=500)


# 3. Hallgatói profil szerkesztése
class HallgatoUpdateView(LoginRequiredMixin, UpdateView):
    """Hallgatói profil szerkesztése. Csak a saját profil módosítható."""
    model = Hallgato
    form_class = HallgatoProfileForm
    template_name = 'tananyag/hallgato_form.html'
    success_url = reverse_lazy('kurzus_list')

    # BIZTONSÁGI ELLENŐRZÉS: Csak a saját objektum szerkeszthető!
    def get_object(self, queryset=None):
        try:
            # Csak azt a Hallgato objektumot kérjük le, ami az aktuálisan bejelentkezett User-hez tartozik
            return self.request.user.hallgato
        except Hallgato.DoesNotExist:
            # Ha a profil nem létezik (bár a KurzusFelvetelView már létrehozza), akkor 404 hiba.
            raise Http404("Hallgató profil nem található.")