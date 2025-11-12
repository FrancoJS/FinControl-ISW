from gestion.models import Transaccion


def crear_transaccion(transaccion):
    try:
        transaccion = Transaccion(tipo=transaccion['tipo'], monto=transaccion['monto'], cuenta_origen_id=transaccion['cuenta_origen'], cuenta_destino_id=transaccion['cuenta_destino'], descripcion=transaccion['descripcion'], usuario_id=transaccion['usuario'], meta_ahorro_id=transaccion['meta_ahorro'])
        transaccion.save()
        return {
            'success': True,
            'mensaje': 'Transaccion creada correctamente',
            'transaccion': transaccion
        }
    except Exception as e:
        print(e)
        return {
            'success': False,
            'mensaje': 'Ocurrio un error al crear la transaccion'
        }

def obtener_transacciones(usuario_id):
    try:
        transacciones = Transaccion.objects.filter(usuario_id=usuario_id).order_by('-id')
        return transacciones
    except Exception as e:
        return {
            'success': False,
            'mensaje': 'Ocurrio un error al obtener las transacciones'
        }