# Backend-BookNest

## Descripción
**Backend-BookNest** es una API RESTful desarrollada para gestionar una plataforma de biblioteca personal y seguimiento de lecturas. Permite a los usuarios registrarse, explorar un catálogo de libros, gestionar autores, y llevar un registro detallado de las lecturas que han realizado o tienen en progreso.

## Características y Funcionalidades Principales
- **Gestión de Usuarios (Auth):** Registro de usuarios, inicio de sesión seguro (autenticación) y gestión de sesiones mediante tokens JWT. Las contraseñas se almacenan de manera segura utilizando hashing (`bcrypt`).
- **Gestión de Libros:** Operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para el catálogo de libros de la plataforma.
- **Gestión de Autores y Editoriales:** Administración de los autores de los libros, manteniendo las relaciones en la base de datos.
- **Seguimiento de Lecturas (Readings):** Permite asociar libros a usuarios para llevar un seguimiento de sus lecturas y el estado de las mismas.
- **Documentación Interactiva:** Generación automática de documentación de la API gracias a Swagger UI y ReDoc (nativos de FastAPI).

## Tecnologías Utilizadas

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web moderno y de alto rendimiento para construir APIs con Python.
- **Python 3:** Lenguaje principal de desarrollo.
- **Uvicorn:** Servidor web ASGI ultra rápido.
- **Pydantic:** Validación de datos, serialización y gestión de configuraciones (incluyendo `pydantic-settings`).
- **Seguridad:** `bcrypt` para el hashing de contraseñas y `python-jose` para la firma y verificación de JSON Web Tokens (JWT).

### Base de Datos
- **[MariaDB](https://mariadb.org/):** Sistema de gestión de bases de datos relacional para almacenar toda la información del sistema.
- **[Adminer](https://www.adminer.org/):** Herramienta ligera de administración de bases de datos con interfaz web.

### Infraestructura y Despliegue
- **[Docker](https://www.docker.com/):** Para contenerizar tanto la aplicación web como los servicios dependientes.
- **Docker Compose:** Para orquestar los múltiples contenedores de forma conjunta (API, Base de datos y Adminer) facilitando el despliegue de desarrollo.

## Estructura del Proyecto

```text
Backend-BookNest/
├── api_nestbook/
│   ├── app/                # Código fuente principal de la API
│   │   ├── auth/           # Lógica de autenticación y seguridad
│   │   ├── database/       # Conexiones y configuraciones a MariaDB
│   │   ├── models/         # Modelos de base de datos / entidades del sistema
│   │   ├── routers/        # Controladores (endpoints) separados por módulo
│   │   └── schemas/        # Esquemas de validación de datos (Pydantic)
│   ├── docker/             # Dockerfile para levantar la imagen de FastAPI
│   ├── compose.yaml        # Configuración de servicios (API, DB, Adminer)
│   └── requirements.txt    # Dependencias del entorno Python
├── doc/                    # Documentación y diseños técnicos
│   ├── db/                 # Modelo Entidad-Relación y script SQL de inicialización
│   ├── examples_json/      # Ejemplos de peticiones/respuestas (payloads)
│   └── Requirements/       # Documentos de requisitos del proyecto
└── README.md               # Este archivo
```

## Requisitos Previos
- Tener instalado [Docker](https://docs.docker.com/get-docker/) y Docker Compose.
- Crear un archivo de configuración `.env` en la ruta `api_nestbook/` para definir las variables de entorno necesarias (ej: credenciales de MariaDB).

## Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd Backend-BookNest
   ```

2. **Configurar las variables de entorno:**
   Navega a `api_nestbook` y crea el archivo `.env` basándote en las variables que requiera la conexión a base de datos (por ejemplo, `MARIADB_ROOT_PASSWORD`, `MARIADB_USER`, `MARIADB_PASSWORD`, `MARIADB_DATABASE`).

3. **Levantar los servicios con Docker Compose:**
   ```bash
   cd api_nestbook
   docker compose up --build -d
   ```

4. **Acceder a la Aplicación:**
   - **API (Raíz):** `http://localhost:8000/`
   - **Documentación Interactiva (Swagger UI):** `http://localhost:8000/docs`
   - **Documentación ReDoc:** `http://localhost:8000/redoc`
   - **Adminer (Gestión DB):** `http://localhost:8080/`

## Base de Datos
El proyecto incluye un volumen que monta el archivo inicial SQL de configuración `doc/db/Physical-Design/bbdd_booknest.sql` dentro del contenedor de MariaDB para automatizar la creación de la estructura de tablas la primera vez que se construye el proyecto con Docker.
