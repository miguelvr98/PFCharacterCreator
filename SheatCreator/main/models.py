from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Personaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
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
    
    class Genero(models.TextChoices):
        F = 'F', 'Femenino'
        M = 'M', 'Masculino'
    genero = models.CharField(max_length=2, choices=Genero.choices,
    null=True)
    altura = models.TextField(verbose_name='Altura', null=True)
    peso = models.TextField(verbose_name='Peso', null=True)
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
        bonificacionRaza = models.ForeignKey('BonificacionRaza',
         on_delete=models.SET_NULL, null=True)

        def __str__(self):
            return self.raza

        class Meta:
            ordering = ('pk', )

    class BonificacionRaza(models.Model):
        bonificacionRaza = models.TextField(verbose_name='Bonificación raza')

        def __str__(self):
            return self.bonificacionRaza

        class Meta:
            ordering = ('pk', )

    class Puntuacion(models.Model):
        puntuacion = models.IntegerField(verbose_name='Puntuación',
        null=True)
        personaje = models.ForeignKey('Personaje',
         on_delete=models.CASCADE)
        habilidad = models.ForeignKey('Habilidad',
         on_delete=models.CASCADE)

        def __str__(self):
            return self.habilidad.habilidad
        
        class Meta:
            ordering = ('pk', )

    class Habilidad(models.Model):
        habilidad = models.TextField(verbose_name='Habilidad')
        #Creo que falta hacer un boolean o un enumerado para ver si
        #la clase es competente

        def __str__(self):
            return self.habilidad

        class Meta:
            ordering = ('pk', )

    class Clase(models.Model):
        clase = models.TextField(verbose_name='Clase')
        nivel = models.IntegerField(verbose_name='Nivel', default=1)
        dadosDeGolpe = models.IntegerField(verbose_name='Dados de golpe',
        default=6)
        ataqueBase = models.TextField(verbose_name='Ataque base',
         null=True)
        fortaleza = models.IntegerField(verbose_name='Fortaleza', 
        null=True)
        reflejos = models.IntegerField(verbose_name='Reflejos', null=True)
        voluntad = models.IntegerField(verbose_name='Fortaleza', null=True)

        def __str__(self):
            return self.clase

        class Meta:
            ordering = ('pk', )
    
    class Dote(models.Model):
        nombre = models.TextField(verbose_name='Dote')
        descripcion = models.TextField(verbose_name='Descripcion')
    
        def __str__(self):
            return self.nombre
        
        class Meta: 
            ordering = ('pk', )

    class PrerrequisitoDote(models.Model):
        ataqueBase = models.IntegerField(verbose_name='Ataque base',
        null=True)
        clase = models.TextField(verbose_name='Clase', null=True)
        nivel = models.IntegerField(verbose_name='Nivel', null=True)
        fuerza = models.IntegerField(verbose_name='Fuerza', null=True)
        destreza = models.IntegerField(verbose_name='Destreza',
         null=True)
        constitucion = models.IntegerField(verbose_name='Constitucion',
        null=True)
        inteligencia = models.IntegerField(verbose_name='Inteligencia',
         null=True)
        sabiduria = models.IntegerField(verbose_name='Sabiduría',
         null=True)
        carisma = models.IntegerField(verbose_name='Carisma', null=True)
        puntuacion = models.ForeignKey('Habilidad', verbose_name='Puntuación de habilidad',
        null=True, on_delete=models.SET_NULL)
        dotes = models.ManyToManyField('Dote', verbose_name='Dotes')

        def __str__(self):
            return str(ataqueBase)+clase+str(nivel)+str(fuerza)+str(destreza)+str(constitucion)+str(inteligencia)+str(sabiduria)+str(carisma)+puntuacion+dotes

        class Meta:
            ordering = ('pk', )


