from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PokemonForm
from .models import Pokemon, Type, TypeEffectiveness, MegaEvolution
from .utils import calculate_combined_effectiveness


def pokedex_view(request):
    pokemons = Pokemon.objects.all().order_by('pokedex_number')
    return render(request, 'pokemon/pokedex.html', {'pokemons': pokemons})

def pokemon_view(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    combined_effectiveness = calculate_combined_effectiveness(pokemon.primary_type, pokemon.secondary_type)

    chain = pokemon.get_full_chain()

    immunities = []
    resistances = []
    super_resistances = []
    neutral = []
    weaknesses = []
    super_weaknesses = []

    for defender_type, multiplier in combined_effectiveness.items():
        if multiplier == 0:
            immunities.append(defender_type)
        elif multiplier == 0.25:
            super_resistances.append(defender_type)
        elif multiplier == 0.5:
            resistances.append(defender_type)
        elif multiplier == 1:
            neutral.append(defender_type)
        elif multiplier == 2:
            weaknesses.append(defender_type)
        elif multiplier == 4:
            super_weaknesses.append(defender_type)

    context = {
        'pokemon': pokemon,
        'chain': chain,
        'immunities': immunities,
        'super_resistances': super_resistances,
        'resistances': resistances,
        'neutral': neutral,
        'weaknesses': weaknesses,
        'super_weaknesses': super_weaknesses,
    }
    return render(request, 'pokemon/pokemon_detail.html', context)

def megaevolution_view(request, megaevolution_id):
    pokemon = get_object_or_404(MegaEvolution, id=megaevolution_id)
    combined_effectiveness = calculate_combined_effectiveness(pokemon.primary_type, pokemon.secondary_type)

    immunities = []
    resistances = []
    super_resistances = []
    neutral = []
    weaknesses = []
    super_weaknesses = []

    for defender_type, multiplier in combined_effectiveness.items():
        if multiplier == 0:
            immunities.append(defender_type)
        elif multiplier == 0.25:
            super_resistances.append(defender_type)
        elif multiplier == 0.5:
            resistances.append(defender_type)
        elif multiplier == 1:
            neutral.append(defender_type)
        elif multiplier == 2:
            weaknesses.append(defender_type)
        elif multiplier == 4:
            super_weaknesses.append(defender_type)

    context = {
        'pokemon': pokemon,
        'immunities': immunities,
        'super_resistances': super_resistances,
        'resistances': resistances,
        'neutral': neutral,
        'weaknesses': weaknesses,
        'super_weaknesses': super_weaknesses,
    }
    return render(request, 'pokemon/pokemon_detail.html', context)

@login_required
def pokemon_creation(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES)
        if form.is_valid():
            pokemon = form.save(commit=False)
            pokemon.creator = request.user
            pokemon.save()
            return redirect('pokemon:pokemon', pokemon_id=pokemon.id)
    else:
        form = PokemonForm()
    return render(request, 'pokemon/create.html', {'form': form})

def type_table(request):
    types = Type.objects.all()
    effectiveness = TypeEffectiveness.objects.all()

    context = {
        'types': types,
        'effectiveness': effectiveness,
    }

    return render(request, 'pokemon/type_table.html', context)