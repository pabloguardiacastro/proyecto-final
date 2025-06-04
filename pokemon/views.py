from django.shortcuts import render
from .models import Pokemon, Type, TypeEffectiveness


def pokedex_view(request):
    pokemons = Pokemon.objects.all().order_by('pokedex_number')
    return render(request, 'pokemon/pokedex.html', {'pokemons': pokemons})


def type_table(request):
    types = Type.objects.all()
    effectiveness = TypeEffectiveness.objects.all()

    context = {
        'types': types,
        'effectiveness': effectiveness,
    }

    return render(request, 'pokemon/type_table.html', context)