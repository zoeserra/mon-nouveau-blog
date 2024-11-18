from django.contrib import admin
from .models import Equipement
from .models import Character
 
admin.site.register(Equipement)
admin.site.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id_character', 'etat', 'lieu', 'photo')  