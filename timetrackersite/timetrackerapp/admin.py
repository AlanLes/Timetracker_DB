from django.contrib import admin
from .models import Pracownik, CzasPracy, Przerwa

# Register your models here.
admin.site.register(Pracownik)          #1
admin.site.register(CzasPracy)          #2
admin.site.register(Przerwa)            #3