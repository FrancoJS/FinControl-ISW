from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page ),
    path('cuenta/', views.cuenta_page ),
    path('crear-cuenta/', views.crear_cuenta )
]
