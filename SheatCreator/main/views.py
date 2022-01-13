from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Personaje, Perfil, Raza
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
        companeros_animales_por_nivel = CompaneroAnimal.objects.all().filter(es_familiar=False).exclude(nivel=None)
        companeros_animales_por_tipo = CompaneroAnimal.objects.all().filter(es_familiar=False).exclude(tipo=None)
        familiares = CompaneroAnimal.objects.all().filter(es_familiar=True).exclude(tipo=None)
        especiales = companero_animal_por_nivel.especiales
        return render(request, 'companero_animal/list.html', {'companero_animal_por_nivel':companero_animal_por_nivel, 'companero_animales_por_tipo':companeros_animales_por_tipo, 'familiares':familiares, 'especiales':especiales})
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
        personajes = Personaje.objects().all().filter(perfil=perfil)
        return render(request, 'personaje/list.html', {'personajes':personajes})
    except:
        return redirect('error_url')

def listar_poderes_por_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        poderes = clase.poderes
        return render(request, 'poder/list.html', {'poderes':poderes})
    except:
        return redirect('error_url')

def listar_especiales_por_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        especiales = clase.especiales
        return render(request, 'especial/list.html', {'especiales':especiales})
    except:
        return redirect('error_url')

def listar_conjuros_por_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        conjuros = clase.conjuros
        return render(request, 'conjuro/list.html', {'conjuros':conjuro})
    except:
        return redirect('error_url')

def mostrar_raza(request, pk):
    try:
        raza = Raza.objects.get(pk=pk)
        bonificaciones_raza = raza.bonificaciones_raza
        return render(request, 'raza/show.html', {'raza':raza, 'bonificaciones_raza':bonificaciones_raza})
    except:
        return redirect('error_url')

def mostrar_dote(request, pk):
    try:
        dote = Dote.objects.get(pk=pk)
        prerrequisito_dote = dote.prerrequisito_dote
        return render(request, 'dote/show.html', {'dote':dote, 'prerrequisito_dote':prerrequisito_dote})
    except:
        return redirect('error_url')

def mostrar_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        clases_nivel = Clase.objects.all().filter(clase=clase.clase).exclude(nivel=0)
        especiales = clase.especiales
        habilidades = clase.habilidades
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
        especiales = companero_animal.especiales
        return render(request, 'companero_animal/show.html', {'companero_animal':companero_animal, 'especiales':especiales})
    except:
        return redirect('error_url')

def mostrar_companero_animal_personaje(request, pk):
    try:
        companero_animal = CompaneroAnimalPersonaje.objects.get(pk=pk)
        personaje = companero_animal.personaje
        if personaje.es_publico==True:
            perfil = usuario_logueado(request)
            assert perfil == personaje.perfil
        dotes = companero_animal-dotes
        trucos = companero_animal.trucos
        especiales = companero_animal.especiales
        puntuaciones_habilidad = companero_animal.puntuacion_habilidad
        for ph in puntuaciones_habilidad:
            diccionario_habilidad[ph.habilidad.habilidad] = ph.puntuacion
        return render(request, 'companero_animal/show.html', {'companero_animal':companero_animal, 'dotes':dotes, 'trucos':trucos, 'especiales':especiales, 'habilidades':diccionario_habilidad})
    except:
        return redirect('error_url')

def mostrar_truco(request, pk):
    try:
        truco = Truco.objects.get(pk=pk)
        prerrequisito_truco = truco.prerrequisito_truco
        return render(request, 'truco/show.html', {'truco':truco, 'prerrequisito_truco':prerrequisito_truco})
    except:
        return redirect('error_url')

def mostrar_propiedad(request, pk):
    try:
        propiedad = Propiedad.objects.get(pk=pk)
        return render(request, 'propiedad/show.html', {'propiedad':propiedad})
    except:
        return redirect('error_url')

def mostrar_linaje(request, pk):
    try:
        linaje = Linaje.objects.get(pk=pk)
        conjuros = linaje.conjuros
        dotes = linaje.dotes
        poderes = linaje.poderes
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
        if personaje.es_publico == False:
            perfil = usuario_logueado(request)
            assert personaje.perfil == perfil
        idiomas = personaje.idiomas
        clases = personaje.clases
        dotes = personaje.dotes
        conjuros = personaje.conjuros
        poderes = personaje.poderes
        inventario = personaje.propiedad_objeto
        puntuaciones_habilidad = personaje.puntuaciones_habilidad
        for ph in puntuaciones_habilidad:
           diccionario_habilidad[ph.habilidad.habilidad] = ph.puntuacion
        return render(request, 'personaje/show.html', {'personaje':personaje, 'habilidades':diccionario_habilidad, 'conjuros':conjuros, 'poderes':poderes, 'inventario':inventario})
    except:
        return redirect('login_url')

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'index.html')

def error(request):
    return render(request, 'paginaError.html')