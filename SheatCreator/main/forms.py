from django import forms
from main.models import Perfil
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class EditarUsernameForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ('username', )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")

        if len(username) < 6:
            msg = "El nombre de usuario debe tener al menos 6 caracteres"
            raise ValidationError({'username': [msg, ]})

        if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", username):
            msg = "El nombre de usuario solo puede contener letras y numeros"
            raise ValidationError({'username': [msg, ]})

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            msg = "El nombre de usuario ya esta en uso"
            raise ValidationError({'username': [msg, ]})
    
class EditarPasswordForm(forms.Form):

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    check_pw = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        check_pw = cleaned_data.get("check_pw")
        if password != check_pw:
            msg = "La contraseña no coincide"
            raise ValidationError({'password': [msg, ]})

        if len(password) < 8:
            msg = "La contraseña debe tener al menos 8 caracteres"
            raise ValidationError({'password': [msg, ]})

        if not re.match("^[A-Za-z0-9\u00f1\u00d1]*$", password):
            msg = "La contraseña solo puede contener letras y numeros"
            raise ValidationError({'password': [msg, ]})

        if not any(x.isupper() for x in password):
            msg = "La contraseña debe contener al menos una mayuscula"
            raise ValidationError({'password': [msg, ]})

class EditarPerfilForm(forms.ModelForm):

    error_messages = {
        'nickname_letters': ("El nombre solo puede contener letras y símbolos"),
    }

    nickname = forms.CharField(label="Nickname", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nickname'}))
    class Meta:
        model = Perfil
        fields = (
            "nickname",
        )

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", nickname):
            raise forms.ValidationError(
                self.error_messages['nickname'],
                code='nickname',
            )
        
        if Perfil.objects.exclude(pk=self.instance.pk).filter(nickname=nickname).exists():
            msg = "El nickname ya esta en uso"
            raise ValidationError({'nickname': [msg, ]})

        return nickname