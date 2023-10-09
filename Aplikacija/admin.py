
from django.contrib import admin

# Register your models here.

from .models import *
'''
            Implementirao: Bogdan Radosavljevic, 2020/0109
            Fajl u kome su registrovane sve tabele iz baze za administratora
'''

admin.site.register(Dogadjaj)
admin.site.register(Sport)
admin.site.register(Pozoriste)
admin.site.register(Muzika)
admin.site.register(Zurka)
admin.site.register(Ostalo)
admin.site.register(Recenzija)
admin.site.register(Korisnik)
admin.site.register(Grad)
admin.site.register(ProdajnoMesto)
admin.site.register(Karta)
admin.site.register(Upit)