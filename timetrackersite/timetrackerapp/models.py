from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import timedelta


class Pracownik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    przelozony_id = models.ForeignKey('Pracownik', null=True, blank=True)
    stanowisko = models.CharField(max_length=20, null=False)

    def __str__(self):
        return "%s's profile" % self.user
    # to do: write some imie and nazwisko validators.

    def is_kierownik(self):
        return self.stanowisko == 'kierownik'



class CzasPracy(models.Model):
    czas_przyjscia = models.DateTimeField(null=True, blank=True)
    czas_wyjscia = models.DateTimeField(null=True, blank=True)
    pracownik = models.ForeignKey(Pracownik)

    def __str__(self):
        return 'Start pracy o: ' + str(self.czas_przyjscia)

    def laczny_czas_pracy(self):
        return "dupa"




class Przerwa(models.Model):
    start_przerwy = models.DateTimeField(null=True, blank=True)
    koniec_przerwy = models.DateTimeField(null=True, blank=True)
    pracownik = models.ForeignKey(Pracownik)

    def __str__(self):
        return 'Start przerwy o: ' + str(self.start_przerwy)



class Urlop(models.Model):
    start_urlopu = models.DateField(null=True, blank=True)
    koniec_urlopu = models.DateField(null=True, blank=True)
    typ_urlopu = models.CharField(max_length=30, null=False)

    def __str__(self):
        return 'Urlop typu ' + self.typ_urlopu



def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Pracownik.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)