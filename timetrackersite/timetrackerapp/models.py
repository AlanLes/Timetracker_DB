from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# from datetime import timedelta

# model kalendarz, pk - id generuje sie automatycznie, wiec data nie jest pk
class Kalendarz(models.Model):
    data = models.DateField(default=timezone.now)
    czy_pracujacy = models.BooleanField
    uwagi = models.CharField(max_length=200)

    def __str__(self):
        return 'Data: ' + self.data


class Przerwa(models.Model):
    start_przerwy = models.TimeField()
    koniec_przerwy = models.TimeField()
    calkowity_czas_przerwy = models.DurationField()

    def __str__(self):
        return 'Laczny czas przerwy' + self.calkowity_czas_przerwy


class CzasPracy(models.Model):
    kalendarz_id = models.ForeignKey(Kalendarz)
    czas_przyjscia = models.TimeField()
    czas_wyjscia = models.TimeField()
    przerwa_id = models.ForeignKey(Przerwa)
    calkowity_czas_pracy = models.DurationField()

    def __str__(self):
        return 'Laczny czas pracy: ' + self.calkowity_czas_pracy


class Urlop(models.Model):
    pracownik_id = models.ForeignKey(Pracownik)
    typ_urlopu = models.CharField(max_length=30)

    def __str__(self):
        return 'Urlop typu ' + self.typ_urlopu+ ' pracownika o id: ' + self.pracownik_id


class Pracownik(models.Model):
    przelozony_id = models.ForeignKey('self')
    imie = models.CharField(max_length=20)
    nazwisko = models.CharField(max_length=30)
    stanowisko = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    haslo = models.CharField(max_length=30)

    def __str__(self):
        return 'Pracownik ' + self.imie + ' ' + self.nazwisko + ' zajmujacy stanowisko ' + self.stanowisko

    def validateEmail(email):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
    # to do: write some imie and nazwisko validators.



class DzienPracownika(models.Model):
    czas_pracy_id = models.ForeignKey(CzasPracy)
    urlop_id = models.ForeignKey(Urlop)
    pracownik_id = models.ForeignKey(Pracownik)