# Generated by Django 5.0.6 on 2024-06-10 02:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacao', '0003_alter_partida_data_partida'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='tempo_inicio',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partida',
            name='tempo_total',
            field=models.DurationField(default=0),
        ),
    ]
