from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

ADMIN = 'Administrador'
TRABAJADOR = 'Trabajador'


def es_administrador(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name=ADMIN).exists()
    )


def es_trabajador(user):
    return user.is_authenticated and user.groups.filter(name=TRABAJADOR).exists()


def grupo_requerido(*grupos):
    """Exige sesión iniciada y pertenecer a alguno de los grupos indicados."""
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser or request.user.groups.filter(name__in=grupos).exists():
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator


admin_required = grupo_requerido(ADMIN)
ambos_required = grupo_requerido(ADMIN, TRABAJADOR)
