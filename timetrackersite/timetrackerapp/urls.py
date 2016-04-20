from django.conf.urls import url
from .views import PracownikListView, PracownikDetailView, MainPageView, start_work
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^pracownicy/$', PracownikListView.as_view(), name='pracownik-list'),
    url(r'^pracownicy/(?P<pk>[0-9]+)/$', PracownikDetailView.as_view(), name='pracownik-datail'),
    url(r'^start-work/$', start_work),
    url(r'^$', MainPageView.as_view()),
]