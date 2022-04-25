from django import forms
from main.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import *
import re
import math

class EditarUsernameForm(forms.ModelForm):

    error_messages = {
        'username_short': ("El nombre de usuario debe tener al menos 6 caracteres"),
        'username_exists': ("Ya existe ese nombre de usuario"),
        'username_letters': ("El nombre de usuario solo puede contener letras y numeros"),
    }

    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ('username', )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 6:
            raise forms.ValidationError(self.error_messages['username_short'], code='username_short', )

        """if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", username):
                raise forms.ValidationError(self.error_messages['username_letters'], code='username_letters', )"""

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['username_exists'], code='username_exists', )
        return username
    
class EditarContrasenaForm(forms.Form):

    error_messages = {
        'password_mismatch': ("Las contraseñas no coinciden"),
        'password_short': ("La contraseña debe tener al menos 8 caracteres"),
        'password_letters': ("La contraseña solo puede contener letras y números"),
        'password_capital': ("La contraseña debe tener al menos una mayúscula"),
    }

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch', )

        """if len(password1) < 8:
            raise forms.ValidationError(self.error_messages['password_short'], code='password_short', )

        if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", password1):
            raise forms.ValidationError(self.error_messages['password_letters'], code='password_letters', )

        if not any(x.isupper() for x in password1):
            raise forms.ValidationError(self.error_messages['password_capital'], code='password_capital', )"""
        return password2
    
class UserForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': ("Las contraseñas no coinciden"),
        'username_exists': ("Ya existe ese nombre de usuario"),
        'password_short': ("La contraseña debe tener al menos 8 caracteres"),
        'password_letters': ("La contraseña solo puede contener letras y números"),
        'password_capital': ("La contraseña debe tener al menos una mayúscula"),
        'username_short': ("El nombre de usuario debe tener al menos 6 caracteres"),
        'username_letters': ("El nombre de usuario solo puede contener letras y numeros"),
    }

    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label=("Password confirmation"), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}), help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'})
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch', )

        """if len(password1) < 8:
            raise forms.ValidationError(self.error_messages['password_short'], code='password_short', )

        if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", password1):
            raise forms.ValidationError(self.error_messages['password_letters'], code='password_letters', )

        if not any(x.isupper() for x in password1):
            raise forms.ValidationError(self.error_messages['password_capital'], code='password_capital', )"""
        return password2

        def clean_username(self):
            username = self.cleaned_data.get("username")
            if len(username) < 6:
                raise forms.ValidationError(self.error_messages['username_short'], code='username_short', )

            """if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", username):
                raise forms.ValidationError(self.error_messages['username_letters'], code='username_letters', )"""

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['username_exists'], code='username_exists', )
        return username
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class PerfilForm(forms.ModelForm):

    error_messages = {
        'nickname_letters': ("El nickname solo puede contener letras y símbolos"),
        'nickname_exists': ("El nickname ya existe"),
    }

    nickname = forms.CharField(label="Nickname", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}))
    
    class Meta:
        model = Perfil
        fields = ('nickname', )

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')

        """if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", nickname):
            raise forms.ValidationError(self.error_messages['nickname_letters'], code='nickname_letters')"""
        
        if Perfil.objects.exclude(pk=self.instance.pk).filter(nickname=nickname).exists():
            raise forms.ValidationError(self.error_messages['nickname_exists'],code='nickname_exists',)
        return nickname

class GDPRForm(forms.Form):
    checkbox = forms.BooleanField(label="", required=True, widget=forms.CheckboxInput())

