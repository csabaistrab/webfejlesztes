# tananyag/models.py
from django.db import models
from django.contrib.auth.models import User


# --- 1. Tanár (ROLE_TANAR) ---
class Tanar(models.Model):
    # Egy-az-egyhez kapcsolat a Django beépített Auth felhasználói rendszeréhez
    felhasznalo = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nev = models.CharField(max_length=100)

    def __str__(self):
        return f"Tanár: {self.nev}"


# --- 2. Kurzus (1:N Kapcsolat SOK oldala) ---
class Kurzus(models.Model):
    nev = models.CharField(max_length=200)
    leiras = models.TextField()

    # 1:N Kapcsolat: Egy Tanárhoz több Kurzus tartozhat
    tanar = models.ForeignKey(Tanar, on_delete=models.CASCADE)

    def __str__(self):
        return self.nev


# --- 3. Hallgató (ROLE_HALLGATO) ---
class Hallgato(models.Model):
    felhasznalo = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nev = models.CharField(max_length=100)

    # N:M Kapcsolat a Kurzushoz, a HallgatoKurzus (köztes) táblán keresztül
    kurzusok = models.ManyToManyField(Kurzus, through='HallgatoKurzus')

    def __str__(self):
        return f"Hallgató: {self.nev}"


# --- 4. HallgatoKurzus (Az N:M Kapcsolati Tábla és a Jegy) ---
class HallgatoKurzus(models.Model):
    hallgato = models.ForeignKey(Hallgato, on_delete=models.CASCADE)
    kurzus = models.ForeignKey(Kurzus, on_delete=models.CASCADE)

    # 🚨 KRITÉRIUM: A jegy mező az N:M kapcsolatban 🚨
    jegy = models.IntegerField()

    class Meta:
        # Ez biztosítja, hogy egy hallgató csak egyszer vehesse fel ugyanazt a kurzust
        unique_together = ('hallgato', 'kurzus')

    def __str__(self):
        return f"{self.hallgato.nev} - {self.kurzus.nev} ({self.jegy})"