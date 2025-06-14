from django import forms

from pokemon.models import Pokemon, MegaEvolution, Move


class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['normal_image', 'name', 'gender', 'weight', 'height', 'primary_type', 'secondary_type', 'primary_ability', 'secondary_ability', 'hidden_ability', 'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']

class MegaEvolutionForm(forms.ModelForm):
    class Meta:
        model = MegaEvolution
        exclude = ['base_pokemon', 'creator']

class EditMovesForm(forms.ModelForm):
    moves = forms.ModelMultipleChoiceField(
        queryset=Move.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Movimientos"
    )

    class Meta:
        model = Pokemon
        fields = ['moves']

class PokemonEditForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        exclude = ['moves', 'creator', 'pokedex_number', 'pokedex_entry', 'generation', 'evolution_method', 'pre_evolution']