from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.landing),
    path('iniciar_sesion/',views.iniciar_sesion),
    path('registro/',views.registro)

]
