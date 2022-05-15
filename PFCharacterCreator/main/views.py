from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from main.models import *
from main.forms import *
from django.core.paginator import Paginator
import math
import random
# import jinja2
# import flask
#import io
#from django.http import FileResponse
#from reportlab.pdfgen import canvas

# Create your views here.

#Este método devuelve el Perfil del usuario
def usuario_logueado(request):
    try:
        id_user = request.user.id
        user_actual = get_object_or_404(User, pk=id_user)
        perfil = Perfil.objects.get(usuario=user_actual)
        return perfil 
    except:
        return redirect('error_url')

@login_required(login_url='/login/')
def editar_usuario(request):
    try:
        usuario = User.objects.get(pk=request.user.id)
        perfil = Perfil.objects.get(usuario=usuario)
        if request.method == 'POST':
            form = EditarUsernameForm(data=request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('perfil'+str(perfil.id))
            else:
                return render(request, 'editarPerfil.html', {'form':form})
        else:
            form = EditarUsernameForm(instance=usuario)
            return render(request, 'editarPerfil.html', {'form':form})
    except:
        redirect('error_url')

def listar_razas(request):
        razas = Raza.objects.all()
        paginator = Paginator(razas, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'raza/list.html', {'razas':page_obj})

def listar_dotes(request):
    try:
        dotes = Dote.objects.all()
        buscador = BuscarDoteForm(var=False)
        paginator = Paginator(dotes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'dote/list.html', {'dotes':page_obj, 'buscador':buscador})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def listar_dotes_propias(request):
    try:
        perfil = usuario_logueado(request)
        dotes = Dote.objects.all().filter(creador=perfil)
        buscador = BuscarDoteForm(var=True)
        paginator = Paginator(dotes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'dote/list.html', {'dotes':page_obj, 'buscador':buscador})
    except:
        return redirect('error_url')

def listar_clases(request):
    try:
        clases = Clase.objects.all().filter(nivel=0)
        return render(request, 'clase/list.html', {'clases':clases})
    except:
        return redirect('error_url')

def listar_habilidades(request):
    try:
        habilidades = Habilidad.objects.all()
        paginator = Paginator(habilidades, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'habilidad/list.html', {'habilidades':page_obj})
    except:
        return redirect('error_url')

#Mirar como meter paginación aquí y revisar las queries
def listar_companeros_animales(request):
    companeros_animales_por_nivel = CompaneroAnimal.objects.all().filter(es_familiar=False).filter(tipo=None).exclude(nivel=0)
    companeros_animales_por_tipo = CompaneroAnimal.objects.all().filter(es_familiar=False).filter(nivel=None)
    familiares = CompaneroAnimal.objects.all().filter(es_familiar=True).exclude(tipo=None)
    aux_ca = CompaneroAnimal.objects.get(nivel=0)
    especiales = aux_ca.especiales.all()
    return render(request, 'companero_animal/list.html', {'companeros_animales_por_nivel':companeros_animales_por_nivel, 'companeros_animales_por_tipo':companeros_animales_por_tipo, 'familiares':familiares, 'especiales':especiales})

def listar_trucos(request):
    try:
        trucos = Truco.objects.all()
        paginator = Paginator(trucos, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'truco/list.html', {'trucos':page_obj})
    except:
        return redirect('error_url')

def listar_propiedades(request):
    try:
        propiedades_arma = Propiedad.objects.all().filter(es_propiedad_arma=True)
        propiedades_armadura = Propiedad.objects.all().filter(es_propiedad_armadura=True)
        propiedades_comun = Propiedad.objects.all().filter(es_propiedad_armadura=True).filter(es_propiedad_arma=True)
        return render(request, 'propiedad/list.html', {'propiedades_arma':propiedades_arma, 'propiedades_armadura':propiedades_armadura, 'propiedades_comun':propiedades_comun})
    except:
        return redirect('error_url')

def listar_linajes(request):
    try:
        linajes = Linaje.objects.all()
        return render(request, 'linaje/list.html', {'linajes':linajes})
    except:
        return redirect('error_url')

def listar_objetos(request):
    try:
        armas = Arma.objects.all()
        armaduras = Armadura.objects.all()
        return render(request, 'objeto/list.html', {'armas':armas, 'armaduras':armaduras})
    except:
        return redirect('error_url')

def listar_personajes_publicos(request):
    try:
        personajes = Personaje.objects.all().filter(es_publico=True)
        buscador = BuscarPersonajeForm(var=False)
        paginator = Paginator(personajes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'personaje/list.html', {'personajes':page_obj, 'buscador':buscador})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def listar_personajes_propios(request):
    try:
        perfil = usuario_logueado(request)
        personajes = Personaje.objects.all().filter(perfil=perfil)
        buscador = BuscarPersonajeForm(var=True)
        paginator = Paginator(personajes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'personaje/list.html', {'personajes':page_obj, 'buscador':buscador})
    except:
        redirect('error_url')

def listar_poderes_por_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        poderes = clase.poderes.all()
        buscador = BuscarPoderForm()
        paginator = Paginator(poderes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'poder/list.html', {'poderes':page_obj, 'buscador':buscador, 'pk':pk})
    except:
        return redirect('error_url')

def listar_especiales_por_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        especiales = clase.especiales.all()
        return render(request, 'especial/list.html', {'especiales':especiales})
    except:
        return redirect('error_url')

#Mirar si meter paginación
def listar_conjuros_por_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        conjuros = clase.conjuros.all()
        buscador = BuscarConjuroForm()
        paginator = Paginator(conjuros, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'conjuro/list.html', {'conjuros':page_obj, 'buscador':buscador, 'pk':pk})
    except:
        return redirect('error_url')

def mostrar_raza(request, pk):
    try:
        raza = Raza.objects.get(pk=pk)
        bonificaciones_raza = raza.bonificaciones_raza.all()
        return render(request, 'raza/show.html', {'raza':raza, 'bonificaciones_raza':bonificaciones_raza})
    except:
        return redirect('error_url')

def mostrar_dote(request, pk):
    dote = Dote.objects.get(pk=pk)
    perfil = usuario_logueado(request)
    if dote.prerrequisito_dote.all() and dote.prerrequisito_raza != None:
        prerrequisito_dote = dote.prerrequisito_dote.all()
        prerrequisito_raza = dote.prerrequisito_raza
        return render(request, 'dote/show.html', {'dote':dote, 'prerrequisito_dote':prerrequisito_dote, 'prerrequisito_raza':prerrequisito_raza})
    elif dote.prerrequisito_dote.all() and dote.prerrequisito_raza == None:
        prerrequisito_dote = dote.prerrequisito_dote.all()
        return render(request, 'dote/show.html', {'dote':dote, 'prerrequisito_dote':prerrequisito_dote})
    prerrequisito_raza = dote.prerrequisito_raza
    return render(request, 'dote/show.html', {'dote':dote, 'prerrequisito_raza':prerrequisito_raza, 'perfil':perfil})

def mostrar_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        clases_nivel = Clase.objects.all().filter(clase=clase.clase).exclude(nivel=0).order_by('nivel')
        clase_1 = Clase.objects.filter(clase=clase.clase).get(nivel=1)
        especiales = clase.especiales.all()
        habilidades = clase_1.habilidades.all()
        return render(request, 'clase/show.html', {'clase':clase, 'clases_nivel':clases_nivel, 'especiales':especiales, 'habilidades':habilidades})
    except:
        return redirect('error_url')

def mostrar_conjuro(request, pk):
    try:
        conjuro = Conjuro.objects.get(pk=pk)
        return render(request, 'conjuro/show.html', {'conjuro':conjuro})
    except:
        return redirect('error_url')

def mostrar_poder(request, pk):
    try:
        poder = Poder.objects.get(pk=pk)
        return render(request, 'poder/show.html', {'poder':poder})
    except:
        return redirect('error_url')

def mostrar_companero_animal(request, pk):
    try:
        companero_animal = CompaneroAnimal.objects.get(pk=pk)
        assert companero_animal.tipo != None
        especiales = companero_animal.especiales.all()
        return render(request, 'companero_animal/show.html', {'companero_animal':companero_animal, 'especiales':especiales})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def mostrar_companero_animal_personaje(request, pk):
    personaje = Personaje.objects.get(pk=pk)
    if personaje.es_publico==False:
        perfil = usuario_logueado(request)
        assert perfil == personaje.perfil
    companero_animal = CompaneroAnimalPersonaje.objects.get(personaje=personaje)
    dotes = companero_animal.dotes.all()
    trucos = companero_animal.trucos.all()
    especiales = companero_animal.especiales.all()
    return render(request, 'companero_animal/show.html', {'companero_animal':companero_animal, 'dotes':dotes, 'trucos':trucos, 'especiales':especiales})

def mostrar_truco(request, pk):
    truco = Truco.objects.get(pk=pk)
    if truco.prerrequisito_truco.all():
        prerrequisito_truco = truco.prerrequisito_truco.all()
        return render(request, 'truco/show.html', {'truco':truco, 'prerrequisito_truco':prerrequisito_truco})
    return render(request, 'truco/show.html', {'truco':truco})

def mostrar_propiedad(request, pk):
    try:
        propiedad = Propiedad.objects.get(pk=pk)
        return render(request, 'propiedad/show.html', {'propiedad':propiedad})
    except:
        return redirect('error_url')

def mostrar_linaje(request, pk):
    try:
        linaje = Linaje.objects.get(pk=pk)
        conjuros = linaje.conjuros.all()
        dotes = linaje.dotes.all()
        poderes = linaje.poderes.all()
        return render(request, 'linaje/show.html', {'linaje':linaje, 'conjuros':conjuros, 'dotes':dotes, 'poderes':poderes})
    except:
        return redirect('error_url')

def mostrar_objeto(request, pk):
    try:
        if Arma.objects.get(pk=pk):
            objeto = Arma.objects.get(pk=pk)
        else:
            objeto = Armadura.objects.get(pk=pk)
        return render(request, 'objeto/show.html', {'objeto':objeto})
    except:
        return redirect('error_url')

def mostrar_personaje(request, pk):
    try:
        personaje = Personaje.objects.get(pk=pk)
        perfil = usuario_logueado(request)
        if personaje.es_publico == False:
            assert personaje.perfil == perfil
        idiomas = personaje.idiomas.all()
        clase = personaje.clase
        clase_nivel_0 = Clase.objects.get(nivel=0, clase=clase.clase)
        dotes = personaje.dotes.all()
        conjuros = personaje.conjuros_conocidos.all()
        poderes = personaje.poderes_conocidos.all()
        inventario = personaje.propiedades_objeto.all()
        return render(request, 'personaje/show.html', {'personaje':personaje, 'conjuros':conjuros, 'poderes':poderes, 'inventario':inventario, 'perfil':perfil, 'clase_nivel_0':clase_nivel_0})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def cambiar_personaje_a_publico(request, pk):
    try:
        perfil = usuario_logueado(request)
        personaje = Personaje.objects.get(pk=pk)
        assert personaje.perfil == perfil
        assert personaje.es_publico == False
        personaje.es_publico = True
        personaje.save()

        personajes = Personaje.objects.all().filter(perfil=perfil)
        return redirect('/personaje/show/'+str(personaje.pk))
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def cambiar_personaje_a_privado(request, pk):
    try:
        perfil = usuario_logueado(request)
        personaje = Personaje.objects.get(pk=pk)
        assert personaje.perfil == perfil
        assert personaje.es_publico == True
        personaje.es_publico = False
        personaje.save()

        personajes = Personaje.objects.all().filter(perfil=perfil)
        return redirect('/personaje/show/'+str(personaje.pk))
    except:
        return redirect('error_url')

def registrar_usuario(request):
    try:
        if request.user.is_authenticated == True:
            return redirect('error_url')

        if request.method == 'POST':
            form_usuario = UserForm(request.POST)
            form_perfil = PerfilForm(request.POST)
            form_gdpr = GDPRForm(request.POST)
            if form_usuario.is_valid() and form_perfil.is_valid() and form_gdpr.is_valid():
                usuario = form_usuario.save()
                perfil = form_perfil.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

                username = form_usuario.cleaned_data['username']
                password = form_usuario.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
        else:
            form_usuario = UserForm()
            form_perfil = PerfilForm()
            form_gdpr = GDPRForm()
        return render(request, 'registration/register.html', {'form_usuario':form_usuario, 'form_perfil':form_perfil, 'form_gdpr':form_gdpr})
    except:
        redirect('error_url')

@login_required(login_url="/login/")
def crear_dote(request):
    if request.method == 'POST':
        form_dote = DoteForm(request.POST)
        perfil = usuario_logueado(request)
        if form_dote.is_valid():
            dote = form_dote.save(commit=False)
            dote.creador = perfil
            dote.nombre = dote.nombre + ' (3er party)'
            dote.descripcion = form_dote.cleaned_data.get('descripcion')
            dote.save()

            return redirect('/dote/show/'+ str(dote.pk))
    else:
         form_dote = DoteForm()
    return render(request, 'dote/edit.html', {'form_dote':form_dote})

@login_required(login_url="/login/")
def editar_dote(request, pk):
    try:
        dote = Dote.objects.get(pk=pk)
        perfil = usuario_logueado(request)
        assert dote.creador == perfil
        if request.method == 'POST':
            form_dote = DoteForm(request.POST, instance=dote)
            perfil = usuario_logueado(request)
            if form_dote.is_valid():
                form_dote.save()
                return redirect('/dote/show/'+ str(dote.pk))
        else:
            form_dote = DoteForm(instance=dote)
        return render(request, 'dote/edit.html', {'form_dote':form_dote})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def eliminar_dote(request, pk):
    try:
        perfil = usuario_logueado(request)
        dote = Dote.objects.get(pk=pk)
        assert dote.creador == perfil
        dote.creador = None
        dote.save()
        return redirect('/dote/perfil/list')
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def mostrar_perfil_propio(request):
    perfil = usuario_logueado(request)
    personajes = Personaje.objects.all().filter(perfil=perfil)
    paginator_personajes = Paginator(personajes, 5)
    page_number_personajes = request.GET.get('page_personaje')
    page_obj_personajes = paginator_personajes.get_page(page_number_personajes)
    dotes = Dote.objects.all().filter(creador=perfil)
    paginator_dotes = Paginator(dotes, 5)
    page_number_dotes = request.GET.get('page_dote')
    page_obj_dotes = paginator_dotes.get_page(page_number_dotes)
    var=True
    num_barbaro = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Bárbaro").count()
    num_bardo = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Bardo").count()
    num_clerigo = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Clérigo").count()
    num_druida = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Druida").count()
    num_explorador = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Explorador").count()
    num_guerrero = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Guerrero").count()
    num_hechicero = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Hechicero").count()
    num_mago = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Mago").count()
    num_monje = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Monje").count()
    num_paladin = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Paladín").count()
    num_picaro = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Pícaro").count()
    return render(request, 'perfil/show.html', {'perfil':perfil, 'personajes':page_obj_personajes, 'num_barbaro':num_barbaro,
         'num_bardo':num_bardo, 'num_clerigo':num_clerigo, 'num_druida':num_druida, 'num_explorador':num_explorador,
          'num_guerrero':num_guerrero, 'num_hechicero':num_hechicero, 'num_mago':num_mago, 'num_monje':num_monje,
          'num_paladin':num_paladin, 'num_picaro':num_picaro, 'dotes':page_obj_dotes, 'var':var})
    
@login_required(login_url="/login/")
def mostrar_perfil(request, pk):
    try:
        perfil = Perfil.objects.get(pk=pk)
        personajes = Personaje.objects.all().filter(perfil=perfil).filter(es_publico=True)
        paginator_personajes = Paginator(personajes, 5)
        page_number_personajes = request.GET.get('page_personaje')
        page_obj_personajes = paginator_personajes.get_page(page_number_personajes)
        dotes = Dote.objects.all().filter(creador=perfil)
        paginator_dotes = Paginator(dotes, 5)
        page_number_dotes = request.GET.get('page_dote')
        page_obj_dotes = paginator_dotes.get_page(page_number_dotes)
        var=False
        num_barbaro = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Bárbaro").count()
        num_bardo = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Bardo").count()
        num_clerigo = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Clérigo").count()
        num_druida = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Druida").count()
        num_explorador = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Explorador").count()
        num_guerrero = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Guerrero").count()
        num_hechicero = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Hechicero").count()
        num_mago = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Mago").count()
        num_monje = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Monje").count()
        num_paladin = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Paladín").count()
        num_picaro = Personaje.objects.all().filter(perfil=perfil).filter(clase__clase="Pícaro").count()
        return render(request, 'perfil/show.html', {'perfil':perfil, 'personajes':page_obj_personajes, 'num_barbaro':num_barbaro,
         'num_bardo':num_bardo, 'num_clerigo':num_clerigo, 'num_druida':num_druida, 'num_explorador':num_explorador,
          'num_guerrero':num_guerrero, 'num_hechicero':num_hechicero, 'num_mago':num_mago, 'num_monje':num_monje,
          'num_paladin':num_paladin, 'num_picaro':num_picaro, 'dotes':page_obj_dotes, 'var':var})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def editar_usuario(request):
    try:
        usuario = User.objects.get(pk=request.user.id)   
        if request.method == 'POST':
            form_editar_username = EditarUsernameForm(request.POST)
            if form_editar_username.is_valid():
                username = form_editar_username.cleaned_data.get('username')
                usuario.username = username
                usuario.save()
                return redirect('mostrar_perfil_propio_url')
        else:
            form_editar_username = EditarUsernameForm(instance=usuario)
        return render(request, 'perfil/edit.html', {'form_editar_username':form_editar_username})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def editar_contrasena(request):
    try:
        usuario = User.objects.get(pk=request.user.id)
        if request.method == 'POST':
            form_editar_contrasena = EditarContrasenaForm(request.POST)
            if form_editar_contrasena.is_valid():
                password = form_editar_contrasena.cleaned_data.get('password1')
                usuario.set_password(password)
                usuario.save()
                return redirect('/login')
        else:
            form_editar_contrasena = EditarContrasenaForm()
        return render(request, 'perfil/edit.html', {'form_editar_contrasena':form_editar_contrasena})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def editar_perfil(request):
    try:
        perfil = usuario_logueado(request)
        if request.method == 'POST':
            form_editar_perfil = PerfilForm(request.POST)
            if form_editar_perfil.is_valid():
                nickname = form_editar_perfil.cleaned_data.get('nickname')
                perfil.nickname = nickname
                perfil.save()
                return redirect('mostrar_perfil_propio_url')
        else:
            form_editar_perfil = PerfilForm(instance=perfil)
        return render(request, 'perfil/edit.html', {'form_editar_perfil':form_editar_perfil})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def eliminar_usuario(request):
    try:
        usuario = User.objects.get(pk=request.user.id)
        usuario.delete()
        return redirect('/')
    except:
        return redirect('error_url')

def buscar_dote(request):
    try:
        dotes = Dote.objects.all()
        if request.method == 'POST':
            var = request.POST.get('var')
            if var == 'True':
                var = True
            elif var == 'False':
                var = False
            buscador = BuscarDoteForm(request.POST, var=var)
            if buscador.is_valid():
                nombre = buscador.cleaned_data.get('nombre')
                tipo = buscador.cleaned_data.get('tipo')
                es_dote_companero_animal = buscador.cleaned_data.get('es_dote_companero_animal')

                if var == True:
                    perfil = usuario_logueado(request)
                    dotes = Dote.objects.all().filter(creador=perfil)

                if nombre != None and nombre != '':
                    dotes = dotes.filter(nombre__icontains=nombre)
                if tipo != '':
                    dotes = dotes.filter(tipo=tipo)
                if es_dote_companero_animal == True:
                    dotes = dotes.filter(es_dote_companero_animal=True)

            paginator = Paginator(dotes, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, 'dote/list.html', {'dotes':page_obj, 'buscador':buscador})
    except:
        return redirect('error_url')

def buscar_poder(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        poderes = clase.poderes.all()
        if request.method == 'POST':
            buscador = BuscarPoderForm(request.POST)
            if buscador.is_valid():
                nombre = buscador.cleaned_data.get('nombre')

                if nombre != None and nombre != '':
                    poderes = poderes.filter(nombre__icontains=nombre)
            paginator = Paginator(poderes, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            buscador = BuscarPoderForm()
        return render(request, 'poder/list.html', {'poderes':page_obj, 'buscador':buscador, 'pk':pk})
    except:
        return redirect('error_url')

def buscar_conjuro(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        conjuros = clase.conjuros.all()
        if request.method == 'POST':
            buscador = BuscarConjuroForm(request.POST)
            if buscador.is_valid():
                nombre = buscador.cleaned_data.get('nombre')
                nivel = buscador.cleaned_data.get('nivel')

                if nombre != None and nombre != '':
                    conjuros = conjuros.filter(nombre__icontains=nombre)
                
                if nivel != None:
                    conjuros = conjuros.filter(nivel=nivel)
            paginator = Paginator(conjuros, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            buscador = BuscarConjuroForm()
        return render(request, 'conjuro/list.html', {'conjuros':page_obj, 'buscador':buscador, 'pk':pk})
    except:
        return redirect('error_url')

def buscar_personaje(request):
    try:
        personajes = Personaje.objects.all().exclude(es_publico=False)
        personajes_aux = Personaje.objects.none()
        if request.user.is_authenticated:
            perfil = usuario_logueado(request)
            personajes_aux = Personaje.objects.all().filter(perfil=perfil).filter(es_publico=True)
        if request.method == 'POST':
            var = request.POST.get('var')
            if var == 'True':
                var = True
            elif var == 'False':
                var = False
            buscador = BuscarPersonajeForm(request.POST, var=var)
            if buscador.is_valid():
                nombre = buscador.cleaned_data.get('nombre')
                clase = buscador.cleaned_data.get('clase')
                personajes = (personajes | personajes_aux).distinct()

                if var == True:
                    personajes = Personaje.objects.all().filter(perfil=perfil)

                if nombre != None and nombre != '':
                    personajes = personajes.filter(nombre__icontains=nombre)
                    
                if clase != None:
                    clases = Clase.objects.all().filter(clase=clase.clase)
                    personajes = personajes.filter(clase__in=clases)

            paginator = Paginator(personajes, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, 'personaje/list.html', {'personajes':page_obj, 'buscador':buscador})
    except:
        return redirect('error_url')

#Elección de puntos, nombre, raza y clase (falta poner como quiere el usuario que sean los puntos de golpe)
@login_required(login_url="/login/")
def crear_personaje_1(request):
    try:
        perfil = usuario_logueado(request)
        puntos_a_elegir = 15
        if request.method == 'POST':
            formulario = PersonajeForm(request.POST)
            if formulario.is_valid():
                raza = formulario.cleaned_data.get('raza')
                clase = formulario.cleaned_data.get('clase')
                tipo = formulario.cleaned_data.get('tipo')
                alineamiento = formulario.cleaned_data.get('alineamiento')
                if tipo == 'Alta fantasía':
                    puntos_a_elegir = 20
                elif tipo == 'Épica':
                    puntos_a_elegir = 25
                formulario_paso_2 = PersonajeForm2(raza=raza, puntos_a_elegir=puntos_a_elegir)
                return render(request, 'personaje/paso2.html', {'raza':raza, 'clase':clase, 'alineamiento':alineamiento, 'formulario_paso_2':formulario_paso_2, 'puntos_a_elegir':puntos_a_elegir})
        else:
            formulario = PersonajeForm()
        return render(request, 'personaje/paso1.html', {'formulario':formulario})
    except:
        return redirect('error_url')

#Elección de puntos de características
@login_required(login_url="/login/")
def crear_personaje_2(request):
    if request.method == 'POST':
        raza = Raza.objects.get(raza=request.POST.get('raza'))
        puntos_a_elegir = request.POST.get('puntos_a_elegir')
        formulario_paso_2 = PersonajeForm2(request.POST, raza=raza, puntos_a_elegir=puntos_a_elegir)
        clase = Clase.objects.get(clase=request.POST.get('clase'), nivel=1)
        alineamiento = request.POST.get('alineamiento')
        if formulario_paso_2.is_valid():
            caracteristica_choice = formulario_paso_2.cleaned_data.get('caracteristica_choice')
            fuerza = formulario_paso_2.cleaned_data.get('fuerza')
            destreza = formulario_paso_2.cleaned_data.get('destreza')
            constitucion = formulario_paso_2.cleaned_data.get('constitucion')
            inteligencia = formulario_paso_2.cleaned_data.get('inteligencia')
            sabiduria = formulario_paso_2.cleaned_data.get('sabiduria')
            carisma = formulario_paso_2.cleaned_data.get('carisma')
            if caracteristica_choice:
                fuerza, destreza, constitucion, inteligencia, sabiduria, carisma = modificar_caracteristica(caracteristica_choice, fuerza, destreza, constitucion, inteligencia, sabiduria, carisma)
            else:
                fuerza, destreza, constitucion, inteligencia, sabiduria, carisma = modificar_caracteristica2(raza, fuerza, destreza, constitucion, inteligencia, sabiduria, carisma)
            formulario_paso_3 = PersonajeForm3(raza=raza, clase=clase, inteligencia=inteligencia)
            clase_nivel_0 = Clase.objects.get(clase=request.POST.get('clase'), nivel=0)
            numero_habilidades_eleccion = clase_nivel_0.puntos_de_habilidad_por_nivel + math.floor((inteligencia-10)/2)
            if numero_habilidades_eleccion <= 0:
                numero_habilidades_eleccion = 1
            numero_idiomas_eleccion = math.floor((inteligencia-10)/2)
            if numero_idiomas_eleccion < 0:
                numero_idiomas_eleccion = 0
            cantidad_conjuros_conocidos_0_eleccion = None
            cantidad_conjuros_conocidos_1_eleccion = None
            if clase.cantidad_conjuros_conocidos.all():
                cantidad_conjuros_conocidos_0_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=0).cantidad
                cantidad_conjuros_conocidos_1_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=1).cantidad
            return render(request, 'personaje/paso3.html', {'raza':raza, 'clase':clase, 'alineamiento':alineamiento, 'fuerza':fuerza, 'destreza':destreza, 'constitucion':constitucion, 'inteligencia':inteligencia, 'sabiduria':sabiduria, 'carisma':carisma, 'formulario_paso_3':formulario_paso_3, 'numero_habilidades_eleccion':numero_habilidades_eleccion, 'numero_idiomas_eleccion':numero_idiomas_eleccion, 'cantidad_conjuros_conocidos_0_eleccion':cantidad_conjuros_conocidos_0_eleccion, 'cantidad_conjuros_conocidos_1_eleccion':cantidad_conjuros_conocidos_1_eleccion, 'clase_nivel_0':clase_nivel_0})
    return render(request, 'personaje/paso2.html', {'raza':raza, 'clase':clase, 'formulario_paso_2':formulario_paso_2, 'puntos_a_elegir':puntos_a_elegir, 'alineamiento':alineamiento})

def modificar_caracteristica(caracteristica_choice, fuerza, destreza, constitucion, inteligencia, sabiduria, carisma):
    if caracteristica_choice == 'Fuerza':
        fuerza = fuerza + 2
    elif caracteristica_choice == 'Destreza':
        destreza == destreza + 2
    elif caracteristica_choice == 'Constitucion':
        constitucion = constitucion + 2
    elif caracteristica_choice == 'Inteligencia':
        inteligencia = inteligencia + 2
    elif caracteristica_choice == 'Sabiduria':
        sabiduria = sabiduria + 2
    elif caracteristica_choice == 'Carisma':
        carisma = carisma + 2
    return fuerza, destreza, constitucion, inteligencia, sabiduria, carisma

def modificar_caracteristica2(raza, fuerza, destreza, constitucion, inteligencia, sabiduria, carisma):
    fuerza = fuerza + raza.fuerza
    destreza = destreza + raza.fuerza
    constitucion = constitucion + raza.constitucion
    inteligencia = inteligencia + raza.inteligencia
    sabiduria = sabiduria + raza.sabiduria
    carisma = carisma + raza.carisma
    return fuerza, destreza, constitucion, inteligencia, sabiduria, carisma

#Habria que meter todos los querysets aqui para que funcione y hacer solo 3 pasos. ¿Añadir el compañero animal una vez esté creado el personaje?
@login_required(login_url="/login/")
def crear_personaje_3(request):
    try:
        if request.method == 'POST':
            raza = Raza.objects.get(raza=request.POST.get('raza'))
            clase = Clase.objects.get(nivel=1, clase=request.POST.get('clase'))
            clase_nivel_0 = Clase.objects.get(clase=request.POST.get('clase'), nivel=0)
            inteligencia = request.POST.get('inteligencia')
            formulario_paso_3 = PersonajeForm3(request.POST, raza=raza, clase=clase, inteligencia=inteligencia)
            alineamiento = request.POST.get('alineamiento')
            fuerza = request.POST.get('fuerza')
            destreza = request.POST.get('destreza')
            constitucion = request.POST.get('constitucion')
            sabiduria = request.POST.get('sabiduria')
            carisma = request.POST.get('carisma')
            numero_habilidades_eleccion = request.POST.get('numero_habilidades_eleccion')
            numero_idiomas_eleccion = request.POST.get('numero_idiomas_eleccion')
            cantidad_conjuros_conocidos_0_eleccion = 0
            cantidad_conjuros_conocidos_1_eleccion = 0
            if clase.cantidad_conjuros_conocidos.all():
                cantidad_conjuros_conocidos_0_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=0).cantidad
                cantidad_conjuros_conocidos_1_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=1).cantidad
            if formulario_paso_3.is_valid():
                nombre = formulario_paso_3.cleaned_data.get('nombre')
                dotes = formulario_paso_3.cleaned_data.get('dotes')
                linaje = formulario_paso_3.cleaned_data.get('linaje')
                habilidades = formulario_paso_3.cleaned_data.get('habilidades')
                idiomas = formulario_paso_3.cleaned_data.get('idiomas')
                conjuros_conocidos_0 = formulario_paso_3.cleaned_data.get('conjuros_conocidos_0')
                conjuros_conocidos_1 = formulario_paso_3.cleaned_data.get('conjuros_conocidos_1')
                conjuros_conocidos = conjuros_conocidos_0 | conjuros_conocidos_1
                if not conjuros_conocidos and clase.conjuros:
                    conjuros_conocidos = clase.conjuros
                personaje = guardar_personaje(request, nombre, raza, clase, alineamiento, fuerza, destreza, constitucion, inteligencia, sabiduria, carisma, dotes, linaje, habilidades, idiomas, conjuros_conocidos)
                return redirect('/personaje/show/'+str(personaje.pk))
        return render(request, 'personaje/paso3.html', {'raza':raza, 'clase':clase, 'clase_nivel_0':clase_nivel_0, 'alineamiento':alineamiento, 'fuerza':fuerza, 'destreza':destreza, 'constitucion':constitucion, 'inteligencia':inteligencia, 'sabiduria':sabiduria, 'carisma':carisma, 'formulario_paso_3':formulario_paso_3, 'numero_habilidades_eleccion':numero_habilidades_eleccion, 'numero_idiomas_eleccion':numero_idiomas_eleccion, 'clase_nivel_0':clase_nivel_0, 'cantidad_conjuros_conocidos_0_eleccion':cantidad_conjuros_conocidos_0_eleccion, 'cantidad_conjuros_conocidos_1_eleccion':cantidad_conjuros_conocidos_1_eleccion})
    except:
        return redirect('error_url')

def guardar_personaje(request, nombre, raza, clase, alineamiento, fuerza, destreza, constitucion, inteligencia, sabiduria, carisma, dotes, linaje, habilidades, idiomas, conjuros_conocidos):
    perfil = usuario_logueado(request)
    clase_nivel_0 = Clase.objects.get(clase=clase, nivel=0)
    dados_de_golpe = clase_nivel_0.dados_de_golpe
    puntuaciones_habilidad = []
    for habilidad in habilidades:
        puntuacion_habilidad = PuntuacionHabilidad.objects.get(puntuacion=1, habilidad=habilidad)
        puntuaciones_habilidad.append(puntuacion_habilidad)
    personaje = Personaje.objects.create(perfil=perfil, nombre=nombre, raza=raza, alineamiento=alineamiento, 
    fuerza=fuerza, destreza=destreza, constitucion=constitucion, inteligencia=inteligencia, sabiduria=sabiduria, carisma=carisma,
    puntos_de_golpe=dados_de_golpe)
    if linaje != None:
        linaje_save = Linaje.objects.get(nombre=linaje)
        personaje.linaje = linaje_save
    for dote in dotes:
        personaje.dotes.add(dote)
    for idioma in raza.idiomas_iniciales.all():
        personaje.idiomas.add(idioma)
    if idiomas:
        for idioma in idiomas:
            personaje.idiomas.add(idioma)
    if conjuros_conocidos:
        for conjuro in conjuros_conocidos.all():
            personaje.conjuros_conocidos.add(conjuro)
    if puntuaciones_habilidad:
        for ph in puntuaciones_habilidad:
            personaje.puntuaciones_habilidad.add(ph)
    personaje.clase = clase
    personaje.save()
    return personaje

#Pensar si quitar los familiares (no vale la pena tenerlos para lo poco que hacen ya) (de momento están quitados)
@login_required(login_url="/login/")
def asignar_companero_animal(request, pk):
    try:
        perfil = usuario_logueado(request)
        personaje = Personaje.objects.get(pk=pk)
        assert perfil == personaje.perfil
        assert not personaje.companero_animal_personaje.all()
        druida_1 = Clase.objects.get(clase='Druida', nivel=1)
        #mago_1 = Clase.objects.get(clase='Mago', nivel=1) habria que incluir or (mago_1 in personaje.clases en el assert de debajo)
        explorador_4 = Clase.objects.get(clase='Explorador', nivel=4)
        assert (druida_1 == personaje.clase) or (explorador_4 == personaje.clase)
        companero_animal_nivel = CompaneroAnimal.objects.get(nivel=1, tipo=None)
        if request.method == 'POST':
            formulario = CompaneroAnimalForm(request.POST)
            if formulario.is_valid():
                nombre = formulario.cleaned_data.get('nombre')
                dotes = formulario.cleaned_data.get('dotes')
                trucos = formulario.cleaned_data.get('trucos')
                habilidades = formulario.cleaned_data.get('habilidades')
                companero_animal_tipo = formulario.cleaned_data.get('companero_animal_tipo')
                guardar_companero_animal(personaje, nombre, dotes, trucos, habilidades, companero_animal_tipo, companero_animal_nivel)
                return redirect('/personaje/show/'+str(personaje.pk))
        else:
            formulario = CompaneroAnimalForm()
        return render(request, 'personaje/companero_animal/asignar.html', {'formulario':formulario, 'personaje':personaje, 'companero_animal_nivel':companero_animal_nivel})
    except:
        return redirect('error_url')

def guardar_companero_animal(personaje, nombre, dotes, trucos, habilidades, companero_animal_tipo, companero_animal_nivel):
    nivel = companero_animal_nivel.nivel
    dados_de_golpe = companero_animal_nivel.dados_de_golpe
    puntos_de_golpe = companero_animal_nivel.puntos_de_golpe
    ataque_base = companero_animal_nivel.ataque_base
    fortaleza = companero_animal_nivel.fortaleza
    reflejos = companero_animal_nivel.reflejos
    voluntad = companero_animal_nivel.voluntad
    puntos_habilidad = companero_animal_nivel.puntos_habilidad
    numero_dotes = companero_animal_nivel.numero_dotes
    numero_trucos = companero_animal_nivel.numero_trucos
    tipo = companero_animal_tipo.tipo
    tamano = companero_animal_tipo.tamano
    velocidad = companero_animal_tipo.velocidad
    ataque = companero_animal_tipo.ataque
    constitucion = companero_animal_tipo.constitucion
    inteligencia = companero_animal_tipo.inteligencia
    sabiduria = companero_animal_tipo.sabiduria
    carisma = companero_animal_tipo.carisma
    nivel_cambio = companero_animal_tipo.nivel_cambio
    companero_animal_cambio = companero_animal_tipo.companero_animal_cambio
    especiales = companero_animal_tipo.especiales
    ca = companero_animal_tipo.ca + companero_animal_nivel.ca
    fuerza = companero_animal_tipo.fuerza + companero_animal_nivel.fuerza
    destreza = companero_animal_tipo.destreza + companero_animal_nivel.destreza

    companero_animal_personaje = CompaneroAnimalPersonaje.objects.create(tipo=tipo, nivel=nivel, dados_de_golpe=dados_de_golpe, 
    puntos_de_golpe=puntos_de_golpe, tamano=tamano, velocidad=velocidad, ca=ca, ataque_base=ataque_base, ataque=ataque, 
    fuerza=fuerza, destreza=destreza, constitucion=constitucion, inteligencia=inteligencia, sabiduria=sabiduria, carisma=carisma, 
    fortaleza=fortaleza, reflejos=reflejos, voluntad=voluntad, numero_dotes=numero_dotes, puntos_habilidad=puntos_habilidad, 
    numero_trucos=numero_trucos, nivel_cambio=nivel_cambio, companero_animal_cambio=companero_animal_cambio, nombre=nombre)
    for especial in especiales.all():
        companero_animal_personaje.especiales.add(especial)
    companero_animal_personaje.dotes.add(dotes)
    for truco in trucos:
        companero_animal_personaje.trucos.add(truco)
    puntuaciones_habilidad = []
    for habilidad in habilidades:
        puntuacion_habilidad = PuntuacionHabilidad.objects.get(puntuacion=1, habilidad=habilidad)
        puntuaciones_habilidad.append(puntuacion_habilidad)
    if puntuaciones_habilidad:
        for ph in puntuaciones_habilidad:
            companero_animal_personaje.puntuacion_habilidad.add(ph)
    companero_animal_personaje.personaje = personaje
    companero_animal_personaje.save()

@login_required(login_url="/login/")
def eliminar_personaje(request, pk):
    try:
        personaje = Personaje.objects.get(pk=pk)
        perfil = usuario_logueado(request)
        assert personaje.perfil == perfil
        personaje.delete()
        return redirect('listar_personajes_propios_url')
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def subir_nivel(request, pk):
    try:
        personaje = Personaje.objects.get(pk=pk)
        perfil = usuario_logueado(request)
        assert personaje.perfil == perfil
        assert personaje.nivel < 20 and personaje.nivel >= 1
        clase = Clase.objects.get(clase=personaje.clase.clase, nivel=personaje.nivel+1)
        druida_1 = Clase.objects.get(clase='Druida', nivel=1)
        explorador_4 = Clase.objects.get(clase='Explorador', nivel=4)
        if druida_1 == personaje.clase or explorador_4 == personaje.clase:
            assert personaje.companero_animal_personaje.all()
        caracteristica_personaje_eleccion = False
        if clase.nivel%4 == 0:
            caracteristica_personaje_eleccion = True
        numero_eleccion_dotes = 0
        if clase.nivel%2 == 1:
            numero_eleccion_dotes = numero_eleccion_dotes + 1
        especiales_clase_dotes = Especial.objects.all().filter(clase=clase).filter(nombre__icontains='Dotes adicionales')
        if especiales_clase_dotes:
            numero_eleccion_dotes = numero_eleccion_dotes + 1
        clase_nivel_0 = Clase.objects.get(clase=clase.clase, nivel=0)
        numero_eleccion_habilidades = clase_nivel_0.puntos_de_habilidad_por_nivel + math.floor((personaje.inteligencia-10)/2)
        if numero_eleccion_habilidades <= 0:
            numero_eleccion_habilidades = 1
        numero_poderes = 0
        especiales_clase_poderes = clase.especiales.all()
        especiales_nombre = ['Poder de furia', 'Enemigo predilecto', 'Entrenamiento en armas', 'Merced', 'Talentos del pícaro']
        for especial in especiales_clase_poderes:
            if especial.nombre in especiales_nombre:
                numero_poderes = numero_poderes + 1
        companero_animal_personaje = personaje.companero_animal_personaje
        caracteristica_companero_animal_eleccion = False
        cap = None
        companero_animal_nivel = None
        if companero_animal_personaje.all():
            for ca in companero_animal_personaje.all():
                cap = ca
            companero_animal_nivel = CompaneroAnimal.objects.get(nivel=ca.nivel+1, tipo=None)
            if companero_animal_nivel.nivel%4 == 0:
                caracteristica_companero_animal_eleccion = True
        cantidad_conjuros_conocidos_0_eleccion = 0
        cantidad_conjuros_conocidos_1_eleccion = 0
        cantidad_conjuros_conocidos_2_eleccion = 0
        cantidad_conjuros_conocidos_3_eleccion = 0
        cantidad_conjuros_conocidos_4_eleccion = 0
        cantidad_conjuros_conocidos_5_eleccion = 0
        cantidad_conjuros_conocidos_6_eleccion = 0
        cantidad_conjuros_conocidos_7_eleccion = 0
        cantidad_conjuros_conocidos_8_eleccion = 0
        cantidad_conjuros_conocidos_9_eleccion = 0
        if clase.cantidad_conjuros_conocidos.all():
            cantidad_conjuros_conocidos_0_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=0).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=0).cantidad
            cantidad_conjuros_conocidos_1_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=1).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=1).cantidad
            if len(clase.cantidad_conjuros_conocidos.all()) == 3 and len(personaje.clase.cantidad_conjuros_conocidos.all()) == 2:
                cantidad_conjuros_conocidos_2_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=2).cantidad
            elif len(clase.cantidad_conjuros_conocidos.all()) > 3 or len(personaje.clase.cantidad_conjuros_conocidos.all()) == 3:
                cantidad_conjuros_conocidos_2_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=2).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=2).cantidad
            if len(clase.cantidad_conjuros_conocidos.all()) == 4 and len(personaje.clase.cantidad_conjuros_conocidos.all()) == 3:
                cantidad_conjuros_conocidos_3_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=3).cantidad
            elif len(clase.cantidad_conjuros_conocidos.all()) > 4 or len(personaje.clase.cantidad_conjuros_conocidos.all()) == 4:
                cantidad_conjuros_conocidos_3_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=3).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=3).cantidad
            if len(clase.cantidad_conjuros_conocidos.all()) == 5 and len(personaje.clase.cantidad_conjuros_conocidos.all()) == 4:
                cantidad_conjuros_conocidos_4_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=4).cantidad
            elif len(clase.cantidad_conjuros_conocidos.all()) > 5 or len(personaje.clase.cantidad_conjuros_conocidos.all()) == 5:
                cantidad_conjuros_conocidos_4_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=4).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=4).cantidad
            if len(clase.cantidad_conjuros_conocidos.all()) == 6 and len(personaje.clase.cantidad_conjuros_conocidos.all()) == 5:
                cantidad_conjuros_conocidos_5_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=5).cantidad
            elif len(clase.cantidad_conjuros_conocidos.all()) > 6 or len(personaje.clase.cantidad_conjuros_conocidos.all()) == 6:
                cantidad_conjuros_conocidos_5_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=5).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=5).cantidad
            if len(clase.cantidad_conjuros_conocidos.all()) == 7 and len(personaje.clase.cantidad_conjuros_conocidos.all()) == 6:
                cantidad_conjuros_conocidos_6_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=6).cantidad
            elif len(clase.cantidad_conjuros_conocidos.all()) > 7 or len(personaje.clase.cantidad_conjuros_conocidos.all()) == 7:
                cantidad_conjuros_conocidos_6_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=6).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=6).cantidad
            if len(clase.cantidad_conjuros_conocidos.all()) == 8 and len(personaje.clase.cantidad_conjuros_conocidos.all()) == 7:
                cantidad_conjuros_conocidos_7_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=7).cantidad
            elif len(clase.cantidad_conjuros_conocidos.all()) > 8 or len(personaje.clase.cantidad_conjuros_conocidos.all()) == 8:
                cantidad_conjuros_conocidos_7_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=7).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=7).cantidad
            if len(clase.cantidad_conjuros_conocidos.all()) == 9 and len(personaje.clase.cantidad_conjuros_conocidos.all()) == 8:
                cantidad_conjuros_conocidos_8_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=8).cantidad
            elif len(clase.cantidad_conjuros_conocidos.all()) > 9 or len(personaje.clase.cantidad_conjuros_conocidos.all()) == 9:
                cantidad_conjuros_conocidos_8_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=8).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=8).cantidad
            if len(clase.cantidad_conjuros_conocidos.all()) == 10 and len(personaje.clase.cantidad_conjuros_conocidos.all()) == 9:
                cantidad_conjuros_conocidos_9_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=9).cantidad
            elif len(personaje.clase.cantidad_conjuros_conocidos.all()) == 10:
                cantidad_conjuros_conocidos_9_eleccion = clase.cantidad_conjuros_conocidos.get(nivel=9).cantidad - personaje.clase.cantidad_conjuros_conocidos.get(nivel=9).cantidad
        if request.method == 'POST':
            formulario = SubirNivelForm(request.POST, personaje=personaje, clase=clase, numero_eleccion_dotes=numero_eleccion_dotes, 
            numero_eleccion_habilidades=numero_eleccion_habilidades, numero_poderes=numero_poderes, 
            companero_animal_nivel=companero_animal_nivel, cantidad_conjuros_conocidos_0_eleccion=cantidad_conjuros_conocidos_0_eleccion, 
            cantidad_conjuros_conocidos_1_eleccion=cantidad_conjuros_conocidos_1_eleccion, 
            cantidad_conjuros_conocidos_2_eleccion=cantidad_conjuros_conocidos_2_eleccion, 
            cantidad_conjuros_conocidos_3_eleccion=cantidad_conjuros_conocidos_3_eleccion, 
            cantidad_conjuros_conocidos_4_eleccion=cantidad_conjuros_conocidos_4_eleccion,
            cantidad_conjuros_conocidos_5_eleccion=cantidad_conjuros_conocidos_5_eleccion,
            cantidad_conjuros_conocidos_6_eleccion=cantidad_conjuros_conocidos_6_eleccion,
            cantidad_conjuros_conocidos_7_eleccion=cantidad_conjuros_conocidos_7_eleccion,
            cantidad_conjuros_conocidos_8_eleccion=cantidad_conjuros_conocidos_8_eleccion,
            cantidad_conjuros_conocidos_9_eleccion=cantidad_conjuros_conocidos_9_eleccion)
            if formulario.is_valid():
                dotes_personaje = formulario.cleaned_data.get('dotes_personaje')
                poderes = formulario.cleaned_data.get('poderes')
                habilidades_personaje = formulario.cleaned_data.get('habilidades_personaje')
                eleccion_puntos_de_golpe = formulario.cleaned_data.get('eleccion_puntos_de_golpe')
                eleccion_caracteristica_personaje = formulario.cleaned_data.get('eleccion_caracteristica_personaje')
                trucos = formulario.cleaned_data.get('trucos')
                habilidades_companero_animal = formulario.cleaned_data.get('habilidades_companero_animal')
                dotes_companero_animal = formulario.cleaned_data.get('dotes_companero_animal')
                eleccion_caracteristica_companero_animal = formulario.cleaned_data.get('eleccion_caracteristica_companero_animal')
                conjuros_conocidos_0 = formulario.cleaned_data.get('conjuros_conocidos_0')
                conjuros_conocidos_1 = formulario.cleaned_data.get('conjuros_conocidos_1')
                conjuros_conocidos_2 = formulario.cleaned_data.get('conjuros_conocidos_2')
                conjuros_conocidos_3 = formulario.cleaned_data.get('conjuros_conocidos_3')
                conjuros_conocidos_4 = formulario.cleaned_data.get('conjuros_conocidos_4')
                conjuros_conocidos_5 = formulario.cleaned_data.get('conjuros_conocidos_5')
                conjuros_conocidos_6 = formulario.cleaned_data.get('conjuros_conocidos_6')
                conjuros_conocidos_7 = formulario.cleaned_data.get('conjuros_conocidos_7')
                conjuros_conocidos_8 = formulario.cleaned_data.get('conjuros_conocidos_8')
                conjuros_conocidos_9 = formulario.cleaned_data.get('conjuros_conocidos_9')
                conjuros_conocidos = personaje.conjuros_conocidos.all() | conjuros_conocidos_0 | conjuros_conocidos_1 | conjuros_conocidos_2 | conjuros_conocidos_3 | conjuros_conocidos_4 | conjuros_conocidos_5 | conjuros_conocidos_6 | conjuros_conocidos_7 | conjuros_conocidos_8 | conjuros_conocidos_9
                if not clase.cantidad_conjuros_conocidos.all():
                    conjuros_conocidos = clase.conjuros
                guardar_subir_nivel_personaje(personaje, dotes_personaje, clase, poderes, habilidades_personaje, eleccion_puntos_de_golpe, eleccion_caracteristica_personaje, conjuros_conocidos)
                if cap != None:
                    guardar_subir_nivel_companero_animal(cap, companero_animal_nivel, trucos, habilidades_companero_animal, dotes_companero_animal, eleccion_caracteristica_companero_animal)
                return redirect('/personaje/show/'+str(personaje.pk))
        else:
            formulario = SubirNivelForm(personaje=personaje, clase=clase, numero_eleccion_dotes=numero_eleccion_dotes, 
            numero_eleccion_habilidades=numero_eleccion_habilidades, numero_poderes=numero_poderes, 
            companero_animal_nivel=companero_animal_nivel, cantidad_conjuros_conocidos_0_eleccion=cantidad_conjuros_conocidos_0_eleccion, 
            cantidad_conjuros_conocidos_1_eleccion=cantidad_conjuros_conocidos_1_eleccion, 
            cantidad_conjuros_conocidos_2_eleccion=cantidad_conjuros_conocidos_2_eleccion, 
            cantidad_conjuros_conocidos_3_eleccion=cantidad_conjuros_conocidos_3_eleccion, 
            cantidad_conjuros_conocidos_4_eleccion=cantidad_conjuros_conocidos_4_eleccion,
            cantidad_conjuros_conocidos_5_eleccion=cantidad_conjuros_conocidos_5_eleccion,
            cantidad_conjuros_conocidos_6_eleccion=cantidad_conjuros_conocidos_6_eleccion,
            cantidad_conjuros_conocidos_7_eleccion=cantidad_conjuros_conocidos_7_eleccion,
            cantidad_conjuros_conocidos_8_eleccion=cantidad_conjuros_conocidos_8_eleccion,
            cantidad_conjuros_conocidos_9_eleccion=cantidad_conjuros_conocidos_9_eleccion)
        return render(request, 'personaje/subir_nivel.html', {'formulario':formulario, 'pk':personaje.pk, 'clase_nivel_0':clase_nivel_0, 'caracteristica_personaje_eleccion':caracteristica_personaje_eleccion, 'caracteristica_companero_animal_eleccion':caracteristica_companero_animal_eleccion, 'companero_animal_personaje':companero_animal_personaje})
    except:
        return redirect('error_url')

