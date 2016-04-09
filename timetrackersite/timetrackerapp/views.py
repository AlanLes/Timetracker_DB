from django.shortcuts import render

# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.utils import timezone
from .models import Pracownik

class PracownikDetailView(DetailView):
    model = Pracownik

    def get_context_data(self, **kwargs):
        context = super(PracownikDetailView, self).get_context_data(self, **kwargs)
        context['now'] = timezone.now()
        return context


class PracownikListView(ListView):
    model = Pracownik

    def get_context_data(self, **kwargs):
        context = super(PracownikListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context