from django.shortcuts import render
from gestion.models import Usuario
from gestion.servicios import metas, cuentas
from gestion.models import Cuenta

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
            request.session['usuario_id'] = usuario.id
            request.session['nombre_usuario'] = usuario.nombre
            request.session['estado_sesion'] = True
            listar_cuentas = cuentas.obtener_cuentas(usuario.id)
            datos = {
                'email': email,
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
    usuario_id = request.session.get('usuario_id')
    lista_cuentas = cuentas.obtener_cuentas(usuario_id)

    lista = {
        "cuentas": lista_cuentas
    }
    return render(request, 'cuenta/cuenta-page.html', lista)

def crear_cuenta(request):
    resultado = {}
    usuario_id = request.session.get('usuario_id')
    if request.method == 'POST':
        nombre = request.POST['nombre']
        saldo = request.POST['saldo']
        respuesta = cuentas.crear_cuenta(nombre, saldo, usuario_id)

        if respuesta["success"] == False:
            resultado["success"] = False
            resultado["mensaje"] = respuesta["mensaje"]
        else:
            resultado["success"] = True
            resultado["mensaje"] = respuesta["mensaje"]

        resultado["cuentas"] = cuentas.obtener_cuentas(usuario_id)

        return render(request, 'cuenta/cuenta-page.html', resultado)
    else:
        resultado["cuentas"] = cuentas.obtener_cuentas(usuario_id=usuario_id)
        return render(request, 'cuenta/cuenta-page.html', resultado)

def transacciones_page(request):
    # obtener id del usuario actual
    usuario_id = request.session.get('id_usuario')



def metas_page(request):
    id_usuario = request.session.get('id_usuario')
    lista_metas = metas.obtener_metas(id_usuario)
    lista_cuentas = cuentas.obtener_cuentas(id_usuario)
    return render(request, 'metas/metas-page.html', {
        'metas': lista_metas,
        'cuentas': lista_cuentas
    })


def crear_meta(request):
    if request.method == 'POST':
        resultado = metas.crear_meta(request)
        usuario_id = request.session.get('id_usuario')
        lista_metas = metas.obtener_metas(usuario_id)
        cuentas_usuario = Cuenta.objects.filter(usuario_id=usuario_id)

        datos = {
            "metas": lista_metas,
            "cuentas": cuentas_usuario,
        }

        if resultado["success"]:
            datos["r"] = resultado["mensaje"]
        else:
            datos["r2"] = resultado["mensaje"]

        return render(request, 'metas/metas-page.html', datos)