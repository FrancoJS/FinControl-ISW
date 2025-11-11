from gestion.models import Cuenta

def crear_cuenta(request):
    try:
        nombre = request.POST['nombre']
        saldo = request.POST['saldo']
        cuenta = Cuenta(nombre=nombre, saldo=saldo, usuario_id=1)
        cuenta.save()
        return {
            "success": True,
            "mensaje": "¡Cuenta creada correctamente!",
        }
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Ocurrió un error al crear la cuenta"
        }

def obtener_cuentas():
    try:
        cuentas = Cuenta.objects.filter(usuario_id=1).order_by('-id')
        return cuentas
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Ocurrio un error al obtener las cuentas"
        }
