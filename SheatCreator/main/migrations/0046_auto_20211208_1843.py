# Generated by Django 3.0.3 on 2021-12-08 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_auto_20211208_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='especial',
            name='clase_perteneciente',
        ),
        migrations.AddField(
            model_name='clase',
            name='descripcion_dados_de_golpe',
            field=models.TextField(null=True, verbose_name='Dado de golpe'),
        ),
        migrations.AddField(
            model_name='clase',
            name='descripcion_habilidades',
            field=models.TextField(null=True, verbose_name='Competente con las habilidades'),
        ),
        migrations.AddField(
            model_name='clase',
            name='descripcion_puntos_de_habilidad',
            field=models.TextField(null=True, verbose_name='Puntos de habilidad por nivel'),
        ),
        migrations.AlterField(
            model_name='clase',
            name='puntos_de_habilidad_por_nivel',
            field=models.TextField(null=True, verbose_name='Puntos de habilidad'),
        ),
    ]