# tananyag/models.py

from django.db import models
from django.contrib.auth.models import User


# --- 1. Alapvető Entitások (1:N kapcsolat alapkő) ---

class Tanar(models.Model):
    # A Tanár egy Django User fiókhoz van kötve
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nev = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Tanár"
        # 🚨 NYELVHELYESSÉGI JAVÍTÁS
        verbose_name_plural = "Tanárok"

    def __str__(self):
        return self.nev


class Hallgato(models.Model):
    # A Hallgató is egy Django User fiókhoz van kötve
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nev = models.CharField(max_length=100)
    kar = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Hallgató"
        # 🚨 NYELVHELYESSÉGI JAVÍTÁS
        verbose_name_plural = "Hallgatók"

    def __str__(self):
        return self.nev


# --- 2. Kurzus Modell (1:N kapcsolat) ---

class Kurzus(models.Model):
    nev = models.CharField(max_length=200)
    leiras = models.TextField()
    # 🚨 1:N KAPCSOLAT: Egy kurzushoz egy tanár tartozik
    tanar = models.ForeignKey(Tanar, on_delete=models.CASCADE, related_name='kurzusok')

    class Meta:
        verbose_name = "Kurzus"
        # 🚨 NYELVHELYESSÉGI JAVÍTÁS
        verbose_name_plural = "Kurzusok"

    def __str__(self):
        return self.nev


# --- 3. N:M Kapcsolat Modell ---

class HallgatoKurzus(models.Model):
    # 🚨 N:M KAPCSOLAT: Kapcsolja a hallgatót a kurzussal
    hallgato = models.ForeignKey(Hallgato, on_delete=models.CASCADE)
    kurzus = models.ForeignKey(Kurzus, on_delete=models.CASCADE)

    # Kapcsolati adat: A jegy is itt tárolódik
    jegy = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Hallgató kurzusa"
        # 🚨 NYELVHELYESSÉGI JAVÍTÁS
        verbose_name_plural = "Hallgatók kurzusai"
        # Ne lehessen kétszer felvenni ugyanazt a kurzust
        unique_together = ('hallgato', 'kurzus',)

    def __str__(self):
        return f"{self.hallgato.nev} - {self.kurzus.nev} ({self.jegy})"