from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

# Patentes chilenas: formato antiguo (AB1234) y nuevo (ABCD12)
validar_patente = RegexValidator(
    r'^([A-Z]{2}\d{4}|[A-Z]{4}\d{2})$',
    'Formato de patente inválido. Ejemplos: ABCD12 o AB1234.',
)


class Vehiculo(models.Model):
    patente = models.CharField(
        'Patente', max_length=6, primary_key=True,
        validators=[validar_patente],
        error_messages={'unique': 'Ya existe un vehículo registrado con esa patente.'},
    )
    marca = models.CharField('Marca', max_length=50)
    modelo = models.CharField('Modelo', max_length=50)
    propietario = models.CharField('Propietario', max_length=100)

    class Meta:
        ordering = ['patente']
        verbose_name = 'vehículo'
        verbose_name_plural = 'vehículos'

    def __str__(self):
        return f'{self.patente} - {self.marca} {self.modelo}'


class ServicioLavado(models.Model):
    class TipoLavado(models.TextChoices):
        BASICO = 'BASICO', 'Básico'
        COMPLETO = 'COMPLETO', 'Completo'
        PREMIUM = 'PREMIUM', 'Premium'

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_PROCESO = 'EN_PROCESO', 'En proceso'
        FINALIZADO = 'FINALIZADO', 'Finalizado'

    # PROTECT: no se puede borrar un vehículo que tenga servicios (integridad de datos)
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.PROTECT, related_name='servicios',
        verbose_name='Vehículo',
    )
    tipo_lavado = models.CharField('Tipo de lavado', max_length=10, choices=TipoLavado.choices)
    fecha = models.DateField('Fecha', default=timezone.localdate)
    precio = models.DecimalField(
        'Precio (CLP)', max_digits=10, decimal_places=0,
        validators=[MinValueValidator(0, 'El precio no puede ser negativo.')],
    )
    estado = models.CharField(
        'Estado', max_length=10, choices=Estado.choices, default=Estado.PENDIENTE,
    )

    class Meta:
        ordering = ['-fecha', '-id']
        verbose_name = 'servicio de lavado'
        verbose_name_plural = 'servicios de lavado'

    def __str__(self):
        return f'{self.get_tipo_lavado_display()} - {self.vehiculo_id} ({self.fecha})'
