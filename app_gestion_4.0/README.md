# Aplicación de Gestión de Usuarios y Recursos del Sistema

Esta es una aplicación web desarrollada en Flask que permite gestionar usuarios y monitorear los recursos del sistema (CPU, RAM, Disco). Además, incluye funcionalidades como la generación de informes en PDF y CSV, backups automáticos de la base de datos, y la limpieza de backups antiguos.

## Características Principales

- **Gestión de Usuarios**: Registro, inicio de sesión, edición de perfiles y asignación de roles (usuario/admin).
- **Monitoreo de Recursos**: Visualización en tiempo real del uso de CPU, RAM y Disco.
- **Generación de Informes**: Creación de informes en formato PDF y CSV con el estado de los recursos del sistema.
- **Backups Automáticos**: Realización de backups automáticos de la base de datos y limpieza de backups antiguos.
- **Logs de Actividad**: Registro de actividades y errores en archivos de log para facilitar la depuración y el monitoreo.

## Tecnologías Utilizadas

- **Flask**: Framework web para Python.
- **SQLAlchemy**: ORM para la gestión de la base de datos.
- **Flask-Login**: Manejo de autenticación y sesiones de usuarios.
- **APScheduler**: Programación de tareas en segundo plano (backups automáticos, monitoreo de recursos).
- **psutil**: Monitoreo de recursos del sistema (CPU, RAM, Disco).
- **FPDF**: Generación de archivos PDF.
- **csv**: Generación de archivos csv.
- **Flask-WTF**: Manejo de formularios web.

## Configuración del Proyecto

### Requisitos Previos

- Python 3.8 o superior.
- MySQL instalado y configurado.
- XAMPP (opcional, para usar MySQL en Windows).

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/JosiasmDev/migithub.git
   cd /ruta/donde/guardaste/el/repositorio/app_gestion_4.0

2. **Crear un entorno en Python**:
    ```bash
    python -m venv venv
    venv\Scripts\activate

3. **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt

4. **Configurar la base de datos**:
- Crear una base de datos en MySQL llamada gestion_sistemas.

- Configurar las credenciales de la base de datos en config.py.

5. **Ejecutar migraciones**:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade

6. **Ejecución**
    ```bash	
    python run.py

## Estructura del Proyecto

- **run.py** Punto de entrada de la aplicación.

- **config.py** Configuración de la aplicación, incluyendo la conexión a la base de datos y rutas de carpetas.

- **utils.py** Funciones utilitarias para la generación de backups, informes y limpieza de backups.

- **forms.py** Formularios para el registro, inicio de sesión y edición de usuarios.

- **app/init.py** Inicialización de la aplicación, configuración de extensiones y blueprints.

- **app/controllers/** Controladores para la gestión de usuarios y recursos.

- **app/models/** Modelos de la base de datos.

- **app/templates/** Plantillas HTML para las vistas de la aplicación.

## Uso de la aplicación.

- **Registro y Autenticación**

Los usuarios pueden registrarse e iniciar sesión en la aplicación.

Los administradores pueden editar los roles de los usuarios.

- **Monitoreo de Recursos**

La aplicación muestra el uso actual de CPU, RAM y Disco.

Los usuarios pueden generar informes en PDF o CSV con el estado de los recursos.

- **Backups**

La aplicación realiza backups automáticos de la base de datos cada 10 segundos (configurable).

Los backups antiguos (más de 2 días) se eliminan automáticamente.

- **Logs**

Los logs de actividad se almacenan en la carpeta logs/ y pueden ser visualizados desde la interfaz web.


## Contribución.

Si deseas contribuir a este proyecto, sigue estos pasos:

Haz un fork del repositorio.

Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).

Realiza tus cambios y haz commit (git commit -am 'Añade nueva funcionalidad').

Haz push a la rama (git push origin feature/nueva-funcionalidad).

Abre un Pull Request.


## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto
Si tienes alguna pregunta o sugerencia, no dudes en contactarme en josiasdicampus@gmail.com.