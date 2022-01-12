from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Personaje
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
    try:
        razas = Raza.objects.all()
        return render(request, 'raza/list.html', {'razas':razas})
    except:
        return redirect('error_url')

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
        companeros_animales_por_tipo = CompaneroAnimal.objects.all().filter(es_familiar=False).exclude(tipo=None)
        familiares = CompaneroAnimal.objects.all().filter(es_familiar=True).exclude(tipo=None)
        return render(request, 'companero_animal/list.html', {'companero_animales_por_tipo':companeros_animales_por_tipo, 'familiares':familiares})
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
        clase = Clase.objects.get(id=pk)
        assert clase.nivel == 0
        poderes = clase.poderes
        return render(request, 'poder/list.html', {'poderes':poderes})
    except:
        return redirect('error_url')

def listar_especiales_por_clase(request, pk):
    try:
        clase = Clase.objects.get(id=pk)
        assert clase.nivel == 0
        especiales = clase.especiales
        return render(request, 'especial/list.html', {'especiales':especiales})
    except:
        return redirect('error_url')

def listar_conjuros_por_clase(request, pk):
    try:
        clase = Clase.objects.get(id=pk)
        assert clase.nivel == 0
        conjuros = clase.conjuros
        return render(request, 'conjuro/list.html', {'conjuros':conjuro})
    except:
        return redirect('error_url')

def mostrar_raza(request, pk):
    try:
        raza = Raza.objects.get(id=pk)
        return render(request, 'raza/show.html', {'raza':raza})
    except:
        return redirect('error_url')

def mostrar_dote(request, pk):
    try:
        dote = Dote.objects.get(id=pk)
        return render(request, 'dote/show.html', {'dote':dote})
    except:
        return redirect('error_url')

def mostrar_clase(request, pk):
    try:
        clase = Clase.objects.get(id=pk)
        assert clase.nivel == 0
        return render(request, 'clase/show.html', {'clase':clase})
    except:
        return redirect('error_url')

def mostrar_conjuro(request, pk):
    try:
        conjuro = Conjuro.objects.get(id=pk)
        return render(request, 'conjuro/show.html', {'conjuro':conjuro})
    except:
        return redirect('error_url')

def mostrar_poder(request, pk):
    try:
        poder = Poder.objects.get(id=pk)
        return render(request, 'poder/show.html', {'poder':poder})
    except:
        return redirect('error_url')

def mostrar_companero_animal(request, pk):
    try:
        companero_animal = CompaneroAnimal.objects.get(pk=id)
        assert companero_animal.tipo != None
        return render(request, 'companero_animal/show.html', {'companero_animal':companero_animal})
    except:
        return redirect('error_url')

def mostrar_truco(request, pk):
    try:
        truco = Truco.objects.get(pk=id)
        return render(request, 'truco/show.html', {'truco':truco})
    except:
        return redirect('error_url')

def mostrar_propiedad(request, pk):
    try:
        propiedad = Propiedad.objects.get(pk=id)
        return render(request, 'propiedad/show.html', {'propiedad':propiedad})
    except:
        return redirect('error_url')

def mostrar_linaje(request, pk):
    try:
        linaje = Linaje.objects.get(pk=id)
        return render(request, 'linaje/show.html', {'linaje':linaje})
    except:
        return redirect('error_url')

def mostrar_objeto(request, pk):
    try:
        if Arma.objects.get(id=pk):
            objeto = Arma.objects.get(id=pk)
        else:
            objeto = Armadura.objects.get(id=pk)
        return render(request, 'objeto/show.html', {'objeto':objeto})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def mostrar_personaje(request, pk):
    try:
        personaje = Personaje.objects.get(id=pk)
        if personaje.es_publico == False:
            perfil = usuario_logueado(request)
            assert personaje.perfil == perfil
        return render(request, 'personaje/show.html', {'personaje':personaje})
    except:
        return redirect('error_url')