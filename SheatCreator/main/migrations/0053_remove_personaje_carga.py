# Generated by Django 3.0.3 on 2021-12-21 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_remove_personaje_iniciativa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaje',
            name='carga',
        ),
    ]