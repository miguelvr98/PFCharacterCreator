# Generated by Django 3.0.3 on 2022-02-02 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20220202_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companeroanimalpersonaje',
            name='personaje',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='companero_animal_personaje', to='main.Personaje'),
        ),
    ]