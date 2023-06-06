from django.contrib import admin
from .models import *

"""
    Author: Jelena Cvetic 2020/0305
    Giving admin privileges to edit Recenzije, Tag, Upitnikpitanje and Upitnikodgovor tables.
"""

admin.site.register(Recenzija)
admin.site.register(Tag)
admin.site.register(Upitnikpitanje)
admin.site.register(Upitnikodgovor)
