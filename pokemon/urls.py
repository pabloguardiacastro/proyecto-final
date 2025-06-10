from django.urls import path
from . import views

app_name = 'pokemon'

urlpatterns = [
    path('pokedex/', views.pokedex_view, name='pokedex'),
    path('type-table/', views.type_table, name='type_table'),
    path('pokemon/new/', views.pokemon_creation, name='new_pokemon'),
    path('pokemon/<pokemon_id>/', views.pokemon_view, name='pokemon'),
    path('megaevolution/<megaevolution_id>/', views.megaevolution_view, name='megaevolution'),
]