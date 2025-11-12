from gestion.models import Cuenta

def crear_cuenta(nombre, saldo, usuario_id):
    try:
        cuenta = Cuenta(nombre=nombre, saldo=saldo, usuario_id=usuario_id)
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

def modificar_cuenta(id_cuenta, nombre, usuario_id):
    try:
        if not usuario_id:
            return {
                "success": False,
                "mensaje": "Sesión expirada o usuario no autenticado."
            }

        id_cuenta = int(id_cuenta)
        cuenta = Cuenta.objects.get(id=id_cuenta, usuario_id=usuario_id)
        cuenta.nombre = nombre
        cuenta.save()

        return {
            "success": True,
            "mensaje": "¡Cuenta modificada correctamente!",
        }

    except Cuenta.DoesNotExist:
        return {
            "success": False,
            "mensaje": "No se encontró una cuenta asociada a este usuario."
        }

    except Exception as e:
        print("Error al modificar cuenta:", e)
        return {
            "success": False,
            "mensaje": "Ocurrió un error al modificar la cuenta."
        }
