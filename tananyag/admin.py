# tananyag/admin.py

from django.contrib import admin
from .models import Tanar, Kurzus, Hallgato, HallgatoKurzus

# Regisztrálja a modelleket, hogy megjelenjenek az Admin felületen
admin.site.register(Tanar)
admin.site.register(Kurzus)
admin.site.register(Hallgato)
admin.site.register(HallgatoKurzus)