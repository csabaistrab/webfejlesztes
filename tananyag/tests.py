# tananyag/tests.py

# Kötelező importok a Django tesztkörnyezethez
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.db import IntegrityError

# Modelljeink importálása
from tananyag.models import Hallgato, Kurzus, Tanar, HallgatoKurzus


# ----------------------------------------------------------------------
# KurzusFelvetelApiTest
# ----------------------------------------------------------------------

# Ez az osztály öröklődik a TestCase-ből, így a tesztfuttató megtalálja
class KurzusFelvetelApiTest(TestCase):
    """Teszteli a kurzus_felvetel API végpont üzleti logikáját."""

    def setUp(self):
        """Tesztadatok beállítása minden teszt előtt."""
        self.client = Client()

        # 1. User fiókok létrehozása
        self.user = User.objects.create_user(username='teszthallgato', password='password')
        self.tanar_user = User.objects.create_user(username='tanar', password='password')

        # 2. Modell profilok létrehozása (OneToOneField miatt szükséges)
        self.hallgato = Hallgato.objects.create(user=self.user, nev='Teszt Hallgató', kar='INF')
        self.tanar = Tanar.objects.create(user=self.tanar_user, nev='Teszt Tanár')

        # 3. Kurzus létrehozása
        self.kurzus = Kurzus.objects.create(nev='Teszt Kurzus', tanar=self.tanar)

    def test_kurzus_felvetel_sikeres(self):
        """Ellenőrzi a sikeres kurzusfelvételt."""
        self.client.login(username='teszthallgato', password='password')

        # Kérés küldése az API-nak
        response = self.client.post('/api/kurzus-felvetel/', {'kurzus_id': self.kurzus.id})

        # Állítás 1: HTTP 200 OK válasz érkezett
        self.assertEqual(response.status_code, 200)

        # Állítás 2: A HallgatoKurzus rekord tényleg létrejött
        self.assertTrue(HallgatoKurzus.objects.filter(
            hallgato=self.hallgato, kurzus=self.kurzus
        ).exists())

    def test_kurzus_felvetel_mar_felvett(self):
        """Ellenőrzi, hogy a rendszer kezeli a duplikált kurzusfelvételt (IntegrityError)."""
        # Előfeltétel: Már felvettük a kurzust
        HallgatoKurzus.objects.create(hallgato=self.hallgato, kurzus=self.kurzus)

        # Teszt: Ismételt felvétel
        self.client.login(username='teszthallgato', password='password')
        response = self.client.post('/api/kurzus-felvetel/', {'kurzus_id': self.kurzus.id})

        # Állítás: HTTP 400 Bad Request érkezett (üzleti logika hiba)
        self.assertEqual(response.status_code, 400)
        self.assertIn('hiba', response.json())

    def test_kurzus_felvetel_bejelentkezes_nelkul(self):
        """Ellenőrzi a biztonságot: bejelentkezés nélkül nem lehet felvenni."""
        # Kérés küldése bejelentkezés nélkül
        response = self.client.post('/api/kurzus-felvetel/', {'kurzus_id': self.kurzus.id})

        # Állítás: HTTP 302 Redirect érkezett (átirányítás a login oldalra)
        # Bár a mi views.py kódunkban van @login_required, ami 302-t várna,
        # a @require_POST és az API-végpont hibakezelése miatt 403-at is adhat,
        # de a 302 a legtisztább jelzés a login_required-től.
        self.assertEqual(response.status_code, 302)