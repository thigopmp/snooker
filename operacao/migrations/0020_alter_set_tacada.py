# Generated by Django 5.0.6 on 2024-08-03 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacao', '0019_set_tacada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='tacada',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
