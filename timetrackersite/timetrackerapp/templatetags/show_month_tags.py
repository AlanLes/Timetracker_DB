from django import template
from django.template import Context
import datetime
import calendar

register = template.Library()


@register.inclusion_tag('timetrackerapp/month_log.html')
def get_month_log(pracownik):
    month_log = []
    now = datetime.datetime.now()

    # month_log.join()

    # month_log = pracownik.czaspracy_set.filter(czas_przyjscia__month=datetime.datetime.now().month)
    for i in range(calendar.monthrange(now.year, now.month)[1]):
        data = datetime.date(now.year, now.month, i+1)
        poj_log = pracownik.t_laczny_czas_pracy(data)
        if poj_log != '00:00:00':
            # str(data), poj_log)
            month_log.append((str(data), poj_log))

    return {'month_log': month_log}