#Mirar bien como se meten las habilidades en el personaje
def guardar_subir_nivel_personaje(personaje, dotes_personaje, clase, poderes, habilidades_personaje, eleccion_puntos_de_golpe, eleccion_caracteristica_personaje, conjuros_conocidos):
    clase_nivel_0 = Clase.objects.get(clase=clase, nivel=0)
    assert clase.nivel - personaje.nivel == 1
    if eleccion_caracteristica_personaje:
        if eleccion_caracteristica_personaje == 'Fuerza':
            personaje.fuerza = personaje.fuerza + 1
        elif eleccion_caracteristica_personaje == 'Destreza':
            personaje.destreza = personaje.destreza + 1
        elif eleccion_caracteristica_personaje == 'Constitucion':
            personaje.constitucion = personaje.constitucion + 1
        elif eleccion_caracteristica_personaje == 'Inteligencia':
            personaje.inteligencia = personaje.inteligencia + 1
        elif eleccion_caracteristica_personaje == 'Sabiduria':
            personaje.sabiduria = personaje.sabiduria + 1
        elif eleccion_caracteristica_personaje == 'Carisma':
           personaje.carisma = personaje.carisma + 1
    if eleccion_puntos_de_golpe == True:
        puntos_de_golpe = personaje.puntos_de_golpe + random.randrange(1, clase_nivel_0.dados_de_golpe)
    else:
        puntos_de_golpe = personaje.puntos_de_golpe + (clase_nivel_0.dados_de_golpe/2)
    puntos_de_golpe = puntos_de_golpe + personaje.bonificadorConstitucion
    personaje.puntos_de_golpe = puntos_de_golpe
    if dotes_personaje:
        for dote in dotes_personaje:
            personaje.dotes.add(dote)
    if poderes:
        personaje.poderes_conocidos.add(poderes)
    if conjuros_conocidos:
        for conjuro in conjuros_conocidos.all():
            personaje.conjuros_conocidos.add(conjuro)
    habilidades = []
    for ph in personaje.puntuaciones_habilidad.all():
        habilidades.append(ph.habilidad)
    for habilidad in habilidades_personaje:
        if habilidad in habilidades:
            ph = personaje.puntuaciones_habilidad.get(habilidad=habilidad)
            puntuacion_habilidad = PuntuacionHabilidad.objects.get(puntuacion=ph.puntuacion+1, habilidad=habilidad)
            personaje.puntuaciones_habilidad.remove(ph)
            personaje.puntuaciones_habilidad.add(puntuacion_habilidad)
        else:
            puntuacion_habilidad = PuntuacionHabilidad.objects.get(puntuacion=1, habilidad=habilidad)
            personaje.puntuaciones_habilidad.add(puntuacion_habilidad)
    personaje.clase = clase
    personaje.save()

