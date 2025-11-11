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
    path('transacciones/', views.transacciones_page ),
    path('crear-transaccion/', views.crear_transaccion ),
    path('cerrar-sesion/', views.cerrar_sesion )
]
