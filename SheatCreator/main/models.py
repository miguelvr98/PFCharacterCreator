from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    nickname = models.TextField(verbose_name='Nickname')
    esAdmin = models.BooleanField(verbose_name='Admin', default=False)

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ('pk', )

class Personaje(models.Model):
    perfil = models.ForeignKey('Perfil', on_delete=models.CASCADE, null=False)
    nombre = models.TextField(verbose_name='Nombre')
    
    class Alineamiento(models.TextChoices):
        LB = 'LB', 'Legal Bueno'
        LN = 'LN', 'Legal Neutral'
        LM = 'LM', 'Legal Malo'
        NB = 'NB', 'Neutral Bueno'
        N = 'N', 'Neutral'
        NM = 'NM', 'Neutral Malo'
        CB = 'CB', 'Caótico Bueno'
        CN = 'CN', 'Caótico Neutral'
        CM = 'CM', 'Caótico Malo'
    alineamiento = models.CharField(verbose_name='alineamiento', 
    max_length=2, choices=Alineamiento.choices, null=True)
    carga = models.TextField(verbose_name='Carga', null=True)
    puntosDeGolpe = models.IntegerField(verbose_name='Puntos de golpe',
    null=True)
    resistenciaDano = models.IntegerField(verbose_name='Resistencia al daño',
    null=True)
    resistenciaConjuros = models.IntegerField(verbose_name='Resistencia a Conjuros',
    null=True)
    claseArmadura = models.IntegerField(verbose_name='Clase de armadura',
    default=10)
    desprevenido = models.IntegerField(verbose_name='Desprevenido',
    default=10)
    toque = models.IntegerField(verbose_name='Toque', default=10)
    bmc = models.IntegerField(verbose_name='Bonus maniobra de combate',
    default=10)
    dmc = models.IntegerField(verbose_name='Defensa maniobra de combate',
    default=10)
    fuerza = models.IntegerField(verbose_name='Fuerza', default=10)
    destreza = models.IntegerField(verbose_name='Destreza', default=10)
    constitucion = models.IntegerField(verbose_name='Constitución',
     default=10)
    inteligencia = models.IntegerField(verbose_name='Inteligencia',
     default=10)
    sabiduria = models.IntegerField(verbose_name='Sabiduría',
     default=10)
    carisma = models.IntegerField(verbose_name='Carisma', default=10)
    idiomas = models.ManyToManyField('Idioma')
    inmune = models.ManyToManyField('Inmune')
    raza = models.ForeignKey('Raza', on_delete=models.CASCADE, null=True)
    clase = models.ManyToManyField('Clase')
    dotes = models.ManyToManyField('Dote')
    puntuacionesHabilidad = models.ManyToManyField('PuntuacionHabilidad')
    inventario = models.ForeignKey('Inventario', on_delete=models.CASCADE, null=True)
    companeroAnimal = models.ForeignKey('CompaneroAnimal', on_delete=models.CASCADE, null=True)
    objetos = models.ManyToManyField('Objeto')


    def BonificadorFuerza(self):
        return int((fuerza-10)/2)
    
    def BonificadorDestreza(self):
        return int((destreza-10)/2)

    def BonificadorConstitucion(self):
        return int((constitucion-10)/2)

    def BonificadorInteligencia(self):
        return int((inteligencia-10)/2)

    def BonificadorSabiduria(self):
        return int((sabiduria-10)/2)

    def BonificadorCarisma(self):
        return int((carisma-10)/2)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('pk', )

    class Idioma(models.Model):
        idioma = models.TextField(verbose_name='Idioma')

        def __str__(self):
            return self.idioma

        class Meta:
            ordering = ('pk', )

    class Inmune(models.Model):
        inmune = models.TextField(verbose_name='Inmune')

        def __str__(self):
            return self.inmune

        class Meta:
            ordering = ('pk', )

    class Raza(models.Model):
        raza = models.TextField(verbose_name='Raza')
        tamano = models.TextField(verbose_name='Tamaño', null=True)
        velocidad = models.TextField(verbose_name='Velocidad', null=True)
        fuerza = models.IntegerField(verbose_name='Fuerza', null=True)
        destreza = models.IntegerField(verbose_name='Destreza', null=True)
        constitucion = models.IntegerField(verbose_name='Constitución', null=True)
        inteligencia = models.IntegerField(verbose_name='Inteligencia', null=True)
        sabiduria = models.IntegerField(verbose_name='Sabiduría', null=True)
        carisma = models.IntegerField(verbose_name='Carisma', null=True)
        bonificacionRaza = models.ManyToManyField('BonificacionRaza')
        idiomas = models.ManyToManyField('Idioma')

        def __str__(self):
            return self.raza

        class Meta:
            ordering = ('raza', )

    class BonificacionRaza(models.Model):
        nombre = models.TextField(verbose_name='Nombre', null=True)
        descripcion = models.TextField(verbose_name='Descripción', null=True)

        def __str__(self):
            return self.nombre

        class Meta:
            ordering = ('pk', )

    class PuntuacionHabilidad(models.Model):
        puntuacion = models.IntegerField(verbose_name='Puntuación',
        null=True)
        habilidad = models.ForeignKey('Habilidad', on_delete=models.CASCADE)

        def __str__(self):
            return self.habilidad.habilidad
        
        class Meta:
            ordering = ('pk', )

    class Habilidad(models.Model):
        habilidad = models.TextField(verbose_name='Habilidad')
        caracteristica = models.TextField(verbose_name='Característica', null=True)

        def __str__(self):
            return self.habilidad

        class Meta:
            ordering = ('habilidad', )

    class Clase(models.Model):
        clase = models.TextField(verbose_name='Clase')
        nivel = models.IntegerField(verbose_name='Nivel', default=1)
        dadosDeGolpe = models.IntegerField(verbose_name='Dados de golpe',
        default=6)
        ataqueBase = models.TextField(verbose_name='Ataque base',
         null=False)
        fortaleza = models.IntegerField(verbose_name='Fortaleza', 
        null=False)
        reflejos = models.IntegerField(verbose_name='Reflejos', null=False)
        voluntad = models.IntegerField(verbose_name='Fortaleza', null=False)
        rafagaDeGolpes = models.TextField(verbose_name='Ráfaga de golpes', null=True)
        danoDesarmado = models.TextField(verbose_name='Daño desarmado', null = True)
        bonificacionAc = models.IntegerField(verbose_name='Bonificación AC', null = True)
        movimientoRapido = models.IntegerField(verbose_name='Movimiento rápido', null =True)
        nivelConjuroDiario = models.ManyToManyField('NivelConjuroDiario')
        poderes = models.ManyToManyField('Poder')
        especiales = models.ManyToManyField('Especial')
        companeroAnimal = models.ManyToManyField('CompaneroAnimal', default=False)
        habilidad = models.ManyToManyField('Habilidad')

        def __str__(self):
            return self.clase

        class Meta:
            ordering = ('clase', )
    
    class Dote(models.Model):
        nombre = models.TextField(verbose_name='Dote')
        descripcion = models.TextField(verbose_name='Descripcion')
        tipo = models.TextField(verbose_name='Tipo', null=True)
        nivel = models.IntegerField(verbose_name='Nivel', null=True)
        ataqueBase = models.IntegerField(verbose_name='Ataque base', null=True)
        fuerza = models.IntegerField(verbose_name='Fuerza', null=True)
        destreza = models.IntegerField(verbose_name='Destreza', null=True)
        constitucion = models.IntegerField(verbose_name='Constitución', null=True)
        inteligencia = models.IntegerField(verbose_name='Inteligencia', null=True)
        sabiduria = models.IntegerField(verbose_name='Sabiduría', null=True)
        carisma = models.IntegerField(verbose_name='Carisma', null=True)
        esDoteCompaneroAnimal = models.BooleanField(verbose_name='Es dote de compañero animal', default=False)
        prerrequisitoDote = models.ManyToManyField('self')
    
        def __str__(self):
            return self.nombre
        
        class Meta: 
            ordering = ('nombre', )

    class Conjuro(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        nivel = models.IntegerField(verbose_name='Nivel')
        escuela = models.TextField(verbose_name='Escuela')
        tiempoDeLanzamiento = models.TextField(verbose_name='Tiempo de lanzamiento')
        alcance = models.TextField(verbose_name='Alcance')
        efecto = models.TextField(verbose_name='Efecto', null=True)
        objetivo = models.TextField(verbose_name='Objetivo', null=True)
        duracion = models.TextField(verbose_name='Duración')
        tiroDeSalvacion = models.BooleanField(verbose_name='Tiro de salvación')
        resistenciaConjuros = models.BooleanField(verbose_name='Resistencia a conjuros')
        descripcion = models.TextField(verbose_name='Descripción')

        def __str__(self):
            return self.nombre

        class Meta:
            ordering = ('nivel', 'nombre', )

    class Poder(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        descripcion = models.TextField(verbose_name='Descripción')
        nivel = models.IntegerField(verbose_name='Nivel', null=True)
        ataqueBase = models.IntegerField(verbose_name='Ataque base', null=True)
        fuerza = models.IntegerField(verbose_name='Fuerza', null=True)
        destreza = models.IntegerField(verbose_name='Destreza', null=True)
        constitucion = models.IntegerField(verbose_name='Constitución', null=True)
        inteligencia = models.IntegerField(verbose_name='Inteligencia', null=True)
        sabiduria = models.IntegerField(verbose_name='Sabiduría', null=True)
        carisma = models.IntegerField(verbose_name='Carisma', null=True)
        prerrequisitoPoder = models.ManyToManyField('self')

        def __str__(self):
            return nombre
        
        class Meta:
            ordering = ('nivel', 'nombre', )

    class NivelConjuroDiario(models.Model):
        cantidad = models.IntegerField(verbose_name='Cantidad')

        def __str__(self):
            return cantidad
        
        class Meta:
            ordering = ('pk', )

    class Especial(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        descripcion = models.TextField(verbose_name='Descripción')
        nivel = models.IntegerField(verbose_name='Nivel', null=True)
        esEspecialCompaneroAnimal = models.BooleanField(verbose_name='Es especial de compañero animal')

        def __str__(self):
            return nombre
        
        class Meta:
            ordering = ('nombre', )

    class CompaneroAnimal(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        nivel = models.IntegerField(verbose_name='Nivel')
        dadosDeGolpe = models.IntegerField(verbose_name='Dados de golpe')
        puntosDeGolpe = models.IntegerField(verbose_name='Puntos de golpe')
        tamano = models.TextField(verbose_name='Tamaño')
        velocidad = models.TextField(verbose_name='Velocidad')
        ca = models.IntegerField(verbose_name='Clase de armadura')
        ataqueBase = models.IntegerField(verbose_name='Ataque base')
        ataque = models.TextField(verbose_name='Ataque')
        fuerza = models.IntegerField(verbose_name='Fuerza')
        destreza = models.IntegerField(verbose_name='Destreza')
        constitucion = models.IntegerField(verbose_name='Constitución')
        inteligencia = models.IntegerField(verbose_name='Inteligencia')
        sabiduria = models.IntegerField(verbose_name='Sabiduría')
        carisma = models.IntegerField(verbose_name='Carisma')
        fortaleza = models.IntegerField(verbose_name='Fortaleza')
        reflejos = models.IntegerField(verbose_name='Reflejos')
        voluntad = models.IntegerField(verbose_name='Voluntad')
        dotes = models.ManyToManyField('Dote')
        especial = models.ManyToManyField('Especial')
        trucos = models.ManyToManyField('Truco')
        puntuacionHabilidad = models.ManyToManyField('PuntuacionHabilidadCA')

        def __str__(self):
            return nombre

        class Meta:
            ordering = ('nombre', )

    class Truco(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        descripcion = models.TextField(verbose_name='Descripción')
        cd = models.IntegerField(verbose_name='CD')
        prerrequisitoTruco = models.ManyToManyField('self')

        def __str__(self):
            return nombre
        
        class Meta:
            ordering = ('nombre', )

    class PuntuacionHabilidadCA(models.Model):
        puntuacion = models.IntegerField(verbose_name='Puntuación')
        habilidad = models.ForeignKey('Habilidad', on_delete=models.CASCADE)

        def __str__(self):
            return self.habilidad.habilidad
        
        class Meta:
            ordering = ('pk', )

    class Inventario(models.Model):
        equipado = models.BooleanField(verbose_name='Está equipado')

    class Objeto(models.Model):
        clase = models.TextField(verbose_name='Clase', null=True)
        nombre = models.TextField(verbose_name='Nombre')
        precio = models.IntegerField(verbose_name='Precio')
        peso = models.IntegerField(verbose_name='Peso', null=True)
        propiedades = models.ManyToManyField('Propiedad')

        def __str__(self):
            return self.nombre
        
        class Meta:
            ordering = ('nombre', )
    
    class Arma(Objeto):
        danoP = models.TextField(verbose_name='Daño P')
        danoM = models.TextField(verbose_name='Daño M')
        critico = models.TextField(verbose_name='Crítico')
        alcance = models.TextField(verbose_name='Alcance', null=True)
        tipo = models.TextField(verbose_name='Tipo')
        especial = models.TextField(verbose_name='Especial')

        def __str__(self):
            return self.nombre

        class Meta:
            ordering = ('nombre', )

    class Armadura(Objeto):
        bonifArm = models.IntegerField(verbose_name='Bonificación armadura')
        bonifMaxDes = models.IntegerField(verbose_name='Bonificación máximo destreza')
        penalizArm = models.IntegerField(verbose_name='Penalizador armadura')
        falloConjArc = models.IntegerField(verbose_name='Fallo conjuro arcano')
        velocidad9m = models.IntegerField(verbose_name='Velocidad 9m')
        velocidad6m = models.IntegerField(verbose_name='Velocidad 6m')

        def __str__(self):
            return self.nombre

        class Meta:
            ordering = ('nombre', )

    class Propiedad(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        descripcion = models.TextField(verbose_name='Descripción')
        coste = models.IntegerField(verbose_name='Coste', null=True)
        costeDinero = models.IntegerField(verbose_name='Coste dinero', null=True)

        def __str__(self):
            return self.nombre

        class Meta:
            ordering = ('nombre', )