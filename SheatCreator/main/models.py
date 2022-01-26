from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    nickname = models.TextField(verbose_name='Nickname')
    es_admin = models.BooleanField(verbose_name='Admin', default=False)

    def __str__(self):
        return self.usuario.username

    class Meta:
        ordering = ('pk', )

# Falta por pensar como hacer los dados de golpe
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
    puntos_de_golpe = models.IntegerField(verbose_name='Puntos de golpe',
    null=True)
    resistencia_dano = models.IntegerField(verbose_name='Resistencia al daño',
    null=True)
    resistencia_conjuros = models.IntegerField(verbose_name='Resistencia a Conjuros',
    null=True)
    fuerza = models.IntegerField(verbose_name='Fuerza', default=10)
    destreza = models.IntegerField(verbose_name='Destreza', default=10)
    constitucion = models.IntegerField(verbose_name='Constitución',
     default=10)
    inteligencia = models.IntegerField(verbose_name='Inteligencia',
     default=10)
    sabiduria = models.IntegerField(verbose_name='Sabiduría',
     default=10)
    carisma = models.IntegerField(verbose_name='Carisma', default=10)
    dinero = models.FloatField(verbose_name='Dinero', default=0.0)
    es_publico = models.BooleanField(verbose_name='Es público', default=False)
    idiomas = models.ManyToManyField('Idioma')
    raza = models.ForeignKey('Raza', on_delete=models.CASCADE, null=True)
    clases = models.ManyToManyField('Clase')
    dotes = models.ManyToManyField('Dote')
    puntuaciones_habilidad = models.ManyToManyField('PuntuacionHabilidad')
    propiedades_objeto = models.ManyToManyField('PropiedadObjeto')
    companero_animal = models.ForeignKey('CompaneroAnimalPersonaje', on_delete=models.CASCADE, null=True)
    conjuros_conocidos = models.ManyToManyField('Conjuro')
    poderes_conocidos = models.ManyToManyField('Poder')
    linaje = models.ForeignKey('Linaje', null=True, on_delete=models.SET_NULL)

    @property
    def bonificadorFuerza(self):
        return int((fuerza-10)/2)
    
    @property
    def bonificadorDestreza(self):
        return int((destreza-10)/2)

    @property
    def bonificadorConstitucion(self):
        return int((constitucion-10)/2)

    @property
    def bonificadorInteligencia(self):
        return int((inteligencia-10)/2)

    @property
    def bonificadorSabiduria(self):
        return int((sabiduria-10)/2)

    @property
    def bonificadorCarisma(self):
        return int((carisma-10)/2)
    
    @property
    def iniciativa(self):
        return bonificadorDestreza

    @property
    def carga(self):
        carga = 0.0
        for propiedad_objeto in self.propiedades_objeto:
            carga_objeto = propiedad_objeto.objeto.peso * propiedad_objeto.objeto.cantidad
            carga = carga + carga_objeto
        return carga

    @property
    def carga_ligera(self):
        carga_ligera = 0.0
        libra = 0.45
        diccionario = {10:33, 11:38, 12:43, 13:50, 14:58, 15:66, 16:76, 17:86, 18:100, 19:116}
        if self.fuerza < 10:
            carga_ligera = self.fuerza * 3.33
        elif self.fuerza >= 10 and self.fuerza <= 19:
            carga_ligera = diccionario.get(self.fuerza) * libra
        elif self.fuerza > 19:
            carga_ligera = diccionario.get(self.fuerza%10) * libra
        if self.raza.tamano == 'Pequeño':
            carga_ligera = carga_ligera/2
        return carga_ligera
    
    @property
    def carga_media(self):
        return carga_ligera(self) * 2
    
    @property
    def carga_maxima(self):
        return carga_media(self) * 2

    @property
    def clase_armadura(self):
        clase_armadura = 10
        for propiedad_objeto in self.propiedades_objeto:
            for propiedad in propiedad_objeto.propiedades:
                if propiedad.equipado == True and ('Armadura' in propiedad_objeto.objeto.clase or 'Escudo' in propiedad_objeto.objeto.clase):
                    bonif_arm = propiedad_objeto.objeto.bonif_arm
                    bonif_max_des = []
                    bonif_max_des.append(propiedad_objeto.objeto.bonif_max_des)
                    max = max(bonif_max_des)
                    clase_armadura = clase_armadura + bonif_arm
                if max >= bonificadorDestreza(self):
                    clase_armadura = clase_armadura + bonificadorDestreza(self)
                else:
                    clase_armadura = clase_armadura + max
        for clase in self.clases:
            clase_armadura = clase_armadura + clase.bonificacion_ac
        return clase_armadura
    
    @property
    def desprevenido(self):
        desprevenido = 10
        for propiedad_objeto in self.propiedades_objeto:
            for propiedad in propiedad_objeto.propiedades:
                if propiedad.equipado == True and ('Armadura' in propiedad_objeto.objeto.clase or 'Escudo' in propiedad_objeto.objeto.clase):
                    bonif_arm = propiedad_objeto.objeto.bonif_arm
                    desprevenido = desprevenido + bonif_arm
        return desprevenido

    @property
    def toque(self):
        toque = 10
        for propiedad_objeto in self.propiedades_objeto:
            for propiedad in propiedad_objeto.propiedades:
                if propiedad.equipado == True and ('Armadura' in propiedad_objeto.objeto.clase or 'Escudo' in propiedad_objeto.objeto.clase):
                    bonif_max_des = []
                    bonif_max_des.append(propiedad_objeto.objeto.bonif_max_des)
                    max = max(bonif_max_des)
                    if max >= bonificadorDestreza(self):
                        toque = toque + bonificadorDestreza(self)
                    else:
                        toque = toque + max 
        return toque

    @property
    def bmc(self):
        ataque_base_sum = 0
        for clase in self.clases:
            ataque_base_sum = ataque_base_sum + clase.ataque_base_int
        bmc = '+' + str(bmc + ataque_base_sum + bonificadorFuerza(self))
        return bmc

    @property
    def dmc(self):
        ataque_base_sum = 0
        for clase in self.clases:
            ataque_base_sum = ataque_base_sum + clase.ataque_base_int
        dmc = 10 + ataque_base_sum + bonificadorFuerza(self) + bonificadorDestreza(self)
        return dmc
    
    @property
    def fortaleza(self):
        fortaleza = 0
        for clase in self.clases:
            fortaleza = fortaleza + clase.fortaleza
        fortaleza = fortaleza + bonificadorConstitucion(self)
        return fortaleza
    
    @property
    def reflejos(self):
        reflejos = 0
        for clase in self.clases:
            reflejos = reflejos + clase.reflejos
        reflejos = reflejos + bonificadorDestreza(self)
        return reflejos

    @property
    def voluntad(self):
        voluntad = 0
        for clase in self.clases:
            voluntad = voluntad + clase.voluntad
        voluntad = voluntad + bonificadorSabiduria(self)
        return voluntad

    @property
    def ataque_base(self):
        ataque_base_sum = 0
        ataque_base = '+'
        for clase in self.clases:
            ataque_base_sum = ataque_base_sum + clase.ataque_base_int
        if ataque_base_sum >= 6:
            while ataque_base_sum >= 6:
                ataque_base = ataque_base + str(ataque_base_sum) + '/'
                ataque_base_sum = ataque_base_sum - 5
            ataque_base = ataque_base + str(ataque_base_sum)
        else:
            ataque_base = ataque_base + str(ataque_base_sum)
        return ataque_base

    @property
    def nivel(self):
        nivel = 0
        for clase in self.clases:
            nivel = nivel + clase.nivel
        return nivel
    
    @property
    def habilidades(self):
        for ph in self.puntuaciones_habilidad:
           habilidades[ph.habilidad.habilidad] = ph.puntuacion
        return habilidades

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
    nivel = models.IntegerField(verbose_name='Nivel', default=0)
    dados_de_golpe = models.IntegerField(verbose_name='Dados de golpe', 
    default=6, null=True)
    ataque_base = models.TextField(verbose_name='Ataque base', 
    null=True)
    ataque_base_int = models.IntegerField(verbose_name='Ataque base', null=False, default=0)
    fortaleza = models.IntegerField(verbose_name='Fortaleza', 
    null=True)
    reflejos = models.IntegerField(verbose_name='Reflejos', null=True)
    voluntad = models.IntegerField(verbose_name='Fortaleza', null=True)
    competencia = models.TextField(verbose_name='Competente con', null=True)
    rafaga_de_golpes = models.TextField(verbose_name='Ráfaga de golpes', null=True)
    dano_desarmado = models.TextField(verbose_name='Daño desarmado', null = True)
    bonificacion_ac = models.IntegerField(verbose_name='Bonificación AC', null = True, default=0)
    movimiento_rapido = models.IntegerField(verbose_name='Movimiento rápido', null =True)
    puntos_de_habilidad_por_nivel = models.IntegerField(verbose_name='Puntos de habilidad', null=True)
    descripcion_dados_de_golpe = models.TextField(verbose_name='Dado de golpe', null=True)
    descripcion_puntos_de_habilidad = models.TextField(verbose_name='Puntos de habilidad por nivel', null=True)
    descripcion_habilidades = models.TextField(verbose_name='Competente con las habilidades', null=True)
    nivel_conjuro_diario = models.ManyToManyField('NivelConjuroDiario')
    cantidad_conjuros_conocidos = models.ManyToManyField('CantidadConjuroConocido')
    poderes = models.ManyToManyField('Poder')
    especiales = models.ManyToManyField('Especial')
    companero_animal = models.ManyToManyField('CompaneroAnimal')
    habilidades = models.ManyToManyField('Habilidad')
    linajes = models.ManyToManyField('Linaje')
    conjuros = models.ManyToManyField('Conjuro')

    def __str__(self):
        return self.clase

    class Meta:
        ordering = ('clase', )
    
