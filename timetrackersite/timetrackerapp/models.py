from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# model kalendarz, pk - id generuje sie automatycznie, wiec data nie jest pk
class Kalendarz(models.Model):
    data = models.DateField(default=timezone.now)
    czy_pracujacy = models.BooleanField
    uwagi = models.CharField(max_length=200)

    def __str__(self):
        return self.data


class CzasPracy(models.Model):
    calendar = models.ForeignKey(Kalendarz)
    czas_przyjscia = models.TimeField