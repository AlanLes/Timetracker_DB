from django.contrib import admin
from .models import Przerwa, CzasPracy, Pracownik, DzienPracownika, Urlop

# Register your models here.
admin.site.register(Przerwa)            #2
admin.site.register(CzasPracy)          #3
admin.site.register(Pracownik)          #4
admin.site.register(DzienPracownika)    #5
admin.site.register(Urlop)              #6