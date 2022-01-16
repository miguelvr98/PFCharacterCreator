from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import *
from main.forms import EditarUsernameForm

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
        return render(request, 'raza/list.html', {'razas':razas})

def listar_dotes(request):
    try:
        dotes = Dote.objects.all()
        return render(request, 'dote/list.html', {'dotes':dotes})
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
        return render(request, 'habilidad/list.html', {'habilidades':habilidades})
    except:
        return redirect('error_url')

def listar_companeros_animales(request):
    try:
        companeros_animales_por_nivel = CompaneroAnimal.objects.all().filter(es_familiar=False).exclude(nivel=None).exclude(nivel=0)
        companeros_animales_por_tipo = CompaneroAnimal.objects.all().filter(es_familiar=False).exclude(tipo=None)
        familiares = CompaneroAnimal.objects.all().filter(es_familiar=True).exclude(tipo=None)
        aux_ca = CompaneroAnimal.objects.get(nivel=0)
        especiales = aux_ca.especiales.all()
        return render(request, 'companero_animal/list.html', {'companeros_animales_por_nivel':companeros_animales_por_nivel, 'companeros_animales_por_tipo':companeros_animales_por_tipo, 'familiares':familiares, 'especiales':especiales})
    except:
        return redirect('error_url')

def listar_trucos(request):
    try:
        trucos = Truco.objects.all()
        return render(request, 'truco/list.html', {'trucos':trucos})
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

@login_required(login_url="/login/")
def listar_personajes_publicos(request):
    try:
        personajes = Personaje.objects.all().filter(es_publico=True)
        return render(request, 'personaje/list.html', {'personajes':personajes})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def listar_personajes_propios(request):
    try:
        perfil = usuario_logueado(request)
        personajes = Personaje.objects.all().filter(perfil=perfil)
        return render(request, 'personaje/list.html', {'personajes':personajes})
    except:
        redirect('error_url')

def listar_poderes_por_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        poderes = clase.poderes.all()
        return render(request, 'poder/list.html', {'poderes':poderes})
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

def listar_conjuros_por_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        conjuros = clase.conjuros.all()
        return render(request, 'conjuro/list.html', {'conjuros':conjuros})
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
    if dote.prerrequisito_dote.all() and dote.prerrequisito_raza != None:
        prerrequisito_dote = dote.prerrequisito_dote.all()
        prerrequisito_raza = dote.prerrequisito_raza
        return render(request, 'dote/show.html', {'dote':dote, 'prerrequisito_dote':prerrequisito_dote, 'prerrequisito_raza':prerrequisito_raza})
    elif dote.prerrequisito_dote.all() and dote.prerrequisito_raza == None:
        prerrequisito_dote = dote.prerrequisito_dote.all()
        return render(request, 'dote/show.html', {'dote':dote, 'prerrequisito_dote':prerrequisito_dote})
    prerrequisito_raza = dote.prerrequisito_raza
    return render(request, 'dote/show.html', {'dote':dote, 'prerrequisito_raza':prerrequisito_raza})

def mostrar_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        clases_nivel = Clase.objects.all().filter(clase=clase.clase).exclude(nivel=0)
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
    if personaje.es_publico==True:
        perfil = usuario_logueado(request)
        assert perfil == personaje.perfil
    companero_animal = personaje.companero_animal
    dotes = companero_animal.dotes.all()
    trucos = companero_animal.trucos.all()
    especiales = companero_animal.especiales.all()
    return render(request, 'companero_animal/show.html', {'companero_animal':companero_animal, 'dotes':dotes, 'trucos':trucos, 'especiales':especiales})

def mostrar_truco(request, pk):
    truco = Truco.objects.get(pk=pk)
    print(truco.prerrequisito_truco.all())
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

@login_required(login_url="/login/")
def mostrar_personaje(request, pk):
    try:
        personaje = Personaje.objects.get(pk=pk)
        if personaje.es_publico == False:
            perfil = usuario_logueado(request)
            assert personaje.perfil == perfil
        idiomas = personaje.idiomas.all()
        clases = personaje.clases.all()
        dotes = personaje.dotes.all()
        conjuros = personaje.conjuros_conocidos.all()
        poderes = personaje.poderes_conocidos.all()
        inventario = personaje.propiedades_objeto.all()
        return render(request, 'personaje/show.html', {'personaje':personaje, 'conjuros':conjuros, 'poderes':poderes, 'inventario':inventario})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def cambiar_personaje_a_publico(request, pk):
    try:
        perfil = usuario_logueado(request)
        personaje = Personaje.objects.get(pk=pk)
        assert personaje.perfil == perfil
        personaje.es_publico = True
        personaje.save()

        personajes = Personaje.objects.all().filter(perfil=perfil)
        return render(request, 'personaje/list.html', {'personajes':personajes})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def cambiar_personaje_a_privado(request, pk):
    try:
        perfil = usuario_logueado(request)
        personaje = Personaje.objects.get(pk=pk)
        assert personaje.perfil == perfil
        personaje.es_publico = False
        personaje.save()

        personajes = Personaje.objects.all().filter(perfil=perfil)
        return render(request, 'personaje/list.html', {'personajes':personajes})
    except:
        return redirect('error_url')


def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'index.html')

def error(request):
    return render(request, 'paginaError.html')