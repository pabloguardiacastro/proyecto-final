from decimal import Decimal

from django.conf import settings
from django.db import models

class EggGroup(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Grupo Huevo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Grupo Huevo"
        verbose_name_plural = "Grupos Huevo"


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Tipo")
    rgb = models.CharField(max_length=7, verbose_name="Color HEX", help_text="Ejemplo: #FF0000", default='#FFFFFF')
    icon = models.ImageField(upload_to='img/types', verbose_name="Icono del Tipo", default='img/types/default_icon.png')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'



class TypeEffectiveness(models.Model):
    MULTIPLIER_CHOICES = [
        (Decimal('0.0'), '0x'),
        (Decimal('0.5'), '0.5x'),
        (Decimal('1.0'), '1x'),
        (Decimal('2.0'), '2x'),
    ]
    attacking_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='ventajas_ofensivas', verbose_name="Tipo Atacante")
    defending_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='ventajas_defensivas', verbose_name="Tipo Defensor")
    multiplier = models.DecimalField(max_digits=3, decimal_places=2, choices=MULTIPLIER_CHOICES, default=Decimal('1.0'), verbose_name="Multiplicador")

    class Meta:
        verbose_name = 'Efectividad de Tipo'
        verbose_name_plural = 'Efectividades de Tipos'
        constraints = [models.UniqueConstraint(fields=['attacking_type', 'defending_type'], name='unique_type_effectiveness')]

    def __str__(self):
        return f"{self.attacking_type} → {self.defending_type}: x{self.multiplier}"


class Ability(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Habilidad")
    description = models.TextField(verbose_name="Descripción de la Habilidad")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'


class Move(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('status', 'Estado'),
        ('physical', 'Físico'),
        ('special', 'Especial'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nombre del Movimiento")
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE_CHOICES, verbose_name="Tipo de Movimiento")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Tipo del Movimiento")
    power = models.PositiveIntegerField(default=0, verbose_name="Poder")
    accuracy = models.PositiveIntegerField(default=100, verbose_name="Precisión")
    description = models.TextField(blank=True, verbose_name="Descripción del Movimiento")

    def __str__(self):
        return f"{self.name} ({self.movement_type})"

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'


class Pokemon(models.Model):
    SEX_CHOICES = [
        ('male', 'Macho'),
        ('female', 'Hembra'),
        ('both', 'Macho/Hembra'),
        ('unknown', 'Desconocido'),
    ]

    pokedex_number = models.PositiveIntegerField(unique=True, null=True, blank=True, verbose_name="Número de la Pokédex")
    name = models.CharField(max_length=100, verbose_name="Nombre del Pokémon")
    pokedex_entry = models.TextField(verbose_name="Entrada de la Pokédex")
    generation = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Generación")
    hp = models.PositiveIntegerField(verbose_name="Vida")
    attack = models.PositiveIntegerField(verbose_name="Ataque")
    defense = models.PositiveIntegerField(verbose_name="Defensa")
    special_attack = models.PositiveIntegerField(verbose_name="Ataque Especial")
    special_defense = models.PositiveIntegerField(verbose_name="Defensa Especial")
    speed = models.PositiveIntegerField(verbose_name="Velocidad")
    normal_image = models.ImageField(upload_to='img/pokemons/', blank=True, null=True, verbose_name="Imagen Normal")
    #shiny_image = models.ImageField(upload_to='img/pokemons/shiny/', blank=True, null=True, verbose_name="Imagen Shiny")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso")
    height = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Altura")
    capture_rate = models.PositiveIntegerField(verbose_name="Ratio de Captura")
    gender = models.CharField(max_length=20, choices=SEX_CHOICES, verbose_name="Posibles géneros")
    egg_groups = models.ManyToManyField(EggGroup, verbose_name="Grupos Huevo")
    primary_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='pokemons_tipo_principal', verbose_name="Tipo Principal")
    secondary_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, related_name='pokemons_tipo_secundario', verbose_name="Tipo Secundario")
    moves = models.ManyToManyField('Move', verbose_name="Movimientos")
    primary_ability = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='primary_pokemons', verbose_name="Habilidad Principal", default=1)
    secondary_ability = models.ForeignKey(Ability, on_delete=models.SET_NULL, null=True, blank=True, related_name='secondary_pokemons', verbose_name="Habilidad Secundaria")
    hidden_ability = models.ForeignKey(Ability, on_delete=models.SET_NULL, null=True, blank=True, related_name='hidden_pokemons', verbose_name="Habilidad Oculta")
    evolution_method = models.TextField(null=True, blank=True, verbose_name="Método de Evolución")
    pre_evolution  = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='evolutions', verbose_name="Evoluciona de")
    #evolutions = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='pre_evolution', verbose_name="Evoluciona a")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Creador")

    def __str__(self):
        return f"{self.pokedex_number} - {self.name}"

    @property
    def base_stat_total(self):
        return sum([self.hp, self.attack, self.defense, self.special_attack, self.special_defense, self.speed])

    def get_base_pokemon(self):
        current = self
        while current.pre_evolution:
            current = current.pre_evolution
        return current

    def get_evolution_chain(self):
        return {
            'pokemon': self,
            'evolutions': [evo.get_evolution_chain() for evo in self.evolutions.all()]
        }

    def get_full_chain(self):
        base = self.get_base_pokemon()
        return base.get_evolution_chain()

    class Meta:
        verbose_name = 'Pokémon'
        verbose_name_plural = 'Pokemons'

class MegaEvolution(models.Model):
    base_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='megaevolutions', verbose_name="Pokémon Base")
    name = models.CharField(max_length=100, verbose_name="Nombre de Mega Evolución")
    normal_image = models.ImageField(upload_to='img/pokemons/megaevolutions/', verbose_name="Imagen Mega Evolución Normal")
    #shiny_image = models.ImageField(upload_to='img/pokemons/megaevolutions/shiny/', verbose_name="Imagen Mega Evolución Shiny")
    hp = models.PositiveIntegerField(verbose_name="Vida")
    attack = models.PositiveIntegerField(verbose_name="Ataque")
    defense = models.PositiveIntegerField(verbose_name="Defensa")
    special_attack = models.PositiveIntegerField(verbose_name="Ataque Especial")
    special_defense = models.PositiveIntegerField(verbose_name="Defensa Especial")
    speed = models.PositiveIntegerField(verbose_name="Velocidad")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso")
    height = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Altura")
    primary_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='megas_tipo_principal', verbose_name="Tipo Principal")
    secondary_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, related_name='megas_tipo_secundario', verbose_name="Tipo Secundario")
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE, verbose_name="Habilidad")
    evolution_method = models.TextField(null=True, blank=True, verbose_name="Método de Mega Evolución")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Creador")


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Mega Evolución"
        verbose_name_plural = "Mega Evoluciones"