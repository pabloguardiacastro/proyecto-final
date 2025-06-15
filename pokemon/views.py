from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PokemonForm, MegaEvolutionForm, EditMovesForm, PokemonEditForm, PokemonEvolutionForm, CommentForm
from .models import Pokemon, Type, TypeEffectiveness, MegaEvolution, Move, Ability
from .utils import calculate_combined_effectiveness


def pokedex_view(request):
    pokemons = Pokemon.objects.all().order_by('pokedex_number')
    megaevolutions = MegaEvolution.objects.all().order_by('base_pokemon__pokedex_number')
    return render(request, 'pokemon/pokedex.html', {
        'pokemons': pokemons,
        'megaevolutions': megaevolutions,
    })

def pokemon_view(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.pokemon = pokemon
            comment.save()
            return redirect('pokemon:pokemon', pokemon_id=pokemon.id)
    else:
        form = CommentForm()

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
        'form': form,
    }

    return render(request, 'pokemon/pokemon_detail.html', context)

def megaevolution_view(request, megaevolution_id):
    pokemon = get_object_or_404(MegaEvolution, id=megaevolution_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.megaevolution = pokemon
            comment.save()
            return redirect('pokemon:megaevolution', megaevolution_id=pokemon.id)
    else:
        form = CommentForm()

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
        'form': form,
    }
    return render(request, 'pokemon/pokemon_detail.html', context)

def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    pokemons = Pokemon.objects.filter(creator=user_profile)
    megaevolutions = MegaEvolution.objects.filter(creator=user_profile)
    return render(request, 'pokemon/profile.html', {
        'pokemons': pokemons,
        'megaevolutions': megaevolutions,
        'user_profile': user_profile,
    })

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

@login_required
def evolution_creation(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    initial_data = {
        'hp': pokemon.hp,
        'attack': pokemon.attack,
        'defense': pokemon.defense,
        'special_attack': pokemon.special_attack,
        'special_defense': pokemon.special_defense,
        'speed': pokemon.speed,
        'weight': pokemon.weight,
        'height': pokemon.height,
        'primary_type': pokemon.primary_type,
        'secondary_type': pokemon.secondary_type,
        'primary_ability': pokemon.primary_ability,
        'secondary_ability': pokemon.secondary_ability,
        'hidden_ability': pokemon.hidden_ability,
    }

    if request.method == 'POST':
        form = PokemonEvolutionForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.pre_evolution = pokemon
            new.creator = request.user
            new.save()
            return redirect('pokemon:pokemon', pokemon_id=new.id)
    else:
        form = PokemonEvolutionForm(initial=initial_data)

    return render(request, 'pokemon/create.html', {
        'form': form,
    })

@login_required
def megaevolution_creation(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    initial_data = {
        'name': "Mega " + pokemon.name,
        'hp': pokemon.hp,
        'attack': pokemon.attack,
        'defense': pokemon.defense,
        'special_attack': pokemon.special_attack,
        'special_defense': pokemon.special_defense,
        'speed': pokemon.speed,
        'weight': pokemon.weight,
        'height': pokemon.height,
        'primary_type': pokemon.primary_type,
        'secondary_type': pokemon.secondary_type,
        'ability': pokemon.primary_ability,
    }

    if request.method == 'POST':
        form = MegaEvolutionForm(request.POST, request.FILES)
        if form.is_valid():
            mega = form.save(commit=False)
            mega.base_pokemon = pokemon
            mega.creator = request.user
            mega.save()
            return redirect('pokemon:megaevolution', megaevolution_id=mega.id)
    else:
        form = MegaEvolutionForm(initial=initial_data)

    return render(request, 'pokemon/create_megaevolution.html', {
        'form': form,
        'pokemon': pokemon,
    })

@login_required
def edit_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    if request.user != pokemon.creator:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PokemonEditForm(request.POST, request.FILES, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('pokemon:pokemon', pokemon_id=pokemon.id)
    else:
        form = PokemonEditForm(instance=pokemon)

    return render(request, 'pokemon/edit.html', {'form': form, 'pokemon': pokemon})

@login_required
def edit_moves(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    if pokemon.creator != request.user:
        return redirect('pokemon:pokemon', pokemon_id=pokemon.id)

    if request.method == 'POST':
        form = EditMovesForm(request.POST, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('pokemon:pokemon', pokemon_id=pokemon.id)
    else:
        form = EditMovesForm(instance=pokemon)

    return render(request, 'pokemon/edit_moves.html', {'form': form, 'pokemon': pokemon})

def type_table(request):
    types = Type.objects.all()
    effectiveness = TypeEffectiveness.objects.all()

    context = {
        'types': types,
        'effectiveness': effectiveness,
    }

    return render(request, 'pokemon/type_table.html', context)

def move_view(request, move_id):
    move = get_object_or_404(Move, id=move_id)
    return render(request, 'pokemon/move_detail.html', {'move': move})

def ability_view(request, ability_id):
    ability = get_object_or_404(Ability, id=ability_id)
    return render(request, 'pokemon/ability_detail.html', {'ability': ability})