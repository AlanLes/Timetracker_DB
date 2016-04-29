from django import template
from django.template import Context
import datetime
import calendar

register = template.Library()


@register.inclusion_tag('timetrackerapp/month_log.html')
def get_month_log(pracownik):
    month_log = []
    now = datetime.datetime.now()
    for i in range(calendar.monthrange(now.year, now.month)[1]):
        data = datetime.date(now.year, now.month, i+1)
        poj_log_pracy = pracownik.t_laczny_czas_pracy(data)
        poj_log_przerw = pracownik.t_laczny_czas_przerw(data)
        if poj_log_pracy != '00:00:00':
            month_log.append((str(data), poj_log_przerw, poj_log_pracy))

    return {'month_log': month_log}
