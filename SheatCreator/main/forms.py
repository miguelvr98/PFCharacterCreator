from django import forms
from main.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import *
import re

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
    nivel = forms.IntegerField(label='Nivel', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nivel', 'min':1, 'max':20}))
    ataque_base = forms.IntegerField(label='Ataque base', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ataque base', 'min':1, 'max':20}))
    fuerza = forms.IntegerField(label='Fuerza', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fuerza', 'min':1}))
    destreza = forms.IntegerField(label='Destreza', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Destreza', 'min':1}))
    constitucion = forms.IntegerField(label='Constitucion', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Constitución', 'min':1}))
    inteligencia = forms.IntegerField(label='Inteligencia', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Inteligencia', 'min':1}))
    sabiduria = forms.IntegerField(label='Sabiduria', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sabiduría', 'min':1}))
    carisma = forms.IntegerField(label='Carisma', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Carisma', 'min':1}))
    es_dote_companero_animal = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    prerrequisito_raza = forms.ModelChoiceField(queryset=Raza.objects, widget=forms.Select(), required=False)
    prerrequisito_dote = forms.ModelMultipleChoiceField(queryset=Dote.objects, widget=forms.CheckboxSelectMultiple(), required=False)

    class Meta:
        model = Dote
        fields = ('nombre', 'tipo', 'nivel', 'ataque_base', 'fuerza', 'destreza', 'constitucion', 'inteligencia', 'sabiduria', 'carisma', 'es_dote_companero_animal', 'prerrequisito_raza', 'prerrequisito_dote')

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match("^[A-Za-zÀ-ÿ]*$", nombre):
            raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        
        if Dote.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError(self.error_messages['nombre_exists'],code='nombre_exists')
        return nombre

class BuscarDoteForm(forms.Form):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
    }
    TIPO_CHOICES = (('General', 'General'), ('Combate', 'Combate'), ('Metamágica', 'Metamágica'), (None, '---------'), )

    nombre = forms.CharField(label='Nombre', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo'}))
    es_dote_companero_animal = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None:
            if not re.match("^[A-Za-zÀ-ÿ]*$", nombre):
                raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre

class BuscarPoderForm(forms.Form):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
    }

    nombre = forms.CharField(label='Nombre', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None:
            if not re.match("^[A-Za-zÀ-ÿ]*$", nombre):
                raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre

class BuscarConjuroForm(forms.Form):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
    }

    nombre = forms.CharField(label='Nombre', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    nivel = forms.IntegerField(label='Nivel', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nivel', 'min':0, 'max':9}))

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None:
            if not re.match("^[A-Za-zÀ-ÿ]*$", nombre):
                raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre

class BuscarPersonajeForm(forms.Form):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras"),
    }

    nombre = forms.CharField(label='Nombre', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    clase = forms.ModelChoiceField(queryset=Clase.objects.all().filter(nivel=0), widget=forms.Select(), required=False)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None:
            if not re.match("^[A-Za-zÀ-ÿ]*$", nombre):
                raise forms.ValidationError(self.error_messages['nombre_letters'], code='nombre_letters')
        return nombre