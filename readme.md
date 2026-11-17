# AutoClean

Sistema web para gestionar los servicios de lavado de un negocio de autos: llevar el registro de los vehículos, los servicios que se les hacen y en qué estado va cada uno. Lo hice con Django, MySQL y Bootstrap como proyecto de la carrera de Ingeniería en Informática y Ciberseguridad en INACAP Curicó.

<!-- Cuando tengas capturas, guárdalas en una carpeta docs/ y agrégalas aquí:
![Lista de vehículos](docs/vehiculos.png)
![Lista de servicios](docs/servicios.png)
-->

## Qué hace

- Inicio y cierre de sesión con la autenticación de Django.
- Dos roles, **Administrador** y **Trabajador**, manejados con grupos de Django.
- CRUD completo de vehículos (patente, marca, modelo, propietario).
- CRUD de servicios de lavado (vehículo, tipo de lavado, fecha, precio y estado).
- Cambio de estado de un servicio: Pendiente, En proceso o Finalizado.
- Buscador de vehículos y filtro de servicios por estado.
- Confirmación antes de eliminar cualquier registro.
- Interfaz responsiva con Bootstrap 5, con mensajes de éxito y de error.

## Roles y permisos

| Acción                                   | Administrador | Trabajador |
|------------------------------------------|:-------------:|:----------:|
| Ver vehículos y servicios                |       ✔       |     ✔      |
| Crear, editar y eliminar vehículos       |       ✔       |     ✘      |
| Crear, editar y eliminar servicios       |       ✔       |     ✘      |
| Cambiar el estado de un servicio         |       ✔       |     ✔      |

Un usuario sin sesión es enviado al login. Un usuario con sesión pero sin el rol necesario ve una pantalla de acceso denegado.

## Reglas de los datos

- La patente es única y se normaliza antes de guardar (mayúsculas, sin guiones ni espacios). Acepta el formato antiguo (`AB1234`) y el nuevo (`ABCD12`).
- El precio no puede ser negativo.
- Un vehículo con servicios pendientes o en proceso **no se puede eliminar**. Si todos sus servicios están finalizados, se puede eliminar y esos servicios se borran junto con él.

## Tecnologías

- Python 3.11
- Django 3.2
- MySQL
- Bootstrap 5.3

## Cómo correrlo en tu computador

**1. Clona el repositorio y entra a la carpeta**

```bash
git clone https://github.com/stevenalyx/AutoClean.git
cd AutoClean
```

**2. Crea un entorno virtual e instala las dependencias**

```bash
python -m venv venv
venv\Scripts\activate        # en Linux o Mac: source venv/bin/activate
pip install django==3.2 mysqlclient
```

Si `mysqlclient` te da problemas al instalar en Windows, puedes usar `pip install pymysql` y agregar esto al principio de `gestion/__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

**3. Crea la base de datos en MySQL**

```sql
CREATE DATABASE autoclean CHARACTER SET utf8mb4;
```

**4. Configura la conexión**

En `gestion/settings.py`, ajusta el bloque `DATABASES` con tu usuario y contraseña de MySQL.

**5. Migra y crea los usuarios**

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py crear_roles --demo
```

El último comando crea los grupos Administrador y Trabajador, y además dos usuarios de prueba: `admin_demo` y `trabajador_demo`, ambos con la contraseña `autoclean123`. Es solo para probar; no los uses en un entorno real. Si prefieres hacerlo a mano, también puedes crear los grupos y asignar usuarios desde `/admin/`.

**6. Levanta el servidor**

```bash
python manage.py runserver
```

Abre http://127.0.0.1:8000/ e inicia sesión.

## Estructura del proyecto

```
AutoClean/
├── manage.py
├── gestion/               # configuración del proyecto (settings, urls)
└── servicios/             # la aplicación
    ├── models.py          # Vehiculo y ServicioLavado
    ├── forms.py           # formularios con sus validaciones
    ├── views.py           # vistas del CRUD
    ├── urls.py
    ├── rangos.py          # decoradores de login y de roles
    ├── permisos_roles.py  # context processor: entrega el rol a las plantillas
    ├── management/        # comando crear_roles
    └── templates/         # base.html, login y plantillas de cada sección
```

## Modelo de datos

**Vehiculo**: `patente` (única), `marca`, `modelo`, `propietario`.

**ServicioLavado**: `vehiculo` (clave foránea a Vehiculo, con `PROTECT`), `tipo_lavado` (Básico, Completo o Premium), `fecha`, `precio` y `estado`.

Un vehículo puede tener muchos servicios.

## Autor

Steven · [@stevenalyx](https://github.com/stevenalyx)