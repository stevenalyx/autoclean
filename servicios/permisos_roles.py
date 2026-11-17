from .rangos import es_administrador, es_trabajador


def roles(request):
    return {
        'es_admin': es_administrador(request.user),
        'es_trabajador': es_trabajador(request.user),
    }