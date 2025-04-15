from django.contrib import admin

from pokemon.models import Pokemon, Type, TypeEffectiveness, Ability, Move, MegaEvolution, EggGroup

admin.site.register(EggGroup)
admin.site.register(Type)
admin.site.register(TypeEffectiveness)
admin.site.register(Ability)
admin.site.register(Move)
admin.site.register(Pokemon)
admin.site.register(MegaEvolution)