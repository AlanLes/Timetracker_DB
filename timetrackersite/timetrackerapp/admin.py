from django.contrib import admin
from .models import Pracownik, CzasPracy, Przerwa, Urlop

# Register your models here.
admin.site.register(Pracownik)          #1
admin.site.register(CzasPracy)          #2
admin.site.register(Przerwa)            #3
admin.site.register(Urlop)              #4