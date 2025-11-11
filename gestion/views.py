from django.shortcuts import render
from gestion.models import Usuario
from gestion.servicios import cuentas
from gestion.servicios import transacciones

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
            listar_cuentas = cuentas.obtener_cuentas()
            datos = {
                'email': email,
                'contraseña': contraseña,
                'cuentas': listar_cuentas
            }
            return render(request, 'cuenta/cuenta-page.html', datos)
        else:
            datos = {
                'r2': 'Credenciales incorrectas'
            }

    return render(request, 'Usuarios/iniciar_sesion.html',datos)


def landing_page(request):
    return render(request, 'landing-page/landing.html')

def cuenta_page(request):
    lista_cuentas = cuentas.obtener_cuentas()

    lista = {
        "cuentas": lista_cuentas
    }
    return render(request, 'cuenta/cuenta-page.html', lista)

def crear_cuenta(request):
    resultado = {}
    if request.method == 'POST':
        respuesta = cuentas.crear_cuenta(request)

        if respuesta["success"] == False:
            resultado["success"] = False
            resultado["mensaje"] = respuesta["mensaje"]
        else:
            resultado["success"] = True
            resultado["mensaje"] = respuesta["mensaje"]

        resultado["cuentas"] = cuentas.obtener_cuentas()

        return render(request, 'cuenta/cuenta-page.html', resultado)
    else:
        resultado["cuentas"] = cuentas.obtener_cuentas()
        return render(request, 'cuenta/cuenta-page.html', resultado)
def transacciones_page(request):
    # obtener id del usuario actual
    usuario_id = request.session.get('id_usuario')

    # obtener transacciones desde la capa de servicios
    lista_transacciones = transacciones.obtener_transacciones(usuario_id)

    # estructura del contexto
    datos = {
        "transacciones": lista_transacciones,
    }

    return render(request, 'transacciones/transacciones-page.html', datos)
