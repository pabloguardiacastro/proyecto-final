from django import forms

from pokemon.models import Pokemon


class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['normal_image', 'name', 'gender', 'weight', 'height', 'primary_type', 'secondary_type', 'primary_ability', 'secondary_ability', 'hidden_ability', 'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']