from django.urls import path
from . import views

app_name = 'pokemon'

urlpatterns = [
    path('pokedex/', views.pokedex_view, name='pokedex'),
    path('type-table/', views.type_table, name='type_table'),
]