class Dote(models.Model):
    nombre = models.TextField(verbose_name='Dote')
    descripcion = models.TextField(verbose_name='Descripcion')
    class Tipo(models.TextChoices):
        GENERAL = 'General'
        COMBATE = 'Combate'
        METAMAGICA = 'Metamágica'
    tipo = models.CharField(max_length=10, choices=Tipo.choices, verbose_name='Tipo', null=True)
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
    #pr_dote son las dotes que la tienen como prerrequisito de dote
    prerrequisito_dote = models.ManyToManyField('self', symmetrical=False, related_name='pr_dote')
    prerrequisito_raza = models.ForeignKey('Raza', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nombre
        
    class Meta: 
        ordering = ('tipo', 'nombre' )

class Conjuro(models.Model):
    nombre = models.TextField(verbose_name='Nombre')
    nivel = models.IntegerField(verbose_name='Nivel')
    escuela = models.TextField(verbose_name='Escuela')
    tiempo_de_lanzamiento = models.TextField(verbose_name='Tiempo de lanzamiento')
    componentes = models.TextField(verbose_name='Componentes', null=True)
    alcance = models.TextField(verbose_name='Alcance')
    efecto = models.TextField(verbose_name='Efecto', null=True)
    area = models.TextField(verbose_name='Área', null=True)
    objetivo = models.TextField(verbose_name='Objetivo', null=True)
    duracion = models.TextField(verbose_name='Duración')
    tiro_de_salvacion = models.TextField(verbose_name='Tiro de salvación')
    resistencia_conjuros = models.TextField(verbose_name='Resistencia a conjuros')
    descripcion = models.TextField(verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nivel', 'nombre', )

class Poder(models.Model):
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    nivel = models.IntegerField(verbose_name='Nivel', default=1)
    prerrequisito_poder = models.ManyToManyField('self', symmetrical=False, related_name='pr_poder')

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

    def __str__(self):
        return self.nombre
        
    class Meta:
        ordering = ('nombre', )

class CompaneroAnimal(models.Model):
    tipo = models.TextField(verbose_name='Tipo', null=True)
    nivel = models.IntegerField(verbose_name='Nivel', null=True)
    dados_de_golpe = models.IntegerField(verbose_name='Dados de golpe', null=True)
    puntos_de_golpe = models.IntegerField(verbose_name='Puntos de golpe', null=True)
    tamano = models.TextField(verbose_name='Tamaño')
    velocidad = models.TextField(verbose_name='Velocidad')
    ca = models.IntegerField(verbose_name='Clase de armadura', default=0)
    ataque_base = models.IntegerField(verbose_name='Ataque base', null=True)
    ataque = models.TextField(verbose_name='Ataque')
    fuerza = models.IntegerField(verbose_name='Fuerza', default=0)
    destreza = models.IntegerField(verbose_name='Destreza', default=0)
    constitucion = models.IntegerField(verbose_name='Constitución', default=0)
    inteligencia = models.IntegerField(verbose_name='Inteligencia', default=0)
    sabiduria = models.IntegerField(verbose_name='Sabiduría', default=0)
    carisma = models.IntegerField(verbose_name='Carisma', default=0)
    fortaleza = models.IntegerField(verbose_name='Fortaleza', null=True)
    reflejos = models.IntegerField(verbose_name='Reflejos', null=True)
    voluntad = models.IntegerField(verbose_name='Voluntad', null=True)
    numero_dotes = models.IntegerField(verbose_name='Número de dotes', null=True)
    puntos_habilidad = models.IntegerField(verbose_name='Puntos de habilidad', null=True)
    numero_trucos = models.IntegerField(verbose_name='Número de trucos', null=True)
    nivel_cambio = models.IntegerField(verbose_name='Nivel de cambio', null=True)
    es_familiar = models.BooleanField(verbose_name='Es familiar', default=False)
    companero_animal_cambio = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    especiales = models.ManyToManyField('Especial')

    def __str__(self):
        return self.tipo

    class Meta:
        ordering = ('tipo', )

class CompaneroAnimalPersonaje(CompaneroAnimal):
    nombre = models.TextField(verbose_name='Nombre')
    dotes = models.ManyToManyField('Dote')
    trucos = models.ManyToManyField('Truco')
    puntuacion_habilidad = models.ManyToManyField('PuntuacionHabilidad')

    @property
    def habilidades(self):
        for ph in self.puntuaciones_habilidad:
           habilidades[ph.habilidad.habilidad] = ph.puntuacion
        return habilidades

class Truco(models.Model):
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    cd = models.TextField(verbose_name='CD')
    prerrequisito_truco = models.ManyToManyField('self', symmetrical=False, related_name='pr_truco')

    def __str__(self):
        return self.nombre
        
    class Meta:
        ordering = ('nombre', )

class PropiedadObjeto(models.Model):
    cantidad = models.IntegerField(verbose_name='Cantidad', default=1)
    propiedades = models.ManyToManyField('Propiedad')
    objeto = models.ForeignKey('Objeto', on_delete=models.CASCADE)

class Propiedad(models.Model):
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    coste = models.IntegerField(verbose_name='Coste', null=True)
    coste_dinero = models.IntegerField(verbose_name='Coste dinero', null=True)
    equipado = models.BooleanField(verbose_name='Está equipado', default=False)
    es_propiedad_arma = models.BooleanField(verbose_name='Es propiedad de arma', default=False)
    es_propiedad_armadura = models.BooleanField(verbose_name='Es propiedad de armadura', default=False)
    prerrequisito_propiedad = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='pr_propiedad')

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre', )

class Objeto(models.Model):
    clase = models.TextField(verbose_name='Clase', null=True)
    nombre = models.TextField(verbose_name='Nombre')
    precio = models.FloatField(verbose_name='Precio', default=0.0)
    peso = models.FloatField(verbose_name='Peso', default=0.0)

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
    bonif_max_des = models.IntegerField(verbose_name='Bonificación máximo destreza', null=True)
    penaliz_arm = models.TextField(verbose_name='Penalizador armadura')
    fallo_conj_arc = models.TextField(verbose_name='Fallo conjuro arcano')
    velocidad_9m = models.TextField(verbose_name='Velocidad 9m')
    velocidad_6m = models.TextField(verbose_name='Velocidad 6m')

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre', )

class Linaje(models.Model):
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    linaje_arcano = models.TextField(verbose_name='Linaje arcano')
    habilidad = models.ForeignKey('Habilidad', null=False, on_delete=models.CASCADE)
    conjuros = models.ManyToManyField('Conjuro')
    dotes = models.ManyToManyField('Dote')
    poderes = models.ManyToManyField('Poder')

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre', )