from django.shortcuts import render

# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.utils import timezone
from .models import Pracownik, CzasPracy, Przerwa, DzienPracownika, Urlop
from django.http import HttpResponse
import datetime

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
    todayWorkTime = CzasPracy()
    todayWorkTime.save()


    presentDay = DzienPracownika()
    presentDay.save()


    return HttpResponse('{"status:" "ok"}')