class DoteForm(forms.ModelForm):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
        'nombre_exists': ("Ese nombre ya existe"),
        'nivel_range': ("El nivel tiene que estar entre 1 y 20"),
        'ataque_base_range': ("El ataque base tiene que estar entre 1 y 20"),
        'fuerza_range': ("La fuerza tiene que ser mayor que 0"),
        'destreza_range': ("La destreza tiene que ser mayor que 0"),
        'constitucion_range': ("La constitución tiene que ser mayor  que 0"),
        'inteligencia_range': ("La inteligencia tiene que ser mayor que 0"),
        'sabiduria_range': ("La sabiduria tiene que ser mayor que 0"),
        'carisma_range': ("La carisma tiene que ser mayor que 0"),
    }

    #Este esta hecho por si no funciona el de models.
    TIPO_CHOICES = (('General', 'General'), ('Combate', 'Combate'), ('Metamágica', 'Metamágica'), )

    nombre = forms.CharField(label='Nombre', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    descripcion = forms.CharField(label='Descripcon', required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}))
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo'}))
    nivel = forms.IntegerField(label='Nivel', initial=1, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nivel', 'min':1, 'max':20}))
    ataque_base = forms.IntegerField(label='Ataque base', initial=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ataque base', 'min':0, 'max':20}))
    fuerza = forms.IntegerField(label='Fuerza', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fuerza', 'min':1}))
    destreza = forms.IntegerField(label='Destreza', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Destreza', 'min':1}))
    constitucion = forms.IntegerField(label='Constitucion', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Constitución', 'min':1}))
    inteligencia = forms.IntegerField(label='Inteligencia', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Inteligencia', 'min':1}))
    sabiduria = forms.IntegerField(label='Sabiduria', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sabiduría', 'min':1}))
    carisma = forms.IntegerField(label='Carisma', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Carisma', 'min':1}))
    es_dote_companero_animal = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    prerrequisito_raza = forms.ModelChoiceField(queryset=Raza.objects, widget=forms.Select(), required=False)
    prerrequisito_dote = forms.ModelMultipleChoiceField(queryset=Dote.objects, widget=forms.SelectMultiple(), required=False)

    class Meta:
        model = Dote
        fields = ('nombre', 'tipo', 'nivel', 'ataque_base', 'fuerza', 'destreza', 'constitucion', 'inteligencia', 'sabiduria', 'carisma', 'es_dote_companero_animal', 'prerrequisito_raza', 'prerrequisito_dote')

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match("^[A-Za-zÀ-ÿ ]*$", nombre):
            raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        
        if Dote.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError(self.error_messages['nombre_exists'],code='nombre_exists')
        return nombre

class BuscarDoteForm(forms.Form):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
    }
    TIPO_CHOICES = (('General', 'General'), ('Combate', 'Combate'), ('Metamágica', 'Metamágica'), (None, '---------'), )

    nombre = forms.CharField(label='Nombre', required=False, widget=forms.TextInput(attrs={'class': 'form-control w-25 p-3 mx-auto', 'placeholder': 'Nombre'}))
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control w-25 mx-auto', 'placeholder': 'Tipo'}))
    es_dote_companero_animal = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'd-flex justify-content-center mx-auto mb-1'}), required=False)

    def __init__(self, *args, **kwargs):
        var = kwargs.pop('var')
        super(BuscarDoteForm, self).__init__(*args, **kwargs)
        self.var = var

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None:
            if not re.match("^[A-Za-zÀ-ÿ ]*$", nombre):
                raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre

class BuscarPoderForm(forms.Form):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
    }

    nombre = forms.CharField(label='Nombre', required=False, widget=forms.TextInput(attrs={'class': 'form-control w-25 p-3 mx-auto', 'placeholder': 'Nombre'}))

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None:
            if not re.match("^[A-Za-zÀ-ÿ ]*$", nombre):
                raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre

class BuscarConjuroForm(forms.Form):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
    }

    nombre = forms.CharField(label='Nombre', required=False, widget=forms.TextInput(attrs={'class': 'form-control w-25 p-3 mx-auto', 'placeholder': 'Nombre'}))
    nivel = forms.IntegerField(label='Nivel', required=False, widget=forms.NumberInput(attrs={'class': 'form-control w-25 mx-auto', 'placeholder': 'Nivel', 'min':0, 'max':9}))

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None:
            if not re.match("^[A-Za-zÀ-ÿ ]*$", nombre):
                raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre

class BuscarPersonajeForm(forms.Form):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
    }

    clase = forms.ModelChoiceField(queryset=Clase.objects.all().filter(nivel=0), widget=forms.Select(attrs={'class': 'd-flex justify-content-center mx-auto mb-1', 'placeholder': 'Clase'}), required=False)
    nombre = forms.CharField(label='Nombre', required=False, widget=forms.TextInput(attrs={'class': 'form-control w-25 p-3 mx-auto', 'placeholder': 'Nombre'}))

    def __init__(self, *args, **kwargs):
        var = kwargs.pop('var')
        super(BuscarPersonajeForm, self).__init__(*args, **kwargs)
        self.var = var

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match("^[A-Za-zÀ-ÿ ]*$", nombre):
            raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre

class PersonajeForm(forms.ModelForm):

    error_messages = {
        'caracteristica_choice_error': ('Debes elegir una característica por escoger humano como raza'),
    }

    #Este esta hecho por si no funciona el de models.
    TIPO_CHOICES = (('Estándar', 'Estándar (15 puntos a repartir)'), ('Alta fantasía', 'Alta fantasía (20 puntos a repartir)'), ('Épica', 'Épica (25 puntos a repartir)'), )
    ALINEAMIENTO_CHOICES = (('LB', 'Legal bueno'), ('LN', 'Legal neutro'), ('LM', 'Legal maligno'), ('NB', 'Neutral bueno'), ('N', 'Neutral'), ('NM', 'Neutral maligno'), ('CB', 'Caótico bueno'), ('CN', 'Caótico neutral'), ('CM', 'Caótico maligno'), )

    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo'}))
    raza = forms.ModelChoiceField(queryset=Raza.objects, widget=forms.Select(attrs={'class': ''}), required=True)
    clase = forms.ModelChoiceField(queryset=Clase.objects.all().filter(nivel=1), widget=forms.Select(attrs={'class': ''}), required=True)
    alineamiento = forms.ChoiceField(choices=ALINEAMIENTO_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Alineamiento'}))

    class Meta:
        model = Personaje
        fields = ('raza', )

class PersonajeForm2(forms.ModelForm):

    error_messages = {
        'caracteristica_choice_error': ('Debes elegir una característica por escoger humano como raza'),
        'puntos_a_elegir_menor_error': ('Sobran puntos de característica'),
        'puntos_a_elegir_mayor_error': ('Faltan puntos de característica'),
    }

    CARACTERISTICA_CHOICES = (('Fuerza', 'Fuerza'), ('Destreza', 'Destreza'), ('Constitucion', 'Constitución'), ('Inteligencia', 'Inteligencia'), ('Sabiduria', 'Sabiduría'), ('Carisma', 'Carisma'), )

    fuerza = forms.IntegerField(label='Fuerza', initial=10, required=True, widget=forms.NumberInput(attrs={'class': 'form-control w-auto d-inline', 'placeholder': 'Fuerza', 'min':7, 'max':18, 'onchange':'calcularPuntosRestantes();'}))
    destreza = forms.IntegerField(label='Destreza', initial=10, required=True, widget=forms.NumberInput(attrs={'class': 'form-control w-auto d-inline', 'placeholder': 'Destreza', 'min':7, 'max':18, 'onchange':'calcularPuntosRestantes();'}))
    constitucion = forms.IntegerField(label='Constitucion', initial=10, required=True, widget=forms.NumberInput(attrs={'class': 'form-control w-auto d-inline', 'placeholder': 'Constitución', 'min':7, 'max':18, 'onchange':'calcularPuntosRestantes();'}))
    inteligencia = forms.IntegerField(label='Inteligencia', initial=10, required=True, widget=forms.NumberInput(attrs={'class': 'form-control w-auto d-inline', 'placeholder': 'Inteligencia', 'min':7, 'max':18, 'onchange':'calcularPuntosRestantes();'}))
    sabiduria = forms.IntegerField(label='Sabiduria', initial=10, required=True, widget=forms.NumberInput(attrs={'class': 'form-control w-auto d-inline', 'placeholder': 'Sabiduría', 'min':7, 'max':18, 'onchange':'calcularPuntosRestantes();'}))
    carisma = forms.IntegerField(label='Carisma', initial=10, required=True, widget=forms.NumberInput(attrs={'class': 'form-control w-auto d-inline', 'placeholder': 'Carisma', 'min':7, 'max':18, 'onchange':'calcularPuntosRestantes();'}))
    caracteristica_choice = forms.ChoiceField(choices=CARACTERISTICA_CHOICES, widget=forms.Select(attrs={'class': 'w-auto'}), required=False)

    class Meta:
        model = Personaje
        fields = ('fuerza', 'destreza', 'constitucion', 'inteligencia', 'sabiduria', 'carisma', )
    
    def clean_caracteristica_choice(self):
        raza = self.raza
        humano = Raza.objects.get(raza='Humano')
        caracteristica_choice = self.cleaned_data.get('caracteristica_choice')
        if raza == humano and not caracteristica_choice:
            raise forms.ValidationError(self.error_messages['caracteristica_choice_error'], code='caracteristica_choice_error')
        return caracteristica_choice

    def clean(self):
        puntos_a_elegir = int(self.puntos_a_elegir)
        diccionario = {7:-4, 8:-2, 9:-1, 10:0, 11:1, 12:2, 13:3, 14:5, 15:7, 16:10, 17:13, 18:17}
        fuerza = self.cleaned_data.get('fuerza')
        destreza = self.cleaned_data.get('destreza')
        constitucion = self.cleaned_data.get('constitucion')
        inteligencia = self.cleaned_data.get('inteligencia')
        sabiduria = self.cleaned_data.get('sabiduria')
        carisma = self.cleaned_data.get('carisma')
        puntos_fuerza = diccionario[fuerza]
        puntos_destreza = diccionario[destreza]
        puntos_constitucion = diccionario[constitucion]
        puntos_inteligencia = diccionario[inteligencia]
        puntos_sabiduria = diccionario[sabiduria]
        puntos_carisma = diccionario[carisma]
        sumatorio = puntos_fuerza + puntos_destreza + puntos_constitucion + puntos_inteligencia + puntos_sabiduria + puntos_carisma
        if sumatorio > puntos_a_elegir:
            raise forms.ValidationError(self.error_messages['puntos_a_elegir_menor_error'], code='puntos_a_elegir_menor_error')
        elif sumatorio < puntos_a_elegir:
            raise forms.ValidationError(self.error_messages['puntos_a_elegir_mayor_error'], code='puntos_a_elegir_mayor_error')

    def __init__(self, *args, **kwargs):
        raza = kwargs.pop('raza')
        puntos_a_elegir = kwargs.pop('puntos_a_elegir')
        super(PersonajeForm2, self).__init__(*args, **kwargs)
        self.raza = Raza.objects.get(raza=raza)
        self.puntos_a_elegir = puntos_a_elegir

class PersonajeForm3(forms.Form):

    error_messages = {
        'dote_max_value': ("Solo puedes elegir una dote, 1 dote extra por ser humano, semielfo o semiorco y 1 dote extra al escoger el guerrero o monje"),
        'dote_prerrequisito_raza': ('El personaje no es de la raza que puede aprender esta dote'),
        'linaje_choice': ('Debes elegir un linaje por escoger el hechicero como clase'),
        'habilidades_number': ('No ha elegido el número de habilidades correcto'),
        'idiomas_number': ('No ha elegido el número de idiomas correcto'),
        'conjuros_conocidos_0_number': ('No ha elegido el número de conjuros de nivel 0 correcto'),
        'conjuros_conocidos_1_number': ('No ha elegido el número de conjuros de nivel 1 correcto'),
        'nombre_letters': ("El nombre solo puede contener letras"),
    }

    linaje = forms.ModelChoiceField(queryset=Linaje.objects, widget=forms.Select(), required=False)
    habilidades = forms.ModelMultipleChoiceField(queryset=Habilidad.objects, widget=forms.CheckboxSelectMultiple(), required=True)
    nombre = forms.CharField(label='Nombre', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))

    def __init__(self, *args, **kwargs):
        raza = kwargs.pop('raza')
        clase = kwargs.pop('clase')
        inteligencia = kwargs.pop('inteligencia')
        super(PersonajeForm3, self).__init__(*args, **kwargs)
        self.raza = Raza.objects.get(raza=raza)
        self.clase = Clase.objects.get(clase=clase, nivel=1)
        self.inteligencia = inteligencia
        queryset1 = Dote.objects.all().filter(prerrequisito_raza=raza)
        queryset2 = Dote.objects.all().filter(prerrequisito_raza=None).filter(nivel=0).filter(ataque_base__lte=self.clase.ataque_base_int).filter(prerrequisito_dote=None)
        queryset3 = Dote.objects.all().filter(prerrequisito_raza=None).filter(nivel=1).filter(ataque_base__lte=self.clase.ataque_base_int).filter(prerrequisito_dote=None).exclude(creador=None)
        self.fields['dotes'] = forms.ModelMultipleChoiceField(queryset=(queryset1 | queryset2 | queryset3).distinct(), widget=forms.CheckboxSelectMultiple(attrs={'class': ''}), required=True)
        self.fields['idiomas'] = forms.ModelMultipleChoiceField(queryset=raza.idiomas_eleccion, widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_0'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=0), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_1'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=1), widget=forms.CheckboxSelectMultiple(), required=False)
    
    def clean_dotes(self):
        dotes = self.cleaned_data.get('dotes')
        numero_dotes = 1
        humano = Raza.objects.get(raza='Humano')
        semielfo = Raza.objects.get(raza='Semielfo')
        semiorco = Raza.objects.get(raza='Semiorco')
        clase = self.clase
        especiales_clase = Especial.objects.all().filter(clase=clase).filter(nombre__icontains='Dotes adicionales')
        if self.raza == humano or self.raza == semielfo or self.raza == semiorco:
            numero_dotes = numero_dotes + 1
        if especiales_clase:
            numero_dotes = numero_dotes + 1
        if len(dotes) != numero_dotes:
            raise forms.ValidationError(self.error_messages['dote_max_value'], code='dote_max_value')
        for dote in dotes:
            if dote.prerrequisito_raza and dote.prerrequisito_raza != self.raza:
                raise forms.ValidationError(self.error_messages['dote_prerrequisito_raza'], code='dote_prerrequisito_raza')
        return dotes
    
    def clean_habilidades(self):
        habilidades = self.cleaned_data.get('habilidades')
        clase = Clase.objects.get(clase=self.clase.clase, nivel=0)
        numero_habilidades_eleccion = clase.puntos_de_habilidad_por_nivel
        inteligencia = math.floor(int(self.inteligencia))
        bonificador_inteligencia = math.floor((inteligencia-10)/2)
        numero_habilidades_eleccion = numero_habilidades_eleccion + bonificador_inteligencia
        if numero_habilidades_eleccion <= 0:
            numero_habilidades_eleccion = 1
        if numero_habilidades_eleccion != len(habilidades):
            raise forms.ValidationError(self.error_messages['habilidades_number'], code='habilidades_number')
        return habilidades
    
    def clean_linaje(self):
        linaje = self.cleaned_data.get('linaje')
        clase = self.clase
        hechicero = Clase.objects.get(nivel=1, clase='Hechicero')
        if hechicero == clase and not linaje:
            raise forms.ValidationError(self.error_messages['linaje_choice'], code='linaje_choice')
        return linaje
    
    def clean_idiomas(self):
        idiomas = self.cleaned_data.get('idiomas')
        inteligencia = math.floor(int(self.inteligencia))
        numero_idiomas_eleccion = math.floor((inteligencia-10)/2)
        if numero_idiomas_eleccion < 0:
            numero_idiomas_eleccion = 0
        if numero_idiomas_eleccion != len(idiomas):
            raise forms.ValidationError(self.error_messages['idiomas_number'], code='idiomas_number')
        return idiomas

    def clean_conjuros_conocidos_0(self):
        clase = self.clase
        conjuros_conocidos_0 = self.cleaned_data.get('conjuros_conocidos_0')
        if conjuros_conocidos_0:
            cantidad_conjuros_conocidos_0 = clase.cantidad_conjuros_conocidos.get(nivel=0).cantidad
            if len(conjuros_conocidos_0) != cantidad_conjuros_conocidos_0:
                raise forms.ValidationError(self.error_messages['conjuros_conocidos_0_number'], code='conjuros_conocidos_0_number')
        return conjuros_conocidos_0
    
    def clean_conjuros_conocidos_1(self):
        clase = self.clase
        conjuros_conocidos_1 = self.cleaned_data.get('conjuros_conocidos_1')
        if conjuros_conocidos_1:
            cantidad_conjuros_conocidos_1 = clase.cantidad_conjuros_conocidos.get(nivel=1).cantidad
            if len(conjuros_conocidos_1) != cantidad_conjuros_conocidos_1:
                raise forms.ValidationError(self.error_messages['conjuros_conocidos_1_number'], code='conjuros_conocidos_1_number')
        return conjuros_conocidos_1
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None:
            if not re.match("^[A-Za-zÀ-ÿ ]*$", nombre):
                raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre

