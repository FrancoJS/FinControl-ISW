from django.shortcuts import render
from gestion.models import MetaAhorro, Cuenta
from datetime import date


def obtener_metas(usuario_id):
    metas = MetaAhorro.objects.filter(cuenta_relacionada__usuario_id=usuario_id)
    for m in metas:
        if m.monto_objetivo > 0:
            m.porcentaje = round((m.monto_actual / m.monto_objetivo) * 100, 2)
        else:
            m.porcentaje = 0
    return metas
    
def crear_meta(request):
    try:
        nombre = request.POST['nombre']
        monto_objetivo = request.POST['monto_objetivo']
        fecha_limite = request.POST['fecha_limite']
        cuenta_relacionada = request.POST['cuenta_relacionada']
        cuenta_id = request.POST['cuenta']

        if monto_objetivo <= 0:
            return {"success": False, "mensaje": "El monto objetivo debe ser mayor a 0."}

        if date.fromisoformat(fecha_limite) < date.today():
            return {"success": False, "mensaje": "La fecha limite debe ser posterior a la fecha actual."}

        nueva_meta = MetaAhorro(
            nombre=nombre,
            monto_objetivo=monto_objetivo,
            monto_actual=0,
            fecha_limite=fecha_limite,
            cuenta_relacionada=Cuenta.objects.get(id=cuenta_id)
        )
        nueva_meta.save()
        return {"success": True, "mensaje": "Meta creada correctamente."}
    except Exception as e:
        print("Error al crear la meta:", e)
        return {"success": False, "mensaje": "Ocurrió un error al crear la meta."}
    
def actualizar_progreso(usuario_id):
    try:
        metas = MetaAhorro.objects.filter(cuenta_relacionada__usuario_id=usuario_id)
        for meta in metas:
            cuenta = meta.cuenta_relacionada
            nuevo_monto = min(cuenta.saldo, meta.monto_objetivo)
            meta.monto_actual = nuevo_monto
            meta.save()

        return {"success": True, "mensaje": "Progreso actualizado correctamente."}

    except Exception as e:
        print("Error al actualizar progreso:", e)
        return {"success": False, "mensaje": "Error al actualizar progreso de metas."}