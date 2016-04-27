from django.conf.urls import url
from .views import PracownikListView, PracownikDetailView, MainPageView, MonthLogView, start_work, start_break, end_break, end_work
from django.views.generic import TemplateView
urlpatterns = [
    url(r'^pracownicy/$', PracownikListView.as_view(), name='pracownik-list'),
    url(r'^pracownicy/(?P<pk>[0-9]+)/$', PracownikDetailView.as_view(), name='pracownik-datail'),

    url(r'^$', MainPageView.as_view()),
    url(r'^log/(?P<id_prac>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', MonthLogView.as_view()),

    url(r'^start-work/$', start_work),
    url(r'^start-break/$', start_break),
    url(r'^end-break/$', end_break),
    url(r'^end-work/$', end_work),

]

