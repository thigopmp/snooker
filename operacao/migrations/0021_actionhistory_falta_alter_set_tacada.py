# Generated by Django 5.0.6 on 2024-08-03 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacao', '0020_alter_set_tacada'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionhistory',
            name='falta',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='set',
            name='tacada',
            field=models.IntegerField(default=0),
        ),
    ]
