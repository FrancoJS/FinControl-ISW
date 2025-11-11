from django.shortcuts import render
from gestion.models import Usuario

def landing(request):
    return render(request, 'LandingPage/landing.html')
def registro(request):
    datos = {}
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        contraseña = request.POST['password']

        if len(contraseña) < 8:
            datos = {
                'r2': 'La contraseña debe tener al menos 8 caracteres.'
            }
        else:
            nuevo = Usuario(nombre=nombre, apellido=apellido, email=email, contraseña=contraseña)
            nuevo.save()
            datos = {
                'nombre': nombre,
                'apellido': apellido,
                'email': email,
                'contraseña': contraseña,
                'r': 'Registrado correctamente!'
            }
    return render(request, 'Usuarios/registro.html', datos)

def iniciar_sesion(request):
    datos = {}
    if request.method == 'POST':
        email = request.POST['email'].strip()
        contraseña = request.POST['password'].strip()
        usuario = Usuario.objects.filter(email=email, contraseña=contraseña).first()
        if usuario:
            request.session['id_usuario'] = usuario.id
            request.session['nombre_usuario'] = usuario.nombre
            datos = {
                'email': email,
                'contraseña': contraseña,
            }
            return render(request, 'Dashboard/dashboard.html', datos)
        else:
            datos = {
                'r2': 'Credenciales incorrectas'
            }
            
    return render(request, 'Usuarios/iniciar_sesion.html',datos)
def dashboard(request):
    pass