from django.shortcuts import render
from gestion.models import Usuario
from gestion.servicios import metas
from gestion.models import MetaAhorro
from gestion.models import Cuenta
from gestion.servicios import transacciones
from gestion.servicios import cuentas

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


def eliminar_cuenta(request):
    resultado = {}
    usuario_id = request.session.get('usuario_id')

    if request.method == 'POST':
        id_cuenta = request.POST.get('id')

        if not id_cuenta:
            resultado['success'] = False
            resultado['mensaje'] = 'No se ha recibido el ID de la cuenta'
        else:
            respuesta = cuentas.eliminar_cuenta(id_cuenta, usuario_id)
            resultado["success"] = respuesta["success"]
            resultado["mensaje"] = respuesta["mensaje"]

        resultado["cuentas"] = cuentas.obtener_cuentas(usuario_id)
        return render(request, 'cuenta/cuenta-page.html', resultado)

    resultado["cuentas"] = cuentas.obtener_cuentas(usuario_id)
    return render(request, 'cuenta/cuenta-page.html', resultado)


def transacciones_page(request):

    usuario_id = request.session.get('usuario_id')
    lista_cuentas = cuentas.obtener_cuentas(usuario_id)
    lista_metas = metas.obtener_metas(usuario_id)
    resultado = {
        "cuentas": lista_cuentas,
        "transacciones": transacciones.obtener_transacciones(usuario_id),
        "metas": lista_metas
    }
    return render(request, 'transacciones/transacciones-page.html', resultado)

def crear_transaccion(request):
    usuario_id = request.session.get('usuario_id')
    if request.method == 'POST' and request.session.get('estado_sesion') == True:
        cuenta_origen = request.POST.get('cuenta_origen')
        cuenta_destino = request.POST.get('cuenta_destino') or None
        meta_ahorro = request.POST.get('meta_ahorro') or None
        monto = request.POST.get('monto')
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo')

        transaccion = {
            'cuenta_origen': cuenta_origen,
            'cuenta_destino': cuenta_destino,
            'monto': monto,
            'descripcion': descripcion,
            'tipo': tipo,
            'usuario': usuario_id,
            'meta_ahorro': meta_ahorro
        }

        resultado = transacciones.crear_transaccion(transaccion)
        lista_metas = metas.obtener_metas(usuario_id)
        lista_cuentas = cuentas.obtener_cuentas(usuario_id)
        lista_transacciones = transacciones.obtener_transacciones(usuario_id)

        resultado["transacciones"] = lista_transacciones
        resultado["cuentas"] = lista_cuentas
        resultado["metas"] = lista_metas


        return render(request, 'transacciones/transacciones-page.html', resultado)



def metas_page(request):
    usuario_id = request.session.get('usuario_id')
    datos = {}

    if not usuario_id:
        datos['r2'] = 'Debe iniciar sesión para acceder a las metas.'
        return render(request, 'Usuarios/iniciar_sesion.html', datos)

    lista_metas = metas.obtener_metas(usuario_id)
    lista_cuentas = cuentas.obtener_cuentas(usuario_id)

    datos = {
        "metas": lista_metas,
        "cuentas": lista_cuentas,
    }
    return render(request, 'metas/metas-page.html', datos)

def crear_meta(request):
    resultado = {}
    if request.method == 'POST':
        respuesta = metas.crear_meta(request)  # Aquí se pasa el request completo, no el id
        if respuesta["success"] == False:
            resultado["success"] = False
            resultado["mensaje"] = respuesta["mensaje"]
        else:
            resultado["success"] = True
            resultado["mensaje"] = respuesta["mensaje"]

        usuario_id = request.session.get('usuario_id')
        resultado["metas"] = metas.obtener_metas(usuario_id)
        resultado["cuentas"] = cuentas.obtener_cuentas(usuario_id)

        return render(request, 'metas/metas-page.html', resultado)
    else:
        usuario_id = request.session.get('usuario_id')
        resultado["metas"] = metas.obtener_metas(usuario_id)
        resultado["cuentas"] = cuentas.obtener_cuentas(usuario_id)
        return render(request, 'metas/metas-page.html', resultado)


def editar_meta(request):
    try:
        meta_id = request.POST.get("meta_id")
        nombre = request.POST.get("nombre")
        monto_objetivo = float(request.POST.get("monto_objetivo", 0))
        monto_actual = float(request.POST.get("monto_actual", 0))
        fecha_limite = request.POST.get("fecha_limite")
        usuario_id = request.session.get('usuario_id')

        if not meta_id:
            resultado = {"success": False, "mensaje": "ID de meta no especificado."}
            return render(request, 'metas/metas-page.html', resultado)

        meta = MetaAhorro.objects.get(id=meta_id)

        meta.nombre = nombre
        meta.monto_objetivo = monto_objetivo
        meta.monto_actual = monto_actual
        meta.fecha_limite = fecha_limite

        meta.save()
        lista_metas = metas.obtener_metas(usuario_id)

        resultado = {"success": True, "mensaje": "Meta actualizada correctamente.", "metas": lista_metas}
        return render(request, 'metas/metas-page.html', resultado)
    except MetaAhorro.DoesNotExist:
        resultado = {"success": False, "mensaje": "La meta no existe o no pertenece al usuario.",}
        return render(request, 'metas/metas-page.html', resultado)
    except Exception as e:
        print("Error al editar meta:", e)
        resultado = {"success": False, "mensaje": "Ocurrió un error al editar la meta."}
        return render(request, 'metas/metas-page.html', resultado)

def eliminar_meta(request):
    meta_id = request.POST.get("id")
    print(meta_id)
    respuesta = metas.eliminar_meta(meta_id)
    usuario_id = request.session.get('usuario_id')
    lista_metas = metas.obtener_metas(usuario_id)
    lista_cuentas = cuentas.obtener_cuentas(usuario_id)

    datos = {
        "metas": lista_metas,
        "cuentas": lista_cuentas,
        "mensaje": respuesta["mensaje"],
        "success": respuesta["success"],
    }
    return render(request, 'metas/metas-page.html', datos)

