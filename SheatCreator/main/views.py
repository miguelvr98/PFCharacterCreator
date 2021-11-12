from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Personaje
from main.forms import EditarUsernameForm

# Create your views here.
def usuario_logueado(request):

    try:
        id_user = request.user.id
        user_actual = get_object_or_404(User, pk=id_user)
        usuario_actual = usuario_actual = Perfil.objects.get(usuario=user_actual)
        return usuario_actual
        
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

@login_required(login_url='/login/')
def listar_personajes_usuario(request):

    try:
        usuario = usuario_logueado(request)
        personajes = Personaje.objects.all().filter(perfil = usuario)
        return render(request, 'personajes/list.html', {'personajes':personajes})

    except:
        return redirect('error_url')

