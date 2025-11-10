from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

class Cuenta (models.Model):
    nombre = models.CharField(max_length=100)
    saldo = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Transaccion(models.Model):
    tipo = models.CharField(max_length=50)
    monto = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    cuenta_origen = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='cuenta_origen')
    cuenta_destino = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='cuenta_destino')
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)

class MetaAhorro(models.Model):
    nombre = models.CharField(max_length=100)
    monto_objetivo = models.IntegerField()
    monto_actual = models.IntegerField()
    fecha_limite = models.DateField()
    cuenta_relacionada = models.ForeignKey(Cuenta, on_delete=models.CASCADE)

class TransaccionRecurrente(models.Model):
    tipo = models.CharField(max_length=50)
    monto = models.IntegerField()
    frecuencia = models.CharField(max_length=50)
    proxima_ejecucion = models.DateField()
    cuenta_relacionada = models.ForeignKey(Cuenta, on_delete=models.CASCADE)