# Generated by Django 3.2.4 on 2021-11-12 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BonificacionRaza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(null=True, verbose_name='Nombre')),
                ('descripcion', models.TextField(null=True, verbose_name='Descripción')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clase', models.TextField(verbose_name='Clase')),
                ('nivel', models.IntegerField(default=1, verbose_name='Nivel')),
                ('dadosDeGolpe', models.IntegerField(default=6, verbose_name='Dados de golpe')),
                ('ataqueBase', models.TextField(verbose_name='Ataque base')),
                ('fortaleza', models.IntegerField(verbose_name='Fortaleza')),
                ('reflejos', models.IntegerField(verbose_name='Reflejos')),
                ('voluntad', models.IntegerField(verbose_name='Fortaleza')),
                ('rafagaDeGolpes', models.TextField(null=True, verbose_name='Ráfaga de golpes')),
                ('danoDesarmado', models.TextField(null=True, verbose_name='Daño desarmado')),
                ('bonificacionAc', models.IntegerField(null=True, verbose_name='Bonificación AC')),
                ('movimientoRapido', models.IntegerField(null=True, verbose_name='Movimiento rápido')),
            ],
            options={
                'ordering': ('clase',),
            },
        ),
        migrations.CreateModel(
            name='CompaneroAnimal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('nivel', models.IntegerField(verbose_name='Nivel')),
                ('dadosDeGolpe', models.IntegerField(verbose_name='Dados de golpe')),
                ('puntosDeGolpe', models.IntegerField(verbose_name='Puntos de golpe')),
                ('tamano', models.TextField(verbose_name='Tamaño')),
                ('velocidad', models.TextField(verbose_name='Velocidad')),
                ('ca', models.IntegerField(verbose_name='Clase de armadura')),
                ('ataqueBase', models.IntegerField(verbose_name='Ataque base')),
                ('ataque', models.TextField(verbose_name='Ataque')),
                ('fuerza', models.IntegerField(verbose_name='Fuerza')),
                ('destreza', models.IntegerField(verbose_name='Destreza')),
                ('constitucion', models.IntegerField(verbose_name='Constitución')),
                ('inteligencia', models.IntegerField(verbose_name='Inteligencia')),
                ('sabiduria', models.IntegerField(verbose_name='Sabiduría')),
                ('carisma', models.IntegerField(verbose_name='Carisma')),
                ('fortaleza', models.IntegerField(verbose_name='Fortaleza')),
                ('reflejos', models.IntegerField(verbose_name='Reflejos')),
                ('voluntad', models.IntegerField(verbose_name='Voluntad')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Conjuro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('nivel', models.IntegerField(verbose_name='Nivel')),
                ('escuela', models.TextField(verbose_name='Escuela')),
                ('tiempoDeLanzamiento', models.TextField(verbose_name='Tiempo de lanzamiento')),
                ('alcance', models.TextField(verbose_name='Alcance')),
                ('efecto', models.TextField(null=True, verbose_name='Efecto')),
                ('objetivo', models.TextField(null=True, verbose_name='Objetivo')),
                ('duracion', models.TextField(verbose_name='Duración')),
                ('tiroDeSalvacion', models.BooleanField(verbose_name='Tiro de salvación')),
                ('resistenciaConjuros', models.BooleanField(verbose_name='Resistencia a conjuros')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
            ],
            options={
                'ordering': ('nivel', 'nombre'),
            },
        ),
        migrations.CreateModel(
            name='Dote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Dote')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('tipo', models.TextField(null=True, verbose_name='Tipo')),
                ('nivel', models.IntegerField(null=True, verbose_name='Nivel')),
                ('ataqueBase', models.IntegerField(null=True, verbose_name='Ataque base')),
                ('fuerza', models.IntegerField(null=True, verbose_name='Fuerza')),
                ('destreza', models.IntegerField(null=True, verbose_name='Destreza')),
                ('constitucion', models.IntegerField(null=True, verbose_name='Constitución')),
                ('inteligencia', models.IntegerField(null=True, verbose_name='Inteligencia')),
                ('sabiduria', models.IntegerField(null=True, verbose_name='Sabiduría')),
                ('carisma', models.IntegerField(null=True, verbose_name='Carisma')),
                ('esDoteCompaneroAnimal', models.BooleanField(default=False, verbose_name='Es dote de compañero animal')),
                ('prerrequisitoDote', models.ManyToManyField(related_name='_main_dote_prerrequisitoDote_+', to='main.Dote')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Especial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('nivel', models.IntegerField(null=True, verbose_name='Nivel')),
                ('esEspecialCompaneroAnimal', models.BooleanField(verbose_name='Es especial de compañero animal')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Habilidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habilidad', models.TextField(verbose_name='Habilidad')),
                ('caracteristica', models.TextField(null=True, verbose_name='Característica')),
            ],
            options={
                'ordering': ('habilidad',),
            },
        ),
        migrations.CreateModel(
            name='Idioma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idioma', models.TextField(verbose_name='Idioma')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Inmune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inmune', models.TextField(verbose_name='Inmune')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipado', models.BooleanField(verbose_name='Está equipado')),
            ],
        ),
        migrations.CreateModel(
            name='NivelConjuroDiario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Objeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clase', models.TextField(null=True, verbose_name='Clase')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('peso', models.IntegerField(null=True, verbose_name='Peso')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.TextField(verbose_name='Nickname')),
                ('esAdmin', models.BooleanField(default=False, verbose_name='Admin')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('coste', models.IntegerField(null=True, verbose_name='Coste')),
                ('costeDinero', models.IntegerField(null=True, verbose_name='Coste dinero')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Arma',
            fields=[
                ('objeto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.objeto')),
                ('danoP', models.TextField(verbose_name='Daño P')),
                ('danoM', models.TextField(verbose_name='Daño M')),
                ('critico', models.TextField(verbose_name='Crítico')),
                ('alcance', models.TextField(null=True, verbose_name='Alcance')),
                ('tipo', models.TextField(verbose_name='Tipo')),
                ('especial', models.TextField(verbose_name='Especial')),
            ],
            options={
                'ordering': ('nombre',),
            },
            bases=('main.objeto',),
        ),
        migrations.CreateModel(
            name='Armadura',
            fields=[
                ('objeto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.objeto')),
                ('bonifArm', models.IntegerField(verbose_name='Bonificación armadura')),
                ('bonifMaxDes', models.IntegerField(verbose_name='Bonificación máximo destreza')),
                ('penalizArm', models.IntegerField(verbose_name='Penalizador armadura')),
                ('falloConjArc', models.IntegerField(verbose_name='Fallo conjuro arcano')),
                ('velocidad9m', models.IntegerField(verbose_name='Velocidad 9m')),
                ('velocidad6m', models.IntegerField(verbose_name='Velocidad 6m')),
            ],
            options={
                'ordering': ('nombre',),
            },
            bases=('main.objeto',),
        ),
        migrations.CreateModel(
            name='Truco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('cd', models.IntegerField(verbose_name='CD')),
                ('prerrequisitoTruco', models.ManyToManyField(related_name='_main_truco_prerrequisitoTruco_+', to='main.Truco')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Raza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raza', models.TextField(verbose_name='Raza')),
                ('tamano', models.TextField(null=True, verbose_name='Tamaño')),
                ('velocidad', models.TextField(null=True, verbose_name='Velocidad')),
                ('fuerza', models.IntegerField(null=True, verbose_name='Fuerza')),
                ('destreza', models.IntegerField(null=True, verbose_name='Destreza')),
                ('constitucion', models.IntegerField(null=True, verbose_name='Constitución')),
                ('inteligencia', models.IntegerField(null=True, verbose_name='Inteligencia')),
                ('sabiduria', models.IntegerField(null=True, verbose_name='Sabiduría')),
                ('carisma', models.IntegerField(null=True, verbose_name='Carisma')),
                ('bonificacionRaza', models.ManyToManyField(to='main.BonificacionRaza')),
                ('idiomas', models.ManyToManyField(to='main.Idioma')),
            ],
            options={
                'ordering': ('raza',),
            },
        ),
        migrations.CreateModel(
            name='PuntuacionHabilidadCA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField(verbose_name='Puntuación')),
                ('habilidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.habilidad')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='PuntuacionHabilidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField(null=True, verbose_name='Puntuación')),
                ('habilidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.habilidad')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Poder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('nivel', models.IntegerField(null=True, verbose_name='Nivel')),
                ('ataqueBase', models.IntegerField(null=True, verbose_name='Ataque base')),
                ('fuerza', models.IntegerField(null=True, verbose_name='Fuerza')),
                ('destreza', models.IntegerField(null=True, verbose_name='Destreza')),
                ('constitucion', models.IntegerField(null=True, verbose_name='Constitución')),
                ('inteligencia', models.IntegerField(null=True, verbose_name='Inteligencia')),
                ('sabiduria', models.IntegerField(null=True, verbose_name='Sabiduría')),
                ('carisma', models.IntegerField(null=True, verbose_name='Carisma')),
                ('prerrequisitoPoder', models.ManyToManyField(related_name='_main_poder_prerrequisitoPoder_+', to='main.Poder')),
            ],
            options={
                'ordering': ('nivel', 'nombre'),
            },
        ),
        migrations.CreateModel(
            name='Personaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('alineamiento', models.CharField(choices=[('LB', 'Legal Bueno'), ('LN', 'Legal Neutral'), ('LM', 'Legal Malo'), ('NB', 'Neutral Bueno'), ('N', 'Neutral'), ('NM', 'Neutral Malo'), ('CB', 'Caótico Bueno'), ('CN', 'Caótico Neutral'), ('CM', 'Caótico Malo')], max_length=2, null=True, verbose_name='alineamiento')),
                ('carga', models.TextField(null=True, verbose_name='Carga')),
                ('puntosDeGolpe', models.IntegerField(null=True, verbose_name='Puntos de golpe')),
                ('resistenciaDano', models.IntegerField(null=True, verbose_name='Resistencia al daño')),
                ('resistenciaConjuros', models.IntegerField(null=True, verbose_name='Resistencia a Conjuros')),
                ('claseArmadura', models.IntegerField(default=10, verbose_name='Clase de armadura')),
                ('desprevenido', models.IntegerField(default=10, verbose_name='Desprevenido')),
                ('toque', models.IntegerField(default=10, verbose_name='Toque')),
                ('bmc', models.IntegerField(default=10, verbose_name='Bonus maniobra de combate')),
                ('dmc', models.IntegerField(default=10, verbose_name='Defensa maniobra de combate')),
                ('fuerza', models.IntegerField(default=10, verbose_name='Fuerza')),
                ('destreza', models.IntegerField(default=10, verbose_name='Destreza')),
                ('constitucion', models.IntegerField(default=10, verbose_name='Constitución')),
                ('inteligencia', models.IntegerField(default=10, verbose_name='Inteligencia')),
                ('sabiduria', models.IntegerField(default=10, verbose_name='Sabiduría')),
                ('carisma', models.IntegerField(default=10, verbose_name='Carisma')),
                ('clase', models.ManyToManyField(to='main.Clase')),
                ('companeroAnimal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.companeroanimal')),
                ('dotes', models.ManyToManyField(to='main.Dote')),
                ('idiomas', models.ManyToManyField(to='main.Idioma')),
                ('inmune', models.ManyToManyField(to='main.Inmune')),
                ('inventario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.inventario')),
                ('objetos', models.ManyToManyField(to='main.Objeto')),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.perfil')),
                ('puntuacionesHabilidad', models.ManyToManyField(to='main.PuntuacionHabilidad')),
                ('raza', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.raza')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.AddField(
            model_name='objeto',
            name='propiedades',
            field=models.ManyToManyField(to='main.Propiedad'),
        ),
        migrations.AddField(
            model_name='companeroanimal',
            name='dotes',
            field=models.ManyToManyField(to='main.Dote'),
        ),
        migrations.AddField(
            model_name='companeroanimal',
            name='especial',
            field=models.ManyToManyField(to='main.Especial'),
        ),
        migrations.AddField(
            model_name='companeroanimal',
            name='puntuacionHabilidad',
            field=models.ManyToManyField(to='main.PuntuacionHabilidadCA'),
        ),
        migrations.AddField(
            model_name='companeroanimal',
            name='trucos',
            field=models.ManyToManyField(to='main.Truco'),
        ),
        migrations.AddField(
            model_name='clase',
            name='companeroAnimal',
            field=models.ManyToManyField(default=False, to='main.CompaneroAnimal'),
        ),
        migrations.AddField(
            model_name='clase',
            name='especiales',
            field=models.ManyToManyField(to='main.Especial'),
        ),
        migrations.AddField(
            model_name='clase',
            name='habilidad',
            field=models.ManyToManyField(to='main.Habilidad'),
        ),
        migrations.AddField(
            model_name='clase',
            name='nivelConjuroDiario',
            field=models.ManyToManyField(to='main.NivelConjuroDiario'),
        ),
        migrations.AddField(
            model_name='clase',
            name='poderes',
            field=models.ManyToManyField(to='main.Poder'),
        ),
    ]
