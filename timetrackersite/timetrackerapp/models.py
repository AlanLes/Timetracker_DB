from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import timedelta
import datetime
import time


def timedelta_to_string(timedel):
    return time.strftime('%H:%M:%S', time.gmtime(timedel.seconds))

class Pracownik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    przelozony_id = models.ForeignKey('Pracownik', null=True, blank=True)
    stanowisko = models.CharField(max_length=20, null=False)

    def __str__(self):
        return "%s's profile" % self.user

    # to do:
    # te metody ktore tu masz z czasem przerobic tak, zeby bpodejmowaly parametr daty, zeby byly uniwersalne
    # to znaczy w sumie tylko ta jedna metoda - laczny_czas_pracy, bo bedzie potrzebna do wyswietlania dla userow potem
    # no i jeszcze zrobic taka metode, ktora bedzie: laczny_czas_pracy_dzisiaj, ktora bedzie wywolywala tamta metode,
    # ale z dzisiejsza data. 

    def is_kierownik(self):
        return self.stanowisko == 'kierownik'

    def laczny_czas_przerw(self):
        laczny_przerw = timedelta(milliseconds=0)
        for konkretny_log in self.przerwa_set.filter(start_przerwy__date=datetime.datetime.today()):
            if konkretny_log.koniec_przerwy:
                laczny_przerw += (konkretny_log.koniec_przerwy - konkretny_log.start_przerwy)
        return time.strftime('%H:%M:%S', time.gmtime(laczny_przerw.seconds))

    def laczny_czas_pracy(self):
        laczny_pracy = timedelta(milliseconds=0)
        for konkretny_log in self.czaspracy_set.filter(czas_przyjscia__date=datetime.datetime.today()):
            if konkretny_log.czas_wyjscia:
                laczny_pracy += (konkretny_log.czas_wyjscia - konkretny_log.czas_przyjscia)
        return time.strftime('%H:%M:%S', time.gmtime(laczny_pracy.seconds))

    def czas_pracy_bez_przerw(self):
        laczny_przerw = timedelta(milliseconds=0)
        for konkretny_log in self.przerwa_set.filter(start_przerwy__date=datetime.datetime.today()):
            if konkretny_log.koniec_przerwy:
                laczny_przerw += (konkretny_log.koniec_przerwy - konkretny_log.start_przerwy)
        laczny_pracy = timedelta(milliseconds=0)
        for konkretny_log in self.czaspracy_set.filter(czas_przyjscia__date=datetime.datetime.today()):
            if konkretny_log.czas_wyjscia:
                laczny_pracy += (konkretny_log.czas_wyjscia - konkretny_log.czas_przyjscia)
        czas_bez_przerw = laczny_pracy - laczny_przerw
        return time.strftime('%H:%M:%S', time.gmtime(czas_bez_przerw.seconds))


    def lista_pracownikow (self):
        return Pracownik.objects.filter(przelozony_id=self)

    def status(self):
        zwrot_statusu = ''
        lastWorkTime = self.czaspracy_set.order_by('-czas_przyjscia').first()
        if lastWorkTime:
            if not lastWorkTime.czas_wyjscia:
                lastBreak = self.przerwa_set.order_by('-start_przerwy').first()
                if lastBreak:
                    # jesli nie ma konca ostatniej przerwy to znaczy ze z niej nie wrocil - jest na przerwie
                    if not lastBreak.koniec_przerwy:
                        zwrot_statusu = 'na przerwie'
                        return zwrot_statusu

                zwrot_statusu = 'pracujesz'
                return zwrot_statusu

        zwrot_statusu = 'nie pracujesz'
        return zwrot_statusu

    def czasy_obecny_miesiac(self):
        log_miesiaca = []
        log_dnia = {'data': '', 'laczny_czas': ''}
        for konkretny_log in self.czaspracy_set.filter(czas_przyjscia__month=datetime.datetime.now().month):
            return ''

        return log_miesiaca




class CzasPracy(models.Model):
    czas_przyjscia = models.DateTimeField(null=True, blank=True)
    czas_wyjscia = models.DateTimeField(null=True, blank=True)
    pracownik = models.ForeignKey(Pracownik)

    def __str__(self):
        return 'Start pracy o: ' + str(self.czas_przyjscia)


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
