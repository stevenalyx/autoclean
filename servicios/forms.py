import re

from django import forms

from .models import ServicioLavado, Vehiculo, validar_patente


class BootstrapMixin:
    """Agrega las clases de Bootstrap a todos los widgets."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css = 'form-select' if isinstance(widget, forms.Select) else 'form-control'
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {css}".strip()


class VehiculoForm(BootstrapMixin, forms.ModelForm):
    # Se declara aparte para normalizar (mayúsculas, sin guiones) ANTES de validar el formato
    patente = forms.CharField(label='Patente', max_length=10, help_text='Ej: ABCD12 o AB1234')

    class Meta:
        model = Vehiculo
        fields = ['patente', 'marca', 'modelo', 'propietario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # La patente es la clave primaria: no se edita una vez creado el vehículo
        if self.instance and not self.instance._state.adding:
            self.fields['patente'].disabled = True

    def clean_patente(self):
        patente = re.sub(r'[\s\-\.]', '', self.cleaned_data['patente']).upper()
        validar_patente(patente)
        return patente  # la unicidad la valida el modelo (validate_unique)

    def _limpiar_texto(self, campo):
        valor = self.cleaned_data[campo].strip()
        if not valor:
            raise forms.ValidationError('Este campo es obligatorio.')
        return valor

    def clean_marca(self):
        return self._limpiar_texto('marca')

    def clean_modelo(self):
        return self._limpiar_texto('modelo')

    def clean_propietario(self):
        return self._limpiar_texto('propietario')


class ServicioForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = ServicioLavado
        fields = ['vehiculo', 'tipo_lavado', 'fecha', 'precio', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'precio': forms.NumberInput(attrs={'min': 0, 'step': 1}),
        }

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio


class EstadoServicioForm(BootstrapMixin, forms.ModelForm):
    """Formulario reducido: es lo único que puede modificar un Trabajador."""
    class Meta:
        model = ServicioLavado
        fields = ['estado']
