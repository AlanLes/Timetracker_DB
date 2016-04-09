from django.conf.urls import url
from .views import PracownikListView, PracownikDetailView

urlpatterns = [
    url(r'^pracownicy/$', PracownikListView.as_view(), name='pracownik-list'),
    url(r'^(?P<id>[-\w]+)/$', PracownikDetailView.as_view(), name='pracownik-detail'),
]