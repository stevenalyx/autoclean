from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'servicios'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='servicios:vehiculo_list', permanent=False)),

    path('vehiculos/', views.vehiculo_list, name='vehiculo_list'),
    path('vehiculos/nuevo/', views.vehiculo_crear, name='vehiculo_crear'),
    path('vehiculos/<str:pk>/editar/', views.vehiculo_editar, name='vehiculo_editar'),
    path('vehiculos/<str:pk>/eliminar/', views.vehiculo_eliminar, name='vehiculo_eliminar'),

    path('servicios/', views.servicio_list, name='servicio_list'),
    path('servicios/nuevo/', views.servicio_crear, name='servicio_crear'),
    path('servicios/<int:pk>/editar/', views.servicio_editar, name='servicio_editar'),
    path('servicios/<int:pk>/estado/', views.servicio_estado, name='servicio_estado'),
    path('servicios/<int:pk>/eliminar/', views.servicio_eliminar, name='servicio_eliminar'),
]
