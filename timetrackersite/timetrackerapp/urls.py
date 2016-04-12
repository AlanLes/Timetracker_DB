from django.conf.urls import url
from .views import PracownikListView, PracownikDetailView, start_work

urlpatterns = [
    url(r'^pracownicy/$', PracownikListView.as_view(), name='pracownik-list'),
    url(r'^pracownicy/(?P<pk>[0-9]+)/$', PracownikDetailView.as_view(), name='pracownik-datail'),
    url(r'^pracownicy/(?P<pk>[0-9]+)/start-work/$', start_work),
]