def guardar_subir_nivel_companero_animal(companero_animal_personaje, companero_animal_nivel, trucos, habilidades_companero_animal, dotes_companero_animal, eleccion_caracteristica_companero_animal):
    if eleccion_caracteristica_companero_animal:
        if eleccion_caracteristica_companero_animal == 'Fuerza':
            companero_animal_personaje.fuerza = companero_animal_personaje.fuerza + 1
        elif eleccion_caracteristica_companero_animal == 'Destreza':
            companero_animal_personaje.companero_animal_personaje = personaje.destreza + 1
        elif eleccion_caracteristica_companero_animal == 'Constitucion':
            companero_animal_personaje.constitucion = companero_animal_personaje.constitucion + 1
        elif eleccion_caracteristica_companero_animal == 'Inteligencia':
            companero_animal_personaje.inteligencia = companero_animal_personaje.inteligencia + 1
        elif eleccion_caracteristica_companero_animal == 'Sabiduria':
            companero_animal_personaje.sabiduria = companero_animal_personaje.sabiduria + 1
        elif eleccion_caracteristica_companero_animal == 'Carisma':
           companero_animal_personaje.carisma = companero_animal_personaje.carisma + 1
    if trucos:
        for truco in trucos:
            companero_animal_personaje.trucos.add(truco)
    if dotes_companero_animal:
        for dote in dotes_companero_animal:
            companero_animal_personaje.dotes.add(dote)
    habilidades = []
    for ph in companero_animal_personaje.puntuacion_habilidad.all():
        habilidades.append(ph.habilidad)
    for habilidad in habilidades_companero_animal:
        if habilidad in habilidades:
            ph = companero_animal_personaje.puntuacion_habilidad.get(habilidad=habilidad)
            puntuacion_habilidad = PuntuacionHabilidad.objects.get(puntuacion=ph.puntuacion+1, habilidad=habilidad)
            companero_animal_personaje.puntuacion_habilidad.remove(ph)
            companero_animal_personaje.puntuacion_habilidad.add(puntuacion_habilidad)
        else:
            puntuacion_habilidad = PuntuacionHabilidad.objects.get(puntuacion=1, habilidad=habilidad)
            companero_animal_personaje.puntuacion_habilidad.add(puntuacion_habilidad)
    companero_animal_personaje.nivel = companero_animal_nivel.nivel
    companero_animal_personaje.dados_de_golpe = companero_animal_nivel.dados_de_golpe
    companero_animal_personaje.puntos_de_golpe = companero_animal_nivel.puntos_de_golpe
    companero_animal_personaje.ataque_base = companero_animal_nivel.ataque_base
    companero_animal_personaje.fortaleza = companero_animal_nivel.fortaleza
    companero_animal_personaje.reflejos = companero_animal_nivel.reflejos
    companero_animal_personaje.voluntad = companero_animal_nivel.voluntad
    companero_animal_personaje.puntos_habilidad = companero_animal_nivel.puntos_habilidad
    companero_animal_personaje.numero_dotes = companero_animal_nivel.numero_dotes
    companero_animal_personaje.numero_trucos = companero_animal_nivel.numero_trucos
    for especial in companero_animal_personaje.especiales.all():
        companero_animal_personaje.especiales.remove(especial)
    for especial in companero_animal_nivel.especiales.all():
        companero_animal_personaje.especiales.add(especial)
    companero_animal_nivel_menos = CompaneroAnimal.objects.get(nivel=companero_animal_nivel.nivel-1, tipo=None)
    companero_animal_personaje.ca = companero_animal_personaje.ca - companero_animal_nivel_menos.ca + companero_animal_nivel.ca
    companero_animal_personaje.fuerza = companero_animal_personaje.fuerza - companero_animal_nivel_menos.fuerza + companero_animal_nivel.fuerza
    companero_animal_personaje.destreza = companero_animal_personaje.destreza - companero_animal_nivel_menos.destreza + companero_animal_nivel.destreza
    if companero_animal_personaje.nivel == companero_animal_personaje.nivel_cambio:
        companero_animal_tipo_list = CompaneroAnimal.objects.all().filter(tipo__icontains=companero_animal_personaje.tipo).filter(nivel=None).exclude(nivel_cambio=None)
        for ca in companero_animal_tipo_list:
            companero_animal_tipo = ca
        companero_animal_tipo_cambio = ca.companero_animal_cambio
        companero_animal_personaje.tipo = companero_animal_tipo_cambio.tipo
        companero_animal_personaje.tamano = companero_animal_tipo_cambio.tamano
        companero_animal_personaje.velocidad = companero_animal_tipo_cambio.velocidad
        companero_animal_personaje.ataque = companero_animal_tipo_cambio.ataque
        companero_animal_personaje.ca = companero_animal_personaje.ca - companero_animal_tipo.ca + companero_animal_tipo_cambio.ca
        companero_animal_personaje.fuerza = companero_animal_personaje.fuerza - companero_animal_tipo.fuerza + companero_animal_tipo_cambio.fuerza
        companero_animal_personaje.destreza = companero_animal_personaje.destreza - companero_animal_tipo.destreza + companero_animal_tipo_cambio.destreza
        companero_animal_personaje.constitucion = companero_animal_personaje.constitucion - companero_animal_tipo.constitucion + companero_animal_tipo_cambio.constitucion
        companero_animal_personaje.inteligencia = companero_animal_personaje.inteligencia - companero_animal_tipo.inteligencia + companero_animal_tipo_cambio.inteligencia
        companero_animal_personaje.sabiduria = companero_animal_personaje.sabiduria - companero_animal_tipo.sabiduria + companero_animal_tipo_cambio.sabiduria
        companero_animal_personaje.carisma = companero_animal_personaje.carisma - companero_animal_tipo.carisma + companero_animal_tipo_cambio.carisma
        companero_animal_personaje.companero_animal_cambio = None
    companero_animal_personaje.save()

def gdpr(request):
    return render(request, 'gdpr.html')

def index(request):
    buscador = BuscarPersonajeForm(var=False)
    return render(request, 'index.html', {'buscador':buscador})

def home(request):
    return render(request, 'index.html')

def error(request):
    return render(request, 'paginaError.html')

# def jinja(request):
#     templateLoader = jinja2.FileSystemLoader(searchpath="./main/templates/")
#     templateEnv = jinja2.Environment(loader=templateLoader)
#     TEMPLATE_FILE = "hola_mundo.html"
#     template = templateEnv.get_template(TEMPLATE_FILE)
#     outputText = template.render(name='Miguel')
#     html_file = open('prueba.html', 'w')
#     html_file.write(outputText)
#     html_file.close()
#     return html_file

#Esto escribe un pdf y lo descarga pero no se como meter la vista que quiero descargar
# def export_pdf(request, pk):
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer)
#     p.drawString(100, 100, "Hello world.")
#     p.showPage()
#     p.save()
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename='hello.pdf')