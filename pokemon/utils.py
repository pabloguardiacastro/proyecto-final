from pokemon.models import Type, TypeEffectiveness


def calculate_combined_effectiveness(primary_type, secondary_type=None):
    eff_map = {(e.attacking_type.id, e.defending_type.id): e.multiplier for e in TypeEffectiveness.objects.all()}
    types = Type.objects.all()

    combined = {}

    for attacker in types:
        m1 = eff_map.get((attacker.id, primary_type.id), 1)
        m2 = eff_map.get((attacker.id, secondary_type.id), 1) if secondary_type else 1
        combined[attacker] = m1 * m2

    return combined
