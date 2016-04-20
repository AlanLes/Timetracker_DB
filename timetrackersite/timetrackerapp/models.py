from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save


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
    data = models.DateField(default=timezone.now, null=False)
    przerwa_id = models.ForeignKey(Przerwa, null=True, blank=True)
    czas_przyjscia = models.TimeField(null=False)
    czas_wyjscia = models.TimeField(null=True, blank=True)
    calkowity_czas_pracy = models.DurationField(null=True, blank=True)

    def __str__(self):
        return 'Start pracy o: ' + str(self.czas_przyjscia)

    def calculate_total_work_time(self):
        self.calkowity_czas_pracy = self.czas_przyjscia - self.czas_wyjscia
        return self.calkowity_czas_pracy


class Pracownik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    przelozony_id = models.ForeignKey('Pracownik', null=True, blank=True)
    stanowisko = models.CharField(max_length=20, null=False)

    def __str__(self):
        return "%s's profile" % self.user
    # to do: write some imie and nazwisko validators.

    def is_kierownik(self):
        return self.stanowisko == 'kierownik'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Pracownik.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Urlop(models.Model):
    typ_urlopu = models.CharField(max_length=30, null=False)

    def __str__(self):
        return 'Urlop typu ' + self.typ_urlopu


class DzienPracownika(models.Model):
    czas_pracy_id = models.ForeignKey(CzasPracy, null=False)
    urlop_id = models.ForeignKey(Urlop, null=True, blank=True)
    pracownik_id = models.ForeignKey(Pracownik, null=False)

    def __str__(self):
        return 'Dzien pracownika.'