class CompaneroAnimalForm(forms.Form):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
        'trucos_number': ('No ha seleccionado el número de trucos correctos'),
        'habilidades_number': ('No ha seleccionado el número de habilidades correctos'),
    }

    nombre = forms.CharField(label='Nombre', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    dotes = forms.ModelChoiceField(queryset=Dote.objects.all().filter(es_dote_companero_animal=True), widget=forms.Select(), required=True)
    trucos = forms.ModelMultipleChoiceField(queryset=Truco.objects.all().filter(prerrequisito_truco=None), widget=forms.CheckboxSelectMultiple(), required=True)
    habilidades = forms.ModelMultipleChoiceField(queryset=Habilidad.objects.filter(es_habilidad_companero_animal=True), widget=forms.CheckboxSelectMultiple(), required=True)
    companero_animal_tipo = forms.ModelChoiceField(queryset=CompaneroAnimal.objects.all().exclude(tipo=None).filter(nivel=None).exclude(nivel_cambio=None), widget=forms.Select(), required=True)

    def __init__(self, *args, **kwargs):
        super(CompaneroAnimalForm, self).__init__(*args, **kwargs)
        self.companero_animal_nivel = CompaneroAnimal.objects.get(nivel=1, tipo=None)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None:
            if not re.match("^[A-Za-zÀ-ÿ ]*$", nombre):
                raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre
    
    def clean_trucos(self):
        trucos = self.cleaned_data.get('trucos')
        if len(trucos) != self.companero_animal_nivel.numero_trucos:
            raise forms.ValidationError(self.error_messages['trucos_number'], code='trucos_number')
        return trucos
    
    def clean_habilidades(self):
        habilidades = self.cleaned_data.get('habilidades')
        if len(habilidades) != self.companero_animal_nivel.puntos_habilidad:
            raise forms.ValidationError(self.error_messages['habilidades_number'], code='habilidades_number')
        return habilidades

class SubirNivelForm(forms.Form):

    error_messages = {
        'dotes_number': ("No ha elegido el número de dotes correcto"),
        'habilidades_number': ('No ha elegido el número de habilidades correcto'),
        'trucos_number': ('No ha seleccionado el número de trucos correctos'),
        'conjuros_number': ('No ha seleccionado el número de conjuros correctos'),
        'poderes_number': ('No ha seleccionado el número de poderes correcto')
    }

    CARACTERISTICA_CHOICES = (('Fuerza', 'Fuerza'), ('Destreza', 'Destreza'), ('Constitucion', 'Constitución'), ('Inteligencia', 'Inteligencia'), ('Sabiduria', 'Sabiduría'), ('Carisma', 'Carisma'), )

    eleccion_caracteristica_personaje = forms.ChoiceField(choices=CARACTERISTICA_CHOICES, widget=forms.Select(), required=False)
    eleccion_caracteristica_companero_animal = forms.ChoiceField(choices=CARACTERISTICA_CHOICES, widget=forms.Select(), required=False)
    eleccion_puntos_de_golpe = forms.BooleanField(label="", required=False, widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        personaje = kwargs.pop('personaje')
        clase = kwargs.pop('clase')
        numero_eleccion_dotes = kwargs.pop('numero_eleccion_dotes')
        numero_eleccion_habilidades = kwargs.pop('numero_eleccion_habilidades')
        numero_poderes = kwargs.pop('numero_poderes')
        companero_animal_nivel = kwargs.pop('companero_animal_nivel')
        cantidad_conjuros_conocidos_0_eleccion = kwargs.pop('cantidad_conjuros_conocidos_0_eleccion')
        cantidad_conjuros_conocidos_1_eleccion = kwargs.pop('cantidad_conjuros_conocidos_1_eleccion')
        cantidad_conjuros_conocidos_2_eleccion = kwargs.pop('cantidad_conjuros_conocidos_2_eleccion')
        cantidad_conjuros_conocidos_3_eleccion = kwargs.pop('cantidad_conjuros_conocidos_3_eleccion')
        cantidad_conjuros_conocidos_4_eleccion = kwargs.pop('cantidad_conjuros_conocidos_4_eleccion')
        cantidad_conjuros_conocidos_5_eleccion = kwargs.pop('cantidad_conjuros_conocidos_5_eleccion')
        cantidad_conjuros_conocidos_6_eleccion = kwargs.pop('cantidad_conjuros_conocidos_6_eleccion')
        cantidad_conjuros_conocidos_7_eleccion = kwargs.pop('cantidad_conjuros_conocidos_7_eleccion')
        cantidad_conjuros_conocidos_8_eleccion = kwargs.pop('cantidad_conjuros_conocidos_8_eleccion')
        cantidad_conjuros_conocidos_9_eleccion = kwargs.pop('cantidad_conjuros_conocidos_9_eleccion')
        super(SubirNivelForm, self).__init__(*args, **kwargs)
        self.personaje = Personaje.objects.get(pk=personaje.pk)
        self.clase = Clase.objects.get(pk=clase.pk)
        self.numero_eleccion_dotes = numero_eleccion_dotes
        self.numero_eleccion_habilidades = numero_eleccion_habilidades
        self.numero_poderes = numero_poderes
        self.cantidad_conjuros_conocidos_0_eleccion = cantidad_conjuros_conocidos_0_eleccion
        self.cantidad_conjuros_conocidos_1_eleccion = cantidad_conjuros_conocidos_1_eleccion
        self.cantidad_conjuros_conocidos_2_eleccion = cantidad_conjuros_conocidos_2_eleccion
        self.cantidad_conjuros_conocidos_3_eleccion = cantidad_conjuros_conocidos_3_eleccion
        self.cantidad_conjuros_conocidos_4_eleccion = cantidad_conjuros_conocidos_4_eleccion
        self.cantidad_conjuros_conocidos_5_eleccion = cantidad_conjuros_conocidos_5_eleccion
        self.cantidad_conjuros_conocidos_6_eleccion = cantidad_conjuros_conocidos_6_eleccion
        self.cantidad_conjuros_conocidos_7_eleccion = cantidad_conjuros_conocidos_7_eleccion
        self.cantidad_conjuros_conocidos_8_eleccion = cantidad_conjuros_conocidos_8_eleccion
        self.cantidad_conjuros_conocidos_9_eleccion = cantidad_conjuros_conocidos_9_eleccion
        numero_trucos = 0
        numero_dotes_companero_animal = 0
        numero_habilidades_companero_animal = 0
        if companero_animal_nivel:
            self.companero_animal_nivel = CompaneroAnimal.objects.get(pk=companero_animal_nivel.pk)
            companero_animal_nivel_menos = CompaneroAnimal.objects.get(nivel=companero_animal_nivel.nivel-1, tipo=None)
            self.numero_trucos = self.companero_animal_nivel.numero_trucos - companero_animal_nivel_menos.numero_trucos
            self.numero_dotes_companero_animal = self.companero_animal_nivel.numero_dotes - companero_animal_nivel_menos.numero_dotes
            self.numero_habilidades_companero_animal = self.companero_animal_nivel.puntos_habilidad - companero_animal_nivel_menos.puntos_habilidad
        else:
            self.companero_animal_nivel = companero_animal_nivel
            self.numero_trucos = numero_trucos
            self.numero_dotes_companero_animal = numero_dotes_companero_animal
            self.numero_habilidades_companero_animal = numero_habilidades_companero_animal
        dotes_personaje_nombre = []
        clase_nivel_0 = Clase.objects.get(clase=clase, nivel=0)
        for dote in personaje.dotes.all():
            dotes_personaje_nombre.append(dote.nombre)
        poderes_personaje_nombre = []
        for poder in personaje.poderes_conocidos.all():
            poderes_personaje_nombre.append(poder.nombre)
        companero_animal_personaje = personaje.companero_animal_personaje
        for ca in companero_animal_personaje.all():
            cap = ca
        trucos_nombre = []
        dotes_companero_animal_nombre = []
        if companero_animal_personaje.all():
            for truco in cap.trucos.all():
                trucos_nombre.append(truco.nombre)
            for dote in cap.dotes.all():
                dotes_companero_animal_nombre.append(dote.nombre)
        especiales_nombre = []
        for especial in clase.especiales.all():
            especiales_nombre.append(especial.nombre)
        conjuros_personaje_nombre = []
        for conjuro in personaje.conjuros_conocidos.all():
            conjuros_personaje_nombre.append(conjuro.nombre)
        queryset1 = Dote.objects.all().filter(prerrequisito_raza=personaje.raza).exclude(nombre__in=dotes_personaje_nombre)
        queryset2 = Dote.objects.all().filter(prerrequisito_raza=None).filter(nivel__lte=clase.nivel).filter(ataque_base__lte=clase.ataque_base_int).filter(prerrequisito_dote=None).exclude(pr_dote__in=personaje.dotes.all()).exclude(nombre__in=dotes_personaje_nombre)
        queryset3 = Dote.objects.all().filter(pr_dote__in=personaje.dotes.all()).exclude(nombre__in=dotes_personaje_nombre)
        queryset4 = clase_nivel_0.poderes.all().filter(nivel__lte=clase.nivel).exclude(pr_poder__in=personaje.poderes_conocidos.all())
        queryset5 = Poder.objects.all().filter(pr_poder__in=personaje.poderes_conocidos.all()).exclude(nombre__in=poderes_personaje_nombre)
        if not 'Talentos mejorados del pícaro' in especiales_nombre and clase.clase == 'Pícaro':
            queryset5 = queryset5.exclude(nivel__lt=10)
        queryset6 = Truco.objects.all().filter(prerrequisito_truco=None).exclude(nombre__in=trucos_nombre)
        if companero_animal_personaje.all():
            queryset7 = Truco.objects.all().filter(pr_truco__in=cap.trucos.all()).exclude(nombre__in=trucos_nombre)
        self.fields['dotes_personaje'] = forms.ModelMultipleChoiceField(queryset=(queryset1 | queryset2 | queryset3).distinct(), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['habilidades_personaje'] = forms.ModelMultipleChoiceField(queryset=Habilidad.objects, widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['poderes'] = forms.ModelChoiceField(queryset=queryset4 | queryset5, widget=forms.Select(), required=False)
        if companero_animal_personaje.all():
            self.fields['trucos'] = forms.ModelMultipleChoiceField(queryset=(queryset6 | queryset7).distinct(), widget=forms.CheckboxSelectMultiple(), required=False)
        else:
            self.fields['trucos'] = forms.ModelMultipleChoiceField(queryset=queryset6, widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['habilidades_companero_animal'] = forms.ModelMultipleChoiceField(queryset=Habilidad.objects.all().filter(es_habilidad_companero_animal=True), widget=forms.SelectMultiple(), required=False)
        self.fields['dotes_companero_animal'] = forms.ModelMultipleChoiceField(queryset=Dote.objects.all().filter(es_dote_companero_animal=True).exclude(nombre__in=dotes_companero_animal_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_0'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=0).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_1'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=1).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_2'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=2).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_3'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=3).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_4'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=4).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_5'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=5).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_6'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=6).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_7'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=7).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_8'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=8).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['conjuros_conocidos_9'] = forms.ModelMultipleChoiceField(queryset=clase.conjuros.all().filter(nivel=9).exclude(nombre__in=conjuros_personaje_nombre), widget=forms.CheckboxSelectMultiple(), required=False)
    
    def clean_dotes_personaje(self):
        dotes_personaje = self.cleaned_data.get('dotes_personaje')
        numero_dotes = self.numero_eleccion_dotes
        if len(dotes_personaje) != numero_dotes:
            raise forms.ValidationError(self.error_messages['dotes_number'], code='dotes_number')
        return dotes_personaje
    
    def clean_habilidades_personaje(self):
        habilidades_personaje = self.cleaned_data.get('habilidades_personaje')
        numero_eleccion_habilidades = self.numero_eleccion_habilidades
        if numero_eleccion_habilidades != len(habilidades_personaje):
            raise forms.ValidationError(self.error_messages['habilidades_number'], code='habilidades_number')
        return habilidades_personaje
    
    def clean_poderes(self):
        poderes = self.cleaned_data.get('poderes')
        set_poderes = []
        set_poderes.append(poderes)
        numero_poderes = self.numero_poderes
        if numero_poderes != len(set_poderes) and poderes != None:
            raise forms.ValidationError(self.error_messages['poderes_number'], code='poderes_number')
        return poderes

    def clean_trucos(self):
        trucos = self.cleaned_data.get('trucos')
        if self.numero_trucos != len(trucos):
            raise forms.ValidationError(self.error_messages['trucos_number'], code='trucos_number')
        return trucos

    def clean_habilidades_companero_animal(self):
        habilidades_companero_animal = self.cleaned_data.get('habilidades_companero_animal')
        if self.numero_habilidades_companero_animal != len(habilidades_companero_animal):
            raise forms.ValidationError(self.error_messages['habilidades_companero_animal'], code='habilidades_companero_animal')
        return habilidades_companero_animal
    
    def clean_dotes_companero_animal(self):
        dotes_companero_animal = self.cleaned_data.get('dotes_companero_animal')
        if self.numero_dotes_companero_animal != len(dotes_companero_animal):
            raise forms.ValidationError(self.error_messages['dotes_number'], code='dotes_number')
        return dotes_companero_animal

    def clean_conjuros_conocidos_0(self):
        conjuros_conocidos_0 = self.cleaned_data.get('conjuros_conocidos_0')
        if len(conjuros_conocidos_0) != self.cantidad_conjuros_conocidos_0_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_0
    
    def clean_conjuros_conocidos_1(self):
        conjuros_conocidos_1 = self.cleaned_data.get('conjuros_conocidos_1')
        if len(conjuros_conocidos_1) != self.cantidad_conjuros_conocidos_1_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_1
    
    def clean_conjuros_conocidos_2(self):
        conjuros_conocidos_2 = self.cleaned_data.get('conjuros_conocidos_2')
        if len(conjuros_conocidos_2) != self.cantidad_conjuros_conocidos_2_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_2

    def clean_conjuros_conocidos_3(self):
        conjuros_conocidos_3 = self.cleaned_data.get('conjuros_conocidos_3')
        if len(conjuros_conocidos_3) != self.cantidad_conjuros_conocidos_3_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_3

    def clean_conjuros_conocidos_4(self):
        conjuros_conocidos_4 = self.cleaned_data.get('conjuros_conocidos_4')
        if len(conjuros_conocidos_4) != self.cantidad_conjuros_conocidos_4_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_4

    def clean_conjuros_conocidos_5(self):
        conjuros_conocidos_5 = self.cleaned_data.get('conjuros_conocidos_5')
        if len(conjuros_conocidos_5) != self.cantidad_conjuros_conocidos_5_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_5

    def clean_conjuros_conocidos_6(self):
        conjuros_conocidos_6 = self.cleaned_data.get('conjuros_conocidos_6')
        if len(conjuros_conocidos_6) != self.cantidad_conjuros_conocidos_6_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_6

    def clean_conjuros_conocidos_7(self):
        conjuros_conocidos_7 = self.cleaned_data.get('conjuros_conocidos_7')
        if len(conjuros_conocidos_7) != self.cantidad_conjuros_conocidos_7_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_7

    def clean_conjuros_conocidos_8(self):
        conjuros_conocidos_8 = self.cleaned_data.get('conjuros_conocidos_8')
        if len(conjuros_conocidos_8) != self.cantidad_conjuros_conocidos_8_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_8

    def clean_conjuros_conocidos_9(self):
        conjuros_conocidos_9 = self.cleaned_data.get('conjuros_conocidos_9')
        if len(conjuros_conocidos_9) != self.cantidad_conjuros_conocidos_9_eleccion:
            raise forms.ValidationError(self.error_messages['conjuros_number'], code='conjuros_number')
        return conjuros_conocidos_9