# Generated by Django 5.0.6 on 2024-06-10 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jogador',
            name='data_nascimento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
