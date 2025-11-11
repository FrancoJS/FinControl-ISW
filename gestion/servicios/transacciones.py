from gestion.models import Transaccion


def crear_transaccion(transaccion):
    try:
        transaccion = Transaccion(tipo=transaccion['tipo'], monto=transaccion['monto'], cuenta_origen_id=transaccion['cuenta_origen'], cuenta_destino_id=transaccion['cuenta_destino'], descripcion=transaccion['descripcion'], categoria='gasto general')
        transaccion.save()
        return {
            'success': True,
            'message': 'Transaccion creada correctamente',
            'transaccion': transaccion
        }
    except Exception as e:
        print(e)
        return {
            'success': False,
            'message': 'Ocurrio un error al crear la transaccion'
        }

def obtener_transacciones(usuario_id):
    try:
        transacciones = Transaccion.objects.filter(cuenta_origen__usuario_id=usuario_id).order_by('-id')
        return transacciones
    except Exception as e:
        return {
            'success': False,
            'message': 'Ocurrio un error al obtener las transacciones'
        }