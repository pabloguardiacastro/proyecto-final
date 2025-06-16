from django.urls import path
from . import views

app_name = 'pokemon'

urlpatterns = [
    path('', views.pokedex_view, name='pokedex'),
    path('type-table/', views.type_table, name='type_table'),
    path('profile/<username>/', views.profile_view, name='profile'),
    path('pokemon/new/', views.pokemon_creation, name='new_pokemon'),
    path('pokemon/<pokemon_id>/', views.pokemon_view, name='pokemon'),
    path('pokemon/<pokemon_id>/edit/', views.edit_pokemon, name='edit_pokemon'),
    path('pokemon/<pokemon_id>/edit-moves/', views.edit_moves, name='edit_moves'),
    path('pokemon/<pokemon_id>/evolution/new/', views.evolution_creation, name='new_evolution'),
    path('pokemon/<pokemon_id>/mega/new/', views.megaevolution_creation, name='new_megaevolution'),
    path('megaevolution/<megaevolution_id>/', views.megaevolution_view, name='megaevolution'),
    path('megaevolution/<megaevolution_id>/edit/', views.edit_megaevolution, name='edit_megaevolution'),
    path('moves/<move_id>/', views.move_view, name='move'),
    path('abilities/<ability_id>/', views.ability_view, name='ability'),
    path('search/<content>/', views.search_view, name='search'),
]