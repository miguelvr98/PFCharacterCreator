"""SheatCreator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name="login_url"),
    path('logout/', LogoutView.as_view(), name="logout_url"),
    path('register/', views.registrar_usuario, name="registrar_usuario_url"),
    path('paginaError/', views.error, name="error_url"),
    path('gdpr/', views.gdpr, name="gdpr_url"),
    path('raza/list/', views.listar_razas, name='listar_razas_url'),
    path('dote/list/', views.listar_dotes, name='listar_dotes_url'),
    path('clase/list/', views.listar_clases, name='listar_clases_url'),
    path('conjuro/list/<int:pk>/', views.listar_conjuros_por_clase, name='listar_conjuros_por_clase_url'),
    path('habilidad/list/', views.listar_habilidades, name='listar_habilidades_url'),
    path('poder/list/<int:pk>/', views.listar_poderes_por_clase, name='listar_poderes_por_clase_url'),
    path('especial/list/<int:pk>/', views.listar_especiales_por_clase, name='listar_especiales_por_clase_url'),
    path('companero_animal/list/', views.listar_companeros_animales, name='listar_companeros_animales_url'),
    path('truco/list/', views.listar_trucos, name='listar_trucos_url'),
    path('propiedad/list/', views.listar_propiedades, name='listar_propiedades_url'),
    path('linaje/list/', views.listar_linajes, name='listar_linajes_url'),
    path('objeto/list/', views.listar_objetos, name='listar_objetos_url'),
    path('personaje/list/', views.listar_personajes_publicos, name='listar_personajes_publicos_url'),
    path('personaje/perfil/list/', views.listar_personajes_propios, name='listar_personajes_propios_url'),
    path('raza/show/<int:pk>/', views.mostrar_raza, name='mostrar_raza_url'),
    path('dote/show/<int:pk>/', views.mostrar_dote, name='mostrar_dote_url'),
    path('clase/show/<int:pk>/', views.mostrar_clase, name='mostrar_clase_url'),
    path('conjuro/show/<int:pk>/', views.mostrar_conjuro, name='mostrar_conjuro_url'),
    path('poder/show/<int:pk>/', views.mostrar_poder, name='mostrar_poder_url'),
    path('companero_animal/show/<int:pk>/', views.mostrar_companero_animal, name='mostrar_companero_animal_url'),
    path('truco/show/<int:pk>/', views.mostrar_truco, name='mostrar_truco_url'),
    path('propiedad/show/<int:pk>/', views.mostrar_propiedad, name='mostrar_propiedad_url'),
    path('linaje/show/<int:pk>/', views.mostrar_linaje, name='mostrar_linaje_url'),
    path('objeto/show/<int:pk>/', views.mostrar_objeto, name='mostrar_objeto_url'),
    path('personaje/show/<int:pk>/', views.mostrar_personaje, name='mostrar_personaje_url'),
    path('companero_animal_personaje/show/<int:pk>/', views.mostrar_companero_animal_personaje, name='mostrar_companero_animal_personaje_url'),
    path('personaje/publico/<int:pk>/', views.cambiar_personaje_a_publico, name='cambiar_personaje_a_publico_url'),
    path('personaje/privado/<int:pk>/', views.cambiar_personaje_a_privado, name='cambiar_personaje_a_privado_url'),
]