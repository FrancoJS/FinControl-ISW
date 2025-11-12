from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page ),
    path('iniciar_sesion/',views.iniciar_sesion),
    path('registro/',views.registro),
    path('cuenta/', views.cuenta_page ),
    path('crear-cuenta/', views.crear_cuenta ),
    path('metas/', views.metas_page),
    path('crear_meta/', views.crear_meta),
    path('editar_meta/', views.editar_meta),
    path('eliminar_meta/<int:meta_id>/', views.eliminar_meta),



]
