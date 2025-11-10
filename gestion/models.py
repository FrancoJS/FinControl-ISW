from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction


TIPOS_TRANSACCIONES = [
    ('INGRESO', 'Ingreso'),
    ('EGRESO', 'Egreso'),
    ('TRANSFERENCIA', 'Transferencia'),
]

FRECUENCIAS = [
    ('DIARIO', 'Diario'),
    ('SEMANAL', 'Semanal'),
    ('MENSUAL', 'Mensual'),
    ('ANUAL', 'Anual'),
]
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

class Cuenta (models.Model):
    nombre = models.CharField(max_length=100)
    saldo = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Transaccion(models.Model):
    tipo = models.CharField(max_length=50, choices=TIPOS_TRANSACCIONES)
    monto = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    cuenta_origen = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, related_name='transaccion_origen', null=True, blank=True)
    cuenta_destino = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, related_name='transaccion_destino', null=True, blank=True)
    descripcion = models.CharField(max_length=100, blank=True)
    categoria = models.CharField(max_length=50, blank=True)
    def clean(self):
        if self.tipo == 'INGRESO' and self.cuenta_origen:
            raise ValidationError("Un ingreso no debe tener cuenta de origen.")
        if self.tipo == 'EGRESO' and self.cuenta_destino:
            raise ValidationError("Un egreso no debe tener cuenta de destino.")
        if self.tipo == 'TRANSFERENCIA':
            if not self.cuenta_origen or not self.cuenta_destino:
                raise ValidationError("Una transferencia requiere cuenta de origen y destino.")
        if self.cuenta_origen == self.cuenta_destino:
            raise ValidationError("No puedes transferir a la misma cuenta.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean()
        with transaction.atomic():  # Garantiza que todo se haga o nada
            if self._state.adding:  # Solo si es nueva transacción
                if self.tipo in ('EGRESO', 'TRANSFERENCIA'):
                    if self.cuenta_origen.saldo < self.monto:
                        raise ValidationError("Saldo insuficiente en la cuenta de origen.")
                    self.cuenta_origen.saldo -= self.monto
                    self.cuenta_origen.save()
                if self.tipo in ('INGRESO', 'TRANSFERENCIA'):
                    self.cuenta_destino.saldo += self.monto
                    self.cuenta_destino.save()
            super().save(*args, **kwargs)


class MetaAhorro(models.Model):
    nombre = models.CharField(max_length=100)
    monto_objetivo = models.IntegerField()
    monto_actual = models.IntegerField()
    fecha_limite = models.DateField()
    cuenta_relacionada = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='meta_ahorro')

class TransaccionRecurrente(models.Model):
    tipo = models.CharField(max_length=50, choices=TIPOS_TRANSACCIONES)
    descripcion = models.CharField(max_length=100, blank=True)
    monto = models.IntegerField()
    frecuencia = models.CharField(max_length=50, choices=FRECUENCIAS)
    proxima_ejecucion = models.DateField()
    cuenta_relacionada = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, null=True)