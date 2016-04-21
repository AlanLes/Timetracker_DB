from django.shortcuts import render

# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
import datetime
from .models import Pracownik, CzasPracy, Przerwa, Urlop
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin



class MainPageView(LoginRequiredMixin, TemplateView):
    template_name = "timetrackerapp/main-page.html"


class PracownikListView(LoginRequiredMixin, ListView):
    model = Pracownik

    def get_context_data(self, **kwargs):
        context = super(PracownikListView, self).get_context_data(**kwargs)
        return context

class PracownikDetailView(LoginRequiredMixin, DetailView):
    model = Pracownik



def start_work(request, **kwargs):
    lastWorkTime = request.user.pracownik.czaspracy_set.order_by('-czas_przyjscia').first()
    status = ''
    # jesli przyszedles do pracy i nie wyszedles z pracy to nieok - sprawdzasz czy ostatni worklog zostal zakonczony
    if lastWorkTime:
        if not lastWorkTime.czas_wyjscia:
            status = '{"status:" "nok"}'
            return HttpResponse(status)

    todayWorkTime = CzasPracy(czas_przyjscia=datetime.datetime.now(), pracownik=request.user.pracownik)
    todayWorkTime.save()
    print(todayWorkTime)
    status = '{"status:" "ok"}'
    return HttpResponse(status)


def start_break(request, **kwargs):
    # jesli przyszedles do pracy i nie wyszedles z pracy to ok bo pracujesz
    # innymi slowy sprawdzasz czy ostatni worklog zostal zakonczony czy nie, jesli nie to git
    # musisz pracowac zeby isc na przerwe
    status = ''
    lastWorkTime = request.user.pracownik.czaspracy_set.order_by('-czas_przyjscia').first()
    if lastWorkTime:
        if not lastWorkTime.czas_wyjscia:
            lastBreak = request.user.pracownik.przerwa_set.order_by('-start_przerwy').first()
            if lastBreak:
                # jesli nie ma konca ostatniej przerwy to nie mozna isc na przerwe lol
                if not lastBreak.koniec_przerwy:
                    status = '{"status:" "nok"}'
                    return HttpResponse(status)

            todayAnotherBreak = Przerwa(start_przerwy=datetime.datetime.now(), pracownik=request.user.pracownik)
            todayAnotherBreak.save()
            print(todayAnotherBreak)
            status = '{"status:" "ok"}'
            return HttpResponse(status)

    status = '{"status:" "nok"}'
    return HttpResponse(status)


def end_break(request, **kwargs):
    # print(request.user.pracownik.przerwa_set.all())
    lastBreak = request.user.pracownik.przerwa_set.order_by('-start_przerwy').first()
    status = ''
    if lastBreak:
        # jesli nie ma konca ostatniej przerwy to wlasnie ta przerwe chcemy zakonczyc
        if not lastBreak.koniec_przerwy:
            lastBreak.koniec_przerwy = datetime.datetime.now()
            lastBreak.save()
            status = '{"status:" "ok"}'
            return HttpResponse(status)

    status = '{"status:" "nok"}'
    return HttpResponse(status)


def end_work(request, **kwargs):
    print(request.user.pracownik.czaspracy_set.all())
