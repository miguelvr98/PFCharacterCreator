from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    nickname = models.TextField(verbose_name='Nickname')
    es_admin = models.BooleanField(verbose_name='Admin', default=False)

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
    puntos_de_golpe = models.IntegerField(verbose_name='Puntos de golpe',
    null=True)
    resistencia_dano = models.IntegerField(verbose_name='Resistencia al daño',
    null=True)
    resistencia_conjuros = models.IntegerField(verbose_name='Resistencia a Conjuros',
    null=True)
    clase_armadura = models.IntegerField(verbose_name='Clase de armadura',
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
    es_publico = models.BooleanField(verbose_name='Es público', default=False)
    idiomas = models.ManyToManyField('Idioma')
    inmune = models.ManyToManyField('Inmune')
    raza = models.ForeignKey('Raza', on_delete=models.CASCADE, null=True)
    clase = models.ManyToManyField('Clase')
    dotes = models.ManyToManyField('Dote')
    puntuaciones_habilidad = models.ManyToManyField('PuntuacionHabilidad')
    propiedades_objeto = models.ManyToManyField('PropiedadObjeto')
    companero_animal = models.ForeignKey('CompaneroAnimalPersonaje', on_delete=models.CASCADE, null=True)
    conjuros_conocidos = models.ManyToManyField('Conjuro')
    poderes_conocidos = models.ManyToManyField('Poder')

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
        fuerza = models.IntegerField(verbose_name='Fuerza', default=0)
        destreza = models.IntegerField(verbose_name='Destreza', default=0)
        constitucion = models.IntegerField(verbose_name='Constitución',default=0)
        inteligencia = models.IntegerField(verbose_name='Inteligencia', default=0)
        sabiduria = models.IntegerField(verbose_name='Sabiduría', default=0)
        carisma = models.IntegerField(verbose_name='Carisma', default=0)
        idiomas_conocidos = models.TextField(verbose_name='Idiomas conocidos', null=True)
        idiomas_eleccion = models.ManyToManyField('Idioma')
        bonificaciones_raza = models.ManyToManyField('BonificacionRaza')

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
        nivel = models.IntegerField(verbose_name='Nivel', default=1, null=True)
        dados_de_golpe = models.IntegerField(verbose_name='Dados de golpe',
        default=6, null=True)
        ataque_base = models.TextField(verbose_name='Ataque base',
         null=True)
        fortaleza = models.IntegerField(verbose_name='Fortaleza', 
        null=True)
        reflejos = models.IntegerField(verbose_name='Reflejos', null=True)
        voluntad = models.IntegerField(verbose_name='Fortaleza', null=True)
        competencia = models.TextField(verbose_name='Competente con', null=True)
        rafaga_de_golpes = models.TextField(verbose_name='Ráfaga de golpes', null=True)
        dano_desarmado = models.TextField(verbose_name='Daño desarmado', null = True)
        bonificacion_ac = models.IntegerField(verbose_name='Bonificación AC', null = True)
        movimiento_rapido = models.IntegerField(verbose_name='Movimiento rápido', null =True)
        puntos_de_habilidad_por_nivel = models.TextField(verbose_name='Puntos de habilidad por nivel', null=True)
        nivel_conjuro_diario = models.ManyToManyField('NivelConjuroDiario')
        cantidad_conjuros_conocidos = models.ManyToManyField('CantidadConjuroConocido')
        poderes = models.ManyToManyField('Poder')
        especiales = models.ManyToManyField('Especial')
        companero_animal = models.ManyToManyField('CompaneroAnimal')
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
        ataque_base = models.IntegerField(verbose_name='Ataque base', null=True)
        fuerza = models.IntegerField(verbose_name='Fuerza', null=True)
        destreza = models.IntegerField(verbose_name='Destreza', null=True)
        constitucion = models.IntegerField(verbose_name='Constitución', null=True)
        inteligencia = models.IntegerField(verbose_name='Inteligencia', null=True)
        sabiduria = models.IntegerField(verbose_name='Sabiduría', null=True)
        carisma = models.IntegerField(verbose_name='Carisma', null=True)
        creador = models.OneToOneField('Perfil', null=True, on_delete=models.SET_NULL)
        es_dote_companero_animal = models.BooleanField(verbose_name='Es dote de compañero animal', default=False)
        prerrequisito_dote = models.ManyToManyField('self')
    
        def __str__(self):
            return self.nombre
        
        class Meta: 
            ordering = ('nombre', )

    class Conjuro(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        nivel = models.IntegerField(verbose_name='Nivel')
        escuela = models.TextField(verbose_name='Escuela')
        tiempo_de_lanzamiento = models.TextField(verbose_name='Tiempo de lanzamiento')
        alcance = models.TextField(verbose_name='Alcance')
        efecto = models.TextField(verbose_name='Efecto', null=True)
        objetivo = models.TextField(verbose_name='Objetivo', null=True)
        duracion = models.TextField(verbose_name='Duración')
        tiro_de_salvacion = models.BooleanField(verbose_name='Tiro de salvación')
        resistencia_conjuros = models.BooleanField(verbose_name='Resistencia a conjuros')
        descripcion = models.TextField(verbose_name='Descripción')

        def __str__(self):
            return self.nombre

        class Meta:
            ordering = ('nivel', 'nombre', )

    class Poder(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        descripcion = models.TextField(verbose_name='Descripción')
        nivel = models.IntegerField(verbose_name='Nivel', null=True)
        ataque_base = models.IntegerField(verbose_name='Ataque base', null=True)
        fuerza = models.IntegerField(verbose_name='Fuerza', null=True)
        destreza = models.IntegerField(verbose_name='Destreza', null=True)
        constitucion = models.IntegerField(verbose_name='Constitución', null=True)
        inteligencia = models.IntegerField(verbose_name='Inteligencia', null=True)
        sabiduria = models.IntegerField(verbose_name='Sabiduría', null=True)
        carisma = models.IntegerField(verbose_name='Carisma', null=True)
        prerrequisito_poder = models.ManyToManyField('self')

        def __str__(self):
            return nombre
        
        class Meta:
            ordering = ('nivel', 'nombre', )

    class NivelConjuroDiario(models.Model):
        cantidad = models.IntegerField(verbose_name='Cantidad')
        nivel = models.IntegerField(verbose_name='Nivel', null=True)

        def __str__(self):
            return str(nivel)+": "+str(cantidad)
        
        class Meta:
            ordering = ('nivel', )

    class CantidadConjuroConocido(models.Model):
        cantidad = models.IntegerField(verbose_name='Cantidad')
        nivel = models.IntegerField(verbose_name='Nivel')

        def __str__(self):
            return str(nivel)+": "+str(cantidad)
        
        class Meta:
            ordering = ('nivel', )

    class Especial(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        descripcion = models.TextField(verbose_name='Descripción')
        es_especial_companero_animal = models.BooleanField(verbose_name='Es especial de compañero animal', default=False)
        clase_perteneciente = models.ForeignKey('Clase', on_delete=models.CASCADE, null=True)

        def __str__(self):
            return nombre
        
        class Meta:
            ordering = ('nombre', )

    class CompaneroAnimal(models.Model):
        tipo = models.TextField(verbose_name='Tipo', null=True)
        nivel = models.IntegerField(verbose_name='Nivel')
        dados_de_golpe = models.IntegerField(verbose_name='Dados de golpe')
        puntos_de_golpe = models.IntegerField(verbose_name='Puntos de golpe')
        tamano = models.TextField(verbose_name='Tamaño')
        velocidad = models.TextField(verbose_name='Velocidad')
        ca = models.IntegerField(verbose_name='Clase de armadura')
        ataque_base = models.IntegerField(verbose_name='Ataque base')
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
        especial = models.ManyToManyField('Especial')

        def __str__(self):
            return tipo

        class Meta:
            ordering = ('tipo', )

    class CompaneroAnimalPersonaje(CompaneroAnimal):
        nombre = models.TextField(verbose_name='Nombre')
        dotes = models.ManyToManyField('Dote')
        trucos = models.ManyToManyField('Truco')
        puntuacion_habilidad = models.ManyToManyField('PuntuacionHabilidadCA')

    class Truco(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        descripcion = models.TextField(verbose_name='Descripción')
        cd = models.TextField(verbose_name='CD')
        prerrequisito_truco = models.ManyToManyField('self')

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

    class PropiedadObjeto(models.Model):
        equipado = models.BooleanField(verbose_name='Está equipado', default=False)
        cantidad = models.IntegerField(verbose_name='Cantidad', default=1)
        propiedades = models.ManyToManyField('Propiedad')
        objeto = models.ForeignKey('Objeto', on_delete=models.CASCADE)

    class Propiedad(models.Model):
        nombre = models.TextField(verbose_name='Nombre')
        descripcion = models.TextField(verbose_name='Descripción')
        coste = models.IntegerField(verbose_name='Coste', null=True)
        coste_dinero = models.IntegerField(verbose_name='Coste dinero', null=True)

        def __str__(self):
            return self.nombre

        class Meta:
            ordering = ('nombre', )

    class Objeto(models.Model):
        clase = models.TextField(verbose_name='Clase', null=True)
        nombre = models.TextField(verbose_name='Nombre')
        precio = models.IntegerField(verbose_name='Precio')
        peso = models.IntegerField(verbose_name='Peso', null=True)

        def __str__(self):
            return self.nombre
        
        class Meta:
            ordering = ('nombre', )
    
    class Arma(Objeto):
        dano_p = models.TextField(verbose_name='Daño P')
        dano_m = models.TextField(verbose_name='Daño M')
        critico = models.TextField(verbose_name='Crítico')
        alcance = models.TextField(verbose_name='Alcance', null=True)
        tipo = models.TextField(verbose_name='Tipo')
        especial = models.TextField(verbose_name='Especial')

        def __str__(self):
            return self.nombre

        class Meta:
            ordering = ('nombre', )

    class Armadura(Objeto):
        bonif_arm = models.IntegerField(verbose_name='Bonificación armadura')
        bonif_max_des = models.IntegerField(verbose_name='Bonificación máximo destreza')
        penaliz_arm = models.IntegerField(verbose_name='Penalizador armadura')
        fallo_conj_arc = models.IntegerField(verbose_name='Fallo conjuro arcano')
        velocidad_9m = models.IntegerField(verbose_name='Velocidad 9m')
        velocidad_6m = models.IntegerField(verbose_name='Velocidad 6m')

        def __str__(self):
            return self.nombre

        class Meta:
            ordering = ('nombre', )