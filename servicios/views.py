from django.contrib import messages
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from .forms import EstadoServicioForm, ServicioForm, VehiculoForm
from .models import ServicioLavado, Vehiculo
from .rangos import admin_required, ambos_required


# ======================= VEHÍCULOS =======================

@ambos_required
def vehiculo_list(request):
    q = request.GET.get('q', '').strip()
    vehiculos = Vehiculo.objects.annotate(total_servicios=Count('servicios'))
    if q:
        vehiculos = vehiculos.filter(
            Q(patente__icontains=q) | Q(marca__icontains=q)
            | Q(modelo__icontains=q) | Q(propietario__icontains=q)
        )
    return render(request, 'servicios/vehiculo_list.html', {'vehiculos': vehiculos, 'q': q})


@admin_required
def vehiculo_crear(request):
    form = VehiculoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        v = form.save()
        messages.success(request, f'Vehículo {v.patente} registrado correctamente.')
        return redirect('servicios:vehiculo_list')
    return render(request, 'servicios/form.html', {
        'form': form, 'titulo': 'Registrar vehículo',
        'cancel_url': 'servicios:vehiculo_list',
    })


@admin_required
def vehiculo_editar(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    form = VehiculoForm(request.POST or None, instance=vehiculo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Vehículo {vehiculo.patente} actualizado.')
        return redirect('servicios:vehiculo_list')
    return render(request, 'servicios/form.html', {
        'form': form, 'titulo': f'Editar vehículo {vehiculo.patente}',
        'cancel_url': 'servicios:vehiculo_list',
    })


@admin_required
def vehiculo_eliminar(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    finalizado = ServicioLavado.Estado.FINALIZADO
    activos = vehiculo.servicios.exclude(estado=finalizado).count()
    finalizados = vehiculo.servicios.filter(estado=finalizado).count()

    if request.method == 'POST':
        if activos:
            messages.error(
                request,
                f'No se puede eliminar {pk}: tiene {activos} servicio(s) pendiente(s) o en proceso.')
        else:
            with transaction.atomic():
                vehiculo.servicios.all().delete()   # solo quedan los finalizados
                vehiculo.delete()
            messages.success(request, f'Vehículo {pk} eliminado.')
        return redirect('servicios:vehiculo_list')

    if activos:
        advertencia = f'Tiene {activos} servicio(s) sin finalizar: no se podrá eliminar hasta que terminen.'
    elif finalizados:
        advertencia = f'Se eliminarán también sus {finalizados} servicio(s) finalizado(s).'
    else:
        advertencia = ''
    return render(request, 'servicios/confirmar_eliminar.html', {
        'titulo': 'Eliminar vehículo', 'objeto': str(vehiculo),
        'advertencia': advertencia, 'cancel_url': 'servicios:vehiculo_list',
    })


# ======================= SERVICIOS =======================

@ambos_required
def servicio_list(request):
    servicios = ServicioLavado.objects.select_related('vehiculo')
    estado = request.GET.get('estado', '')
    patente = request.GET.get('vehiculo', '')
    if estado in ServicioLavado.Estado.values:
        servicios = servicios.filter(estado=estado)
    if patente:
        servicios = servicios.filter(vehiculo_id=patente)
    return render(request, 'servicios/servicio_list.html', {
        'servicios': servicios, 'estados': ServicioLavado.Estado.choices,
        'estado_sel': estado, 'patente_sel': patente,
    })


@admin_required
def servicio_crear(request):
    initial = {}
    if request.GET.get('vehiculo'):
        initial['vehiculo'] = request.GET['vehiculo']
    form = ServicioForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Servicio de lavado registrado correctamente.')
        return redirect('servicios:servicio_list')
    return render(request, 'servicios/form.html', {
        'form': form, 'titulo': 'Registrar servicio de lavado',
        'cancel_url': 'servicios:servicio_list',
    })


@admin_required
def servicio_editar(request, pk):
    servicio = get_object_or_404(ServicioLavado, pk=pk)
    form = ServicioForm(request.POST or None, instance=servicio)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Servicio actualizado.')
        return redirect('servicios:servicio_list')
    return render(request, 'servicios/form.html', {
        'form': form, 'titulo': f'Editar servicio #{servicio.pk}',
        'cancel_url': 'servicios:servicio_list',
    })


@admin_required
def servicio_eliminar(request, pk):
    servicio = get_object_or_404(ServicioLavado, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado.')
        return redirect('servicios:servicio_list')
    return render(request, 'servicios/confirmar_eliminar.html', {
        'titulo': 'Eliminar servicio', 'objeto': str(servicio),
        'cancel_url': 'servicios:servicio_list',
    })


@ambos_required
def servicio_estado(request, pk):
    """Administrador y Trabajador pueden cambiar únicamente el estado."""
    servicio = get_object_or_404(ServicioLavado, pk=pk)
    form = EstadoServicioForm(request.POST or None, instance=servicio)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Estado del servicio #{pk} actualizado a "{servicio.get_estado_display()}".')
        return redirect('servicios:servicio_list')
    return render(request, 'servicios/form.html', {
        'form': form, 'titulo': f'Actualizar estado del servicio #{servicio.pk}',
        'subtitulo': str(servicio), 'cancel_url': 'servicios:servicio_list',
    })