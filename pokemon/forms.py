from django import forms

from pokemon.models import Pokemon, MegaEvolution, Move, Comment


class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['normal_image', 'name', 'gender', 'weight', 'height', 'primary_type', 'secondary_type', 'primary_ability', 'secondary_ability', 'hidden_ability', 'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']

class PokemonEvolutionForm(PokemonForm):
    class Meta(PokemonForm.Meta):
        fields = PokemonForm.Meta.fields + ['evolution_method']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evolution_method'].required = True

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario aquí...', 'style': 'width: 100%;'})}
        labels = {'text': ''}