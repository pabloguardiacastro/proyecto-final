# Generated by Django 5.1.7 on 2025-04-12 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Habilidad',
            new_name='Ability',
        ),
        migrations.RenameModel(
            old_name='Movimiento',
            new_name='Move',
        ),
        migrations.RenameModel(
            old_name='Tipo',
            new_name='Type',
        ),
        migrations.RenameModel(
            old_name='EfectividadTipo',
            new_name='TypeEffectiveness',
        ),
    ]
