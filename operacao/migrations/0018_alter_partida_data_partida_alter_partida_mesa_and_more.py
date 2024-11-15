# Generated by Django 5.0.6 on 2024-07-27 06:46

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacao', '0017_alter_partida_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partida',
            name='data_partida',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='partida',
            name='mesa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partidas', to='operacao.mesa'),
        ),
        migrations.AlterField(
            model_name='partida',
            name='tempo_total',
            field=models.DurationField(default=datetime.timedelta),
        ),
    ]
