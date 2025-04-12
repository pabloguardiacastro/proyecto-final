from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Tipo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'


class TypeEffectiveness(models.Model):
    attacking_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='ventajas_ofensivas', verbose_name="Tipo Atacante")
    defending_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='ventajas_defensivas', verbose_name="Tipo Defensor")
    multiplier = models.FloatField(help_text="Por ejemplo: 2.0, 0.5, 0.0, 1.0", verbose_name="Multiplicador")

    class Meta:
        unique_together = ('attacking_type', 'defending_type')
        verbose_name = 'Efectividad de Tipo'
        verbose_name_plural = 'Efectividades de Tipos'

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
    power = models.PositiveIntegerField(verbose_name="Poder")
    description = models.TextField(blank=True, verbose_name="Descripción del Efecto Secundario")

    def __str__(self):
        return f"{self.name} ({self.movement_type})"

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'


class Pokemon(models.Model):
    SEX_CHOICES = [
        ('male', 'Macho'),
        ('female', 'Hembra'),
        ('both', 'Ambos'),
        ('unknown', 'Desconocido'),
    ]

    pokedex_number = models.PositiveIntegerField(unique=True, verbose_name="Número de la Pokédex")
    name = models.CharField(max_length=100, verbose_name="Nombre del Pokémon")
    pokedex_entry = models.TextField(verbose_name="Entrada de la Pokédex")
    hp = models.PositiveIntegerField(verbose_name="Vida")
    attack = models.PositiveIntegerField(verbose_name="Ataque")
    defense = models.PositiveIntegerField(verbose_name="Defensa")
    special_attack = models.PositiveIntegerField(verbose_name="Ataque Especial")
    special_defense = models.PositiveIntegerField(verbose_name="Defensa Especial")
    speed = models.PositiveIntegerField(verbose_name="Velocidad")
    normal_image = models.ImageField(upload_to='static/pokemons/normal/', blank=True, null=True, verbose_name="Imagen Normal")
    shiny_image = models.ImageField(upload_to='pokemons/pokemons/shiny/', blank=True, null=True, verbose_name="Imagen Shiny")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso")
    height = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Altura")
    capture_rate = models.PositiveIntegerField(verbose_name="Ratio de Captura")
    gender = models.CharField(max_length=20, choices=SEX_CHOICES, verbose_name="Posibles géneros")
    primary_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='pokemones_tipo_principal', verbose_name="Tipo Principal")
    secondary_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, related_name='pokemones_tipo_secundario', verbose_name="Tipo Secundario")

    def __str__(self):
        return f"{self.pokedex_number} - {self.name}"

    class Meta:
        verbose_name = 'Pokémon'
        verbose_name_plural = 'Pokemons'