from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction


TIPOS_TRANSACCIONES = [
    ('INGRESO', 'Ingreso'),
    ('EGRESO', 'Egreso'),
    ('TRANSFERENCIA', 'Transferencia'),
]

TIPOS_CUENTA = (
        ('CC', 'Cuenta Corriente'),
        ('CA', 'Cuenta de Ahorro'),
        ('CV', 'Cuenta Vista'),
        ('CI', 'Cuenta de Inversión'),
        ('CE', 'Cuenta Corriente Empresarial'),
        ('CD', 'Cuenta Digital'),
        ('OTRO', 'Otro'),
    )

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
    tipo = models.CharField(max_length=50, choices=TIPOS_CUENTA)

class MetaAhorro(models.Model):
    nombre = models.CharField(max_length=100)
    monto_objetivo = models.IntegerField()
    monto_actual = models.IntegerField()
    fecha_limite = models.DateField()
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class TransaccionRecurrente(models.Model):
    tipo = models.CharField(max_length=50, choices=TIPOS_TRANSACCIONES)
    descripcion = models.CharField(max_length=100, blank=True)
    monto = models.IntegerField()
    frecuencia = models.CharField(max_length=50, choices=FRECUENCIAS)
    proxima_ejecucion = models.DateField()
    cuenta_relacionada = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, null=True)

class Transaccion(models.Model):
    tipo = models.CharField(max_length=50, choices=TIPOS_TRANSACCIONES)
    monto = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    cuenta_origen = models.ForeignKey(
        Cuenta, on_delete=models.SET_NULL, related_name='transaccion_origen', null=True, blank=True
    )
    cuenta_destino = models.ForeignKey(
        Cuenta, on_delete=models.SET_NULL, related_name='transaccion_destino', null=True, blank=True
    )
    meta_ahorro = models.ForeignKey(
        MetaAhorro, on_delete=models.SET_NULL, related_name='transaccion_meta_ahorro', null=True, blank=True
    )
    descripcion = models.CharField(max_length=100, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def clean(self):
    # --- Validaciones básicas por tipo ---
        if self.tipo == 'INGRESO' and self.cuenta_origen:
            raise ValidationError("Un ingreso no debe tener cuenta de origen.")

        if self.tipo == 'EGRESO' and self.cuenta_destino:
            raise ValidationError("Un egreso no debe tener cuenta de destino.")

    # --- Validaciones para TRANSFERENCIA ---
        if self.tipo == 'TRANSFERENCIA':
        # Requiere un origen
            if not (self.cuenta_origen or self.meta_ahorro):
                raise ValidationError("Una transferencia debe tener una cuenta o meta de ahorro de origen.")

        # Requiere un destino
            if not (self.cuenta_destino or self.meta_ahorro):
                raise ValidationError("Una transferencia debe tener una cuenta o meta de ahorro de destino.")

        # No puede tener origen y destino vacíos o idénticos
            if (self.cuenta_origen and self.cuenta_destino) and (self.cuenta_origen == self.cuenta_destino):
                raise ValidationError("No puedes transferir a la misma cuenta.")

            if self.meta_ahorro and (
                (self.cuenta_origen and self.meta_ahorro == self.cuenta_origen) or
                (self.cuenta_destino and self.meta_ahorro == self.cuenta_destino)):
                raise ValidationError("No puedes transferir entre la misma meta y cuenta.")

    # --- Validación de saldo en origen ---
        if self.tipo in ('EGRESO', 'TRANSFERENCIA'):
            if self.cuenta_origen and self.cuenta_origen.saldo < self.monto:
                raise ValidationError("Saldo insuficiente en la cuenta de origen.")


    # --- Validación de límites de meta de ahorro destino ---
        if self.meta_ahorro and self.tipo in ('INGRESO', 'TRANSFERENCIA'):
            if self.meta_ahorro.monto_actual + self.monto > self.meta_ahorro.monto_objetivo:
                raise ValidationError("No puedes sobrepasar el monto objetivo de la meta de ahorro.")


    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean()
        with transaction.atomic():
            if self._state.adding:  # Solo si es nueva transacción
                # Restar de origen
                if self.tipo in ('EGRESO', 'TRANSFERENCIA'):
                    if self.cuenta_origen:
                        self.cuenta_origen.saldo -= self.monto
                        self.cuenta_origen.save()
                    elif self.meta_ahorro:
                        self.meta_ahorro.monto_actual -= self.monto
                        self.meta_ahorro.save()
                # Sumar al destino
                if self.tipo in ('INGRESO', 'TRANSFERENCIA'):
                    if self.cuenta_destino:
                        self.cuenta_destino.saldo += self.monto
                        self.cuenta_destino.save()
                    elif self.meta_ahorro:
                        self.meta_ahorro.monto_actual += self.monto
                        self.meta_ahorro.save()
            super().save(*args, **kwargs)


