# tananyag/forms.py

from django import forms
from .models import Hallgato

class HallgatoProfileForm(forms.ModelForm):
    class Meta:
        # A Hallgato modellből hozzuk létre a formot
        model = Hallgato
        # Csak ezeket a mezőket engedélyezzük szerkesztésre
        fields = ['nev', 'kar']