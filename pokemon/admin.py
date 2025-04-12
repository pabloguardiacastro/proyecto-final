from django.contrib import admin

from pokemon.models import Pokemon, Type, TypeEffectiveness, Ability, Move

admin.site.register(Type)
admin.site.register(TypeEffectiveness)
admin.site.register(Ability)
admin.site.register(Move)
admin.site.register(Pokemon)