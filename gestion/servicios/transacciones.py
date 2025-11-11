from gestion.models import Transaccion

def obtener_transacciones(usuario_id):
    try:
        transacciones = (
            Transaccion.objects
            .filter(cuenta_origen__usuario_id=usuario_id)
            .order_by('-fecha')
        )
        return transacciones
    except Exception as e:
        print("Error al obtener transacciones:", e)
        return []
