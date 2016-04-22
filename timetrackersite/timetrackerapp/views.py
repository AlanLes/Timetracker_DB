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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        c = super(MainPageView, self).get_context_data(**kwargs)
        user = self.request.user
        pracownik = user.pracownik
        obecny_dzien = CzasPracy.objects.filter(pracownik=pracownik,
                                                czas_przyjscia__day=datetime.datetime.now().day,
                                                czas_przyjscia__month=datetime.datetime.now().month,
                                                czas_przyjscia__year=datetime.datetime.now().year)
        przerwy_obecnego_dnia = Przerwa.objects.filter(pracownik=pracownik,
                                                       start_przerwy__day=datetime.datetime.now().day,
                                                       start_przerwy__month=datetime.datetime.now().month,
                                                       start_przerwy__year=datetime.datetime.now().year)
        c["log_dnia"] = obecny_dzien
        c["log_przerw"] = przerwy_obecnego_dnia
        return c



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
    status = ''
    # najpierw sprawdzasz czy jestes w pracy, czyli czy przyjscie do pracy zostalo odnotowane
    # i zakonczenie nie zostalo odnotowane
        # jesli nie ma ostatniego przyjscia, czyli nie byles w pracy ani razu - nok
        # jesli ostatnie przyjscie jest i jest zakonczone - nok
        # jesli ostatnie przyjscie jest i nie jest zakonczone ->
            # potem sprawdzasz czy ostatnia przerwa na ktorej byles zostala zakonczona
                # jesli nie zostala zakonczona to zakanczasz ja i zakanczasz prace
            #jesli zostala zakonczona to zakanczasz prace

    # jesli przyszedles do pracy i nie wyszedles z pracy to ok bo pracujesz
    # innymi slowy sprawdzasz czy ostatni worklog zostal zakonczony czy nie, jesli nie to git
    # musisz pracowac zeby moc zakonczyc prace !
    lastWorkTime = request.user.pracownik.czaspracy_set.order_by('-czas_przyjscia').first()
    if lastWorkTime:
        print("lastWorkTime")
        if not lastWorkTime.czas_wyjscia:
            print("not lastWorkTime.czas_wyjscia")
            lastBreak = request.user.pracownik.przerwa_set.order_by('-start_przerwy').first()
            if lastBreak:
                print("lastBreak")
                # jesli nie ma konca ostatniej przerwy to nalezy go stworzyc - koniec przerwy i koniec pracy w jednym
                if not lastBreak.koniec_przerwy:
                    print("not lastBreak.koniec_przerwy")
                    lastBreak.koniec_przerwy = datetime.datetime.now()
                    lastBreak.save()
                    print(lastBreak.koniec_przerwy)
                    lastWorkTime.czas_wyjscia = datetime.datetime.now()
                    lastWorkTime.save()
                    status = '{"status:" "ok"}'
                    return HttpResponse(status)
                else:
                    # byl na przerwie  (chocby jakiejs kiedys!) i zakonczyl przerwe!
                    lastWorkTime.czas_wyjscia = datetime.datetime.now()
                    lastWorkTime.save()
                    status = '{"status:" "ok"}'
                    return HttpResponse(status)
            else:
                print("else")
                #w takim wypadku oznacza to, ze nie byles dzisiaj na przerwie, ale to spoko, nic nie szkodzi
                lastWorkTime.czas_wyjscia = datetime.datetime.now()
                lastWorkTime.save()
                status = '{"status:" "ok"}'
                return HttpResponse(status)
    print("not ok")
    status = '{"status:" "nok"}'
    return HttpResponse(status)