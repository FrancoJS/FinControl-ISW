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
            return render(request, 'Usuarios/registro.html', datos)
        else:
            usuario = Usuario(nombre=nombre, apellido=apellido, email=email, contraseña=contraseña)
            usuario.save()
            request.session['usuario_id'] = usuario.id
            request.session['nombre_usuario'] = usuario.nombre
            request.session['estado_sesion'] = True
            datos = {
                'nombre': nombre,
                'r': 'Registrado correctamente!'
            }
            return render(request, 'cuenta/cuenta-page.html', datos)

    return render(request, 'Usuarios/registro.html')

def iniciar_sesion(request):
    datos = {}
    if request.method == 'POST':
        email = request.POST['email'].strip()
        contraseña = request.POST['password'].strip()
        usuario = Usuario.objects.filter(email=email, contraseña=contraseña).first()
        if usuario:
            request.session['usuario_id'] = usuario.id
            request.session['nombre_usuario'] = usuario.nombre
            request.session['estado_sesion'] = True
            listar_cuentas = cuentas.obtener_cuentas(usuario.id)
            datos = {
                'email': email,
                'cuentas': listar_cuentas,
            }
            return render(request, 'cuenta/cuenta-page.html', datos)
        else:
            datos = {
                'r2': 'Credenciales incorrectas'
            }

    return render(request, 'Usuarios/iniciar_sesion.html',datos)


def cerrar_sesion(request):
    request.session.flush()
    return render(request, 'Usuarios/iniciar_sesion.html')

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
        tipo = request.POST['tipo']
        respuesta = cuentas.crear_cuenta(nombre, saldo, usuario_id, tipo)

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
    
def modificar_cuenta(request):
    resultado = {}
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        resultado["success"] = False
        resultado["mensaje"] = "Sesión expirada. Inicia sesión nuevamente."
        return render(request, 'Usuarios/iniciar_sesion.html', resultado)

    if request.method == 'POST':
        id_cuenta = request.POST.get('id')
        nombre = request.POST.get('nombre')

        # Validar entrada
        if not id_cuenta or not nombre:
            resultado["success"] = False
            resultado["mensaje"] = "Datos incompletos para modificar la cuenta."
        else:
            respuesta = cuentas.modificar_cuenta(id_cuenta, nombre, usuario_id)
            resultado["success"] = respuesta["success"]
            resultado["mensaje"] = respuesta["mensaje"]

        resultado["cuentas"] = cuentas.obtener_cuentas(usuario_id)
        return render(request, 'cuenta/cuenta-page.html', resultado)


    resultado["cuentas"] = cuentas.obtener_cuentas(usuario_id)
    return render(request, 'cuenta/cuenta-page.html', resultado)

def landing_page(request):
    return render(request, 'landing-page/landing.html')


def transacciones_page(request):
    usuario_id = request.session.get('usuario_id')
    lista_cuentas = cuentas.obtener_cuentas(usuario_id)
    print(lista_cuentas)
    resultado = {
        "cuentas": lista_cuentas,
        "transacciones": transacciones.obtener_transacciones(usuario_id)
    }
    return render(request, 'transacciones/transacciones-page.html', resultado)

def crear_transaccion(request):
    usuario_id = request.session.get('usuario_id')
    if request.method == 'POST' and request.session.get('estado_sesion') == True:
        cuenta_origen = request.POST.get('cuenta_origen')
        cuenta_destino = request.POST.get('cuenta_destino')
        print(cuenta_destino)
        print(cuenta_origen)
        monto = request.POST.get('monto')
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo')

        transaccion = {
            'cuenta_origen': cuenta_origen,
            'cuenta_destino': cuenta_destino,
            'monto': monto,
            'descripcion': descripcion,
            'tipo': tipo,
            'usuario': usuario_id
        }

        resultado = transacciones.crear_transaccion(transaccion)
        lista_cuentas = cuentas.obtener_cuentas(usuario_id)
        lista_transacciones = transacciones.obtener_transacciones(usuario_id)

        resultado["transacciones"] = lista_transacciones
        resultado["cuentas"] = lista_cuentas


        return render(request, 'transacciones/transacciones-page.html', resultado)


