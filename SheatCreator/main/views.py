from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from main.models import *
from main.forms import *

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
        buscador = BuscarDoteForm()
        return render(request, 'dote/list.html', {'dotes':dotes, 'buscador':buscador})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def listar_dotes_propias(request):
    try:
        perfil = usuario_logueado(request)
        dotes = Dote.objects.all().filter(creador=perfil)
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
        buscador = BuscarPersonajeForm()
        return render(request, 'personaje/list.html', {'personajes':personajes, 'buscador':buscador})
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def listar_personajes_propios(request):
    try:
        perfil = usuario_logueado(request)
        personajes = Personaje.objects.all().filter(perfil=perfil)
        buscador = BuscarPersonajeForm()
        return render(request, 'personaje/list.html', {'personajes':personajes, 'buscador':buscador})
    except:
        redirect('error_url')

def listar_poderes_por_clase(request, pk):
    try:
        clase = Clase.objects.get(pk=pk)
        assert clase.nivel == 0
        poderes = clase.poderes.all()
        buscador = BuscarPoderForm()
        return render(request, 'poder/list.html', {'poderes':poderes, 'buscador':buscador, 'pk':pk})
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
        buscador = BuscarConjuroForm()
        return render(request, 'conjuro/list.html', {'conjuros':conjuros, 'buscador':buscador, 'pk':pk})
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
        assert personaje.es_publico == False
        personaje.es_publico = True
        personaje.save()

        personajes = Personaje.objects.all().filter(perfil=perfil)
        return redirect('listar_personajes_propios_url')
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
        return redirect('listar_personajes_propios_url')
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
    try:
        if request.method == 'POST':
            form_dote = DoteForm(request.POST)
            perfil = usuario_logueado(request)
            if form_dote.is_valid():
                dote = form_dote.save(commit=False)
                dote.creador = perfil
                dote.save()

                return redirect('/dote/show/'+ str(dote.pk))
        else:
            form_dote = DoteForm()
        return render(request, 'dote/edit.html', {'form_dote':form_dote})
    except:
        return redirect('error_url')

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
        dote.delete()
        return redirect('/dote/perfil/list')
    except:
        return redirect('error_url')

@login_required(login_url="/login/")
def mostrar_perfil_propio(request):
    try:
        perfil = usuario_logueado(request)
        personajes = Personaje.objects.all().filter(perfil=perfil)
        return render(request, 'perfil/show.html', {'perfil':perfil, 'personajes':personajes})
    except:
        return redirect('error_url')
    
@login_required(login_url="/login/")
def mostrar_perfil(request, pk):
    try:
        perfil = Perfil.objects.get(pk=pk)
        personajes = Personaje.objects.all().filter(perfil=perfil).filter(es_publico=True)
        return render(request, 'perfil/show.html', {'perfil':perfil, 'personajes':personajes})
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
        return redirect('/login')
    except:
        return redirect('error_url')

def buscar_dote(request):
    try:
        dotes = Dote.objects.all()
        if request.method == 'POST':
            buscador = BuscarDoteForm(request.POST)
            if buscador.is_valid():
                nombre = buscador.cleaned_data.get('nombre')
                tipo = buscador.cleaned_data.get('tipo')
                es_dote_companero_animal = buscador.cleaned_data.get('es_dote_companero_animal')

                if nombre != None and nombre != '':
                    dotes = dotes.filter(nombre__icontains=nombre)
                if tipo != '':
                    dotes = dotes.filter(tipo=tipo)
                if es_dote_companero_animal == True:
                    dotes = dotes.filter(es_dote_companero_animal=True)
        else:
            buscador = BuscarDoteForm()
        return render(request, 'dote/list.html', {'dotes':dotes, 'buscador':buscador})
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
        else:
            buscador = BuscarPoderForm()
        return render(request, 'poder/list.html', {'poderes':poderes, 'buscador':buscador, 'pk':pk})
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
        else:
            buscador = BuscarConjuroForm()
        return render(request, 'conjuro/list.html', {'conjuros':conjuros, 'buscador':buscador, 'pk':pk})
    except:
        return redirect('error_url')

def buscar_personaje(request):
    try:
        personajes = Personaje.objects.all()
        if request.user.is_authenticated:
            perfil = usuario_logueado(request)
            personajes_aux = personajes.filter(perfil=perfil)
        else:
            personajes = personajes.filter().exclude(es_publico=False)
        if request.method == 'POST':
            buscador = BuscarPersonajeForm(request.POST)
            if buscador.is_valid():
                nombre = buscador.cleaned_data.get('nombre')
                clase = buscador.cleaned_data.get('clase')
                personajes = personajes | personajes_aux

                if nombre != None and nombre != '':
                    personajes = personajes.filter(nombre__icontains=nombre)
                
                if clase != None:
                    clases = Clase.objects.all().filter(clase=clase.clase)
                    personajes = personajes.filter(clases__in=clases)
        else:
            buscador = BuscarPersonajeForm()
        return render(request, 'personaje/list.html', {'personajes':personajes, 'buscador':buscador})
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
                nombre = formulario.cleaned_data.get('nombre')
                raza = formulario.cleaned_data.get('raza')
                clase = formulario.cleaned_data.get('clase')
                tipo = formulario.cleaned_data.get('tipo')
                alineamiento = formulario.cleaned_data.get('alineamiento')
                if tipo == 'Alta fantasía':
                    puntos_a_elegir = 20
                elif tipo == 'Épica':
                    puntos_a_elegir = 25
                formulario_paso_2 = PersonajeForm2(raza=raza)
                return render(request, 'personaje/paso2.html', {'nombre':nombre, 'raza':raza, 'clase':clase, 'alineamiento':alineamiento, 'formulario_paso_2':formulario_paso_2, 'puntos_a_elegir':puntos_a_elegir})
        else:
            formulario = PersonajeForm()
        return render(request, 'personaje/paso1.html', {'formulario':formulario})
    except:
        return redirect('error_url')

#Elección de puntos de características
def crear_personaje_2(request):
    try:
        if request.method == 'POST':
            raza = Raza.objects.get(raza=request.POST.get('raza'))
            formulario_paso_2 = PersonajeForm2(request.POST, raza=raza)
            nombre = request.POST.get('nombre')
            clase = Clase.objects.get(clase=request.POST.get('clase'), nivel=1)
            puntos_a_elegir = request.POST.get('puntos_a_elegir')
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
                formulario_paso_3 = PersonajeForm3(raza=raza, clase=clase)
                return render(request, 'personaje/paso3.html', {'nombre':nombre, 'raza':raza, 'clase':clase, 'alineamiento':alineamiento, 'fuerza':fuerza, 'destreza':destreza, 'constitucion':constitucion, 'inteligencia':inteligencia, 'sabiduria':sabiduria, 'carisma':carisma, 'formulario_paso_3':formulario_paso_3})
        return render(request, 'personaje/paso2.html', {'nombre':nombre, 'raza':raza, 'clase':clase, 'formulario_paso_2':formulario_paso_2, 'puntos_a_elegir':puntos_a_elegir, 'alineamiento':alineamiento})
    except:
        return redirect('error_url')

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

#Elección de dotes y linaje hay que reenviar al paso 4 (elección de habilidades o elección de compañero animal)
def crear_personaje_3(request):
    try:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            raza = Raza.objects.get(raza=request.POST.get('raza'))
            clase = Clase.objects.get(nivel=1, clase=request.POST.get('clase'))
            formulario_paso_3 = PersonajeForm3(request.POST, raza=raza, clase=clase)
            alineamiento = request.POST.get('alineamiento')
            fuerza = request.POST.get('fuerza')
            destreza = request.POST.get('destreza')
            constitucion = request.POST.get('constitucion')
            inteligencia = request.POST.get('inteligencia')
            sabiduria = request.POST.get('sabiduria')
            carisma = request.POST.get('carisma')
            if formulario_paso_3.is_valid():
                dotes = formulario_paso_3.cleaned_data.get('dotes')
                linaje = formulario_paso_3.cleaned_data.get('linaje')
                formulario_paso_4 = PersonajeForm4()
                return render(request, 'personaje/paso4.html', {'nombre':nombre, 'raza':raza, 'clase':clase, 'alineamiento':alineamiento, 'fuerza':fuerza, 'destreza':destreza, 'constitucion':constitucion, 'inteligencia':inteligencia, 'sabiduria':sabiduria, 'carisma':carisma, 'dotes':dotes, 'linaje':linaje, 'formulario_paso_4':formulario_paso_4})
        return render(request, 'personaje/paso3.html', {'nombre':nombre, 'raza':raza, 'clase':clase, 'alineamiento':alineamiento, 'fuerza':fuerza, 'destreza':destreza, 'constitucion':constitucion, 'inteligencia':inteligencia, 'sabiduria':sabiduria, 'carisma':carisma, 'formulario_paso_3':formulario_paso_3})
    except:
        return redirect('error_url')

        
def gdpr(request):
    return render(request, 'gdpr.html')

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'index.html')

def error(request):
    return render(request, 'paginaError.html')