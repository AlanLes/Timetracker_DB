from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# from datetime import timedelta

# model kalendarz, pk - id generuje sie automatycznie, wiec data nie jest pk
class Kalendarz(models.Model):
    data = models.DateField(default=timezone.now, null=False)
    czy_pracujacy = models.BooleanField(default=True, null=False)
    uwagi = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return 'Data: ' + str(self.data)


class Przerwa(models.Model):
    start_przerwy = models.TimeField(null=False)
    koniec_przerwy = models.TimeField(null=True, blank=True)
    calkowity_czas_przerwy = models.DurationField(null=True, blank=True)

    def __str__(self):
        return 'Start przerwy o: ' + str(self.start_przerwy)

    def calculate_total_break_time(self):
        self.calkowity_czas_przerwy = self.start_przerwy - self.koniec_przerwy
        return self.calkowity_czas_przerwy


class CzasPracy(models.Model):
    kalendarz_id = models.ForeignKey(Kalendarz, null=False)
    czas_przyjscia = models.TimeField(null=False)
    czas_wyjscia = models.TimeField(null=True, blank=True)
    przerwa_id = models.ForeignKey(Przerwa, null=True, blank=True)
    calkowity_czas_pracy = models.DurationField(null=True, blank=True)

    def __str__(self):
        return 'Start pracy o: ' + str(self.czas_przyjscia)

    def calculate_total_work_time(self):
        self.calkowity_czas_pracy = self.czas_przyjscia - self.czas_wyjscia
        return self.calkowity_czas_pracy


class Pracownik(models.Model):
    przelozony_id = models.ForeignKey('self', null=True, blank=True)
    imie = models.CharField(max_length=20, null=False)
    nazwisko = models.CharField(max_length=30, null=False)
    stanowisko = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False)
    haslo = models.CharField(max_length=30, null=False)

    def __str__(self):
        return 'Pracownik ' + self.imie + ' ' + self.nazwisko + ' zajmujacy stanowisko ' + self.stanowisko

    # to do: write some imie and nazwisko validators.


class Urlop(models.Model):
    pracownik_id = models.ForeignKey(Pracownik, null=False)
    typ_urlopu = models.CharField(max_length=30, null=False)

    def __str__(self):
        return 'Urlop typu ' + self.typ_urlopu


class DzienPracownika(models.Model):
    czas_pracy_id = models.ForeignKey(CzasPracy, null=False)
    urlop_id = models.ForeignKey(Urlop, null=True, blank=True)
    pracownik_id = models.ForeignKey(Pracownik, null=False)

    def __str__(self):
        return 'Dzien pracownika.'