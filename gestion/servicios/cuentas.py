from gestion.models import Cuenta

def crear_cuenta(nombre, saldo, usuario_id, tipo):
    try:
        cuenta = Cuenta(nombre=nombre, saldo=saldo, usuario_id=usuario_id, tipo=tipo)
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

def obtener_cuentas(usuario_id):
    try:
        cuentas = Cuenta.objects.filter(usuario_id=usuario_id).order_by('-id')
        return cuentas
    except Exception as e:
        return {
            "success": False,
            "mensaje": "Ocurrio un error al obtener las cuentas"
        }
