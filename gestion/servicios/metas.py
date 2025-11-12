from gestion.models import MetaAhorro, Cuenta
from datetime import datetime

def crear_meta(request):
    try:
        print("Entrando a crear_meta...")  # Depuración

        nombre = request.POST.get('nombre')
        monto_objetivo = float(request.POST.get('monto_objetivo', 0))
        monto_actual = float(request.POST.get('monto_actual', 0))
        fecha_limite = request.POST.get('fecha_limite')
        usuario_id = request.session.get('usuario_id')

        print(f"Datos recibidos: nombre={nombre}, objetivo={monto_objetivo}, actual={monto_actual}, fecha={fecha_limite}, usuario={usuario_id}")

        if not usuario_id:
            print("No hay usuario_id en sesión")
            return {"success": False, "mensaje": "Usuario no autenticado."}


        meta = MetaAhorro.objects.create(
            nombre=nombre,
            monto_objetivo=monto_objetivo,
            monto_actual=monto_actual,
            fecha_limite=fecha_limite,
            user_id=usuario_id,
        )

        print("Meta creada correctamente con ID:", meta.id)

        return {"success": True, "mensaje": "Meta creada correctamente."}

    except Exception as e:
        import traceback
        print("Error al crear meta:", e)
        traceback.print_exc()
        return {"success": False, "mensaje": "Ocurrió un error al guardar la meta."}

def obtener_metas(usuario_id):
    try:
        metas = MetaAhorro.objects.filter(user_id=usuario_id).order_by('-id')
        for meta in metas:
            if meta.monto_objetivo > 0:
                meta.porcentaje = round((meta.monto_actual / meta.monto_objetivo) * 100, 2)
            else:
                meta.porcentaje = 0
        return metas
    except Exception as e:
        print("Error al obtener metas:", e)
        return []

def editar_meta(meta_id, nombre, monto_objetivo,  fecha_limite,  usuario_id):
    try:
        meta = MetaAhorro.objects.get(id=meta_id, usuario_id=usuario_id)
        meta.nombre = nombre
        meta.monto_objetivo = monto_objetivo
        meta.fecha_limite = fecha_limite
        meta.save()
        return {"success": True, "mensaje": "Meta actualizada correctamente."}
    except MetaAhorro.DoesNotExist:
        return {"success": False, "mensaje": "Meta no encontrada."}
    except Exception as e:
        return {"success": False, "mensaje": f"Ocurrió un error: {str(e)}"}

def eliminar_meta(meta_id):
    try:
        meta = MetaAhorro.objects.get(id=meta_id)
        meta.delete()
        return {
            "success": True,
            "mensaje": "Meta eliminada correctamente."
        }
    except MetaAhorro.DoesNotExist:
        return {
            "success": False,
            "mensaje": "La meta no existe."
        }
    except Exception as e:
        print("Error al eliminar meta:", e)
        return {
            "success": False,
            "mensaje": "Ocurrió un error al eliminar la meta."
        }