from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import timedelta
import datetime
import time


def timedelta_to_text(timedel):
    tmp = timedel
    return time.strftime('%H:%M:%S', time.gmtime(tmp))


class Pracownik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    przelozony_id = models.ForeignKey('Pracownik', null=True, blank=True)
    stanowisko = models.CharField(max_length=20, null=False)

    def __str__(self):
        return "%s's profile" % self.user

    def is_kierownik(self):
        return self.stanowisko == 'kierownik'

    def lista_pracownikow(self):
        return Pracownik.objects.filter(przelozony_id=self)

    ### PRZERWY
    def laczny_czas_przerw(self, date):
        laczny_przerw = timedelta(milliseconds=0)
        for konkretny_log in self.przerwa_set.filter(start_przerwy__date=date):
            if konkretny_log.koniec_przerwy:
                laczny_przerw += (konkretny_log.koniec_przerwy - konkretny_log.start_przerwy)
        return laczny_przerw.seconds

    def laczny_czas_przerw_dzis(self):
        dzis = datetime.datetime.today()
        return self.laczny_czas_przerw(dzis)

    def t_laczny_czas_przerw(self, date):
        tmp = self.laczny_czas_przerw(date)
        return timedelta_to_text(tmp)

    def t_laczny_czas_przerw_dzis(self):
        tmp = self.laczny_czas_przerw_dzis()
        return timedelta_to_text(tmp)

    ### CZAS PRACY
    def laczny_czas_pracy(self, date):
        laczny_pracy = timedelta(milliseconds=0)
        for konkretny_log in self.czaspracy_set.filter(czas_przyjscia__date=date):
            if konkretny_log.czas_wyjscia:
                laczny_pracy += (konkretny_log.czas_wyjscia - konkretny_log.czas_przyjscia)
        return laczny_pracy.seconds

    def laczny_czas_pracy_dzis(self):
        dzis = datetime.datetime.today()
        return self.laczny_czas_pracy(dzis)

    def t_laczny_czas_pracy(self, date):
        tmp = self.laczny_czas_pracy(date)
        return timedelta_to_text(tmp)

    def t_laczny_czas_pracy_dzis(self):
        tmp = self.laczny_czas_pracy_dzis()
        return timedelta_to_text(tmp)

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


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Pracownik.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
