from django.conf.urls import url
from .views import MainPageView, start_work, start_break, end_break, end_work
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', MainPageView.as_view()),

    url(r'^start-work/$', start_work),
    url(r'^start-break/$', start_break),
    url(r'^end-break/$', end_break),
    url(r'^end-work/$', end_work),
]
