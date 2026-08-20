# Aplicativo de Bienestar Universitario – IUB

Prototipo funcional mínimo (primera iteración) del sistema de registro y
gestión de actividades de Bienestar Universitario, construido con
**Python + Django 6.1 + MySQL/MariaDB**.

> Nota: el taller original define PostgreSQL como tecnología principal.
> Si este proyecto se entrega/evalúa contra ese documento, confirma con tu
> equipo o el profesor que el cambio a MySQL esté permitido.

> ⚠️ **Importante sobre versiones — léelo antes de instalar.**
> Django 6.1 requiere **MariaDB 10.11 o superior** (o MySQL 8.4+). XAMPP
> para Windows trae por defecto MariaDB 10.4.32, que **no es compatible**.
> Este proyecto asume que ya actualizaste manualmente el MariaDB de tu
> XAMPP a una versión 10.11+ (por ejemplo 11.4 LTS u 11.8 LTS). Si no lo
> has hecho, sigue la guía de actualización antes de continuar, o usa la
> alternativa más simple: bajar el proyecto a Django 4.2 LTS (compatible
> con la MariaDB que XAMPP trae de fábrica, sin tocar nada de XAMPP).

## Qué incluye esta primera iteración

- **Usuario personalizado** (`usuarios`): tipo/número de documento, correo
  institucional, programa o dependencia y rol (estudiante, docente,
  funcionario, contratista, personal de Bienestar). Login/logout con el
  sistema de autenticación de Django.
- **Actividades** (`actividades`): registro, cupos, estado, responsable.
- **Inscripciones**: un usuario se inscribe en una actividad, se valida que
  haya cupo, y se genera un **código QR único** (UUID) por inscripción.
- **Validación de asistencia**: en esta entrega es **manual** (se ingresa el
  código como texto) — el escaneo por cámara del navegador queda como
  mejora futura, tal como se definió en el análisis de viabilidad.
- **Panel de administración** de Django para el CRUD de usuarios y
  actividades (cubre el requerimiento de complejidad baja / viabilidad alta).

## Estructura del proyecto

```
bienestar_iub/       Configuración del proyecto (settings, urls)
usuarios/            App: modelo de usuario personalizado + admin
actividades/         App: Actividad, Inscripción, vistas, QR, templates
templates/            Templates base y de login
database/             Volcado SQL (schema) para importar en XAMPP/phpMyAdmin
requirements.txt
.env.example          Variables de entorno de ejemplo
```

## Puesta en marcha con XAMPP (MySQL local)

1. **Iniciar MySQL desde el Panel de Control de XAMPP** (botón "Start" en
   el módulo MySQL). Por defecto queda en `localhost:3306`, usuario `root`
   sin contraseña.

2. **Crear la base de datos**, con cualquiera de estas dos opciones:
   - **Opción A (recomendada): importar el schema ya listo.**
     Abre phpMyAdmin (`http://localhost/phpmyadmin`) → pestaña *Importar*
     → selecciona el archivo `database/bienestar_iub_schema.sql` de este
     proyecto → *Continuar*. Esto crea la base `bienestar_iub` con todas
     las tablas (usuarios, actividades, inscripciones, tablas internas de
     Django) ya generadas y probadas.
   - **Opción B: crear la base vacía y dejar que Django genere las tablas.**
     En phpMyAdmin, *Nueva* → nombre `bienestar_iub` → cotejamiento
     `utf8mb4_unicode_ci` → *Crear*. Luego correr `migrate` (paso 6) para
     que Django cree las tablas.

3. Crear y activar entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   Se usa **PyMySQL** (no `mysqlclient`) como driver de MySQL porque es
   puro Python: no necesita compilar nada ni instalar Visual C++ Build
   Tools en Windows.

5. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   ```
   Los valores por defecto ya están pensados para XAMPP (`root`, sin
   contraseña, puerto `3306`). Ajusta solo si tu instalación es distinta.

   Cargar las variables antes de correr los comandos:
   ```bash
   export $(cat .env | xargs)          # Linux/Mac
   # En Windows PowerShell, exporta cada variable a mano, por ejemplo:
   # $env:DB_NAME="bienestar_iub"
   ```

6. Migraciones y superusuario:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
   Si ya importaste `database/bienestar_iub_schema.sql` (Opción A), este
   paso solo confirma que todo está sincronizado; no debería crear tablas
   nuevas.

7. Levantar el servidor:
   ```bash
   python manage.py runserver
   ```
   - Panel admin: http://127.0.0.1:8000/admin/
   - Actividades: http://127.0.0.1:8000/actividades/
   - Validación manual de asistencia (solo personal de Bienestar):
     http://127.0.0.1:8000/actividades/validar-asistencia/

### Si aún no tienes XAMPP levantado

Puedes arrancar con SQLite mientras lo configuras: pon
`DJANGO_USE_SQLITE=True` en tu `.env`. Recuerda volver a `False` y borrar
`db.sqlite3` cuando quieras pasar a MySQL de verdad.

## Próximos pasos sugeridos (según el análisis de riesgos del taller)

1. Crear el repositorio en GitHub **ya**, antes de seguir programando, con
   ramas por funcionalidad y commits frecuentes.
2. Probar un despliegue vacío en Hostinger cuanto antes (WSGI + variables de
   entorno) para descartar problemas de configuración.
3. Documentar en este README cualquier paso adicional de entorno para que
   todo el equipo pueda levantar el proyecto localmente.
4. Iterar sobre formularios propios (en vez de solo el admin) para que
   estudiantes/docentes se registren desde una vista pública si se requiere.
5. Dejar el escaneo de QR por cámara (getUserMedia + jsQR/ZXing) para una
   iteración futura, como quedó definido en el alcance.
