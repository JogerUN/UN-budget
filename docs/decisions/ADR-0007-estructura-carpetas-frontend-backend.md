# ADR-0007: Estructura del repositorio para frontend y backend

**Autor:** Kevin Flórez  
**Fecha:** 2026-11-18

## Estado

Propuesto

## Contexto

UN-Budget necesita una interfaz web para presentar información y un backend para exponer operaciones y consultar PostgreSQL. El equipo también necesita construir y ejecutar ambas aplicaciones en conjunto, pero mantener sus lenguajes, dependencias y responsabilidades separados.

El repositorio actual ya refleja esa separación: `compose.yaml` coordina los servicios desde la raíz; `src/backend` contiene la aplicación FastAPI y sus dependencias Python; `src/frontend` contiene una aplicación Astro, sus dependencias Node, archivos estáticos y configuración de Nginx. Ambos servicios tienen su propio Dockerfile. Los archivos `.env` locales no se incluyen en este ADR ni deben versionarse.

## Estructura observada

```text
.
├── compose.yaml
├── docs/
└── src/
    ├── backend/
    │   ├── Dockerfile
    │   ├── .dockerignore
    │   ├── .env.example
    │   ├── requirements.txt
    │   ├── pyproject.toml
    │   ├── alembic.ini
    │   └── app/
    │       ├── main.py
    │       ├── api/v1/endpoints/
    │       ├── core/config.py
    │       ├── db/session.py
    │       ├── models/prueba.py
    │       ├── repositories/consultas.py
    │       ├── schemas/
    │       └── services/
    └── frontend/
        ├── Dockerfile
        ├── nginx.conf
        ├── package.json
        ├── package-lock.json
        ├── astro.config.mjs
        ├── tsconfig.json
        ├── public/
        └── src/
            ├── pages/index.astro
            ├── layouts/BaseLayout.astro
            ├── components/MessageCard.astro
            ├── scripts/api-client.js
            └── styles/custom.css
```

`compose.yaml` define los servicios `backend` y `frontend` en una red compartida. Solo publica el frontend en el puerto 80; el backend expone internamente el puerto 8000. No define un servicio PostgreSQL, por lo que esta estructura no decide si la base de datos debe ser otro contenedor o un servicio externo.

## Decisión

Se propone conservar un único repositorio, con las aplicaciones independientes dentro de `src/backend` y `src/frontend`, y mantener `compose.yaml` en la raíz como punto común de construcción y ejecución. Cada aplicación conserva sus propias dependencias, archivos de configuración y Dockerfile.

El frontend se comunica con el backend por HTTP mediante la ruta relativa `/api`. Nginx sirve los archivos estáticos y reenvía `/api` al servicio `backend` dentro de la red de Compose. El frontend no accede directamente a PostgreSQL ni importa módulos internos de Python.

En el backend, `app/main.py` crea FastAPI y contiene actualmente los endpoints `/health` y `/api`; `app/core/config.py` lee la configuración; `app/db/session.py` establece la conexión SQLAlchemy; `app/models/` define el modelo de prueba; y `app/repositories/consultas.py` agrupa consultas para ese modelo. Los directorios `api/v1/endpoints/`, `schemas/` y `services/` ya existen como espacios para separar rutas, contratos de datos y reglas de negocio cuando se implementen.

En el frontend, Astro organiza la ruta de inicio en `src/pages/`; `layouts/` comparte la estructura de página; `components/` contiene la tarjeta del mensaje; `scripts/api-client.js` solicita los datos a `/api`; `styles/` guarda estilos propios; y `public/` contiene recursos estáticos. `package.json` y `package-lock.json` registran las dependencias y permiten instalaciones reproducibles.

## Justificación

- **Una ubicación clara por aplicación:** `src/backend` y `src/frontend` hacen evidente qué archivos corresponden al servidor y cuáles a la interfaz, y permiten que cada Dockerfile tenga un contexto de construcción independiente.
- **Dependencias aisladas:** Python y FastAPI se administran desde el backend; Node y Astro, desde el frontend. Esto evita mezclar herramientas y facilita construir cada imagen por separado.
- **Composición centralizada:** `compose.yaml` en la raíz conecta ambos servicios en una red común y expresa qué puerto es público. El equipo puede cambiar cómo se construye una aplicación sin mover la orquestación.
- **Frontera por API:** la llamada relativa `/api` y el proxy de Nginx mantienen al backend y a PostgreSQL fuera del navegador. El frontend no depende de detalles internos de implementación ni de una IP fija.
- **Organización incremental del backend:** la configuración, conexión, modelos y consultas ya tienen ubicaciones identificables. Las carpetas `schemas`, `services` y `api/v1/endpoints` dan una ruta de crecimiento sin obligar a implementar capas vacías antes de necesitarlas.
- **Interfaz reutilizable:** separar páginas, layout, componentes, scripts y estilos permite evolucionar la interfaz sin concentrar toda la presentación y la comunicación en un solo archivo.
- **Adecuación al walking skeleton:** la página, la API y el proxy permiten verificar el recorrido navegador → Nginx → FastAPI → PostgreSQL de manera integrada.

## Alternativas consideradas

### Mezclar frontend y backend en una sola aplicación

Reduciría el número de carpetas, pero mezclaría tecnologías, dependencias y responsabilidades. También haría más difícil construir o reemplazar una capa de forma independiente.

### Mantener frontend y backend en repositorios separados

Ofrecería ciclos de versión independientes, pero aumentaría la coordinación necesaria para acordar cambios en la API y desplegar versiones compatibles. Para el MVP académico, un repositorio compartido con aplicaciones separadas es más simple.

### Permitir que el frontend consulte PostgreSQL directamente

Expondría credenciales y detalles de persistencia al navegador y duplicaría responsabilidades del backend. Se mantiene FastAPI como intermediario entre la interfaz y la base de datos.

## Consecuencias

### Positivas

- Frontend y backend pueden desarrollarse y construirse por separado dentro de un repositorio común.
- Compose integra ambas aplicaciones y Nginx presenta un único punto de entrada web.
- Las carpetas actuales proporcionan un lugar concreto para agregar funcionalidades gradualmente.
- La ruta relativa `/api` funciona sin fijar la IP de la máquina en el código del navegador.

### Costos y riesgos

- El equipo debe mantener el contrato de rutas, JSON y errores entre Astro y FastAPI.
- Los paquetes `schemas/` y `services/` del backend están vacíos; `api/v1/endpoints/` aún no contiene rutas. Los endpoints actuales están en `main.py`, por lo que si la API crece convendrá moverlos a routers versionados.
- `models/prueba.py` y `repositories/consultas.py` implementan un ejemplo `Item`, no los modelos ni operaciones completas de presupuestos, ingresos y gastos.
- `styles/custom.css` existe vacío; la personalización visual todavía está pendiente.
- La conexión a PostgreSQL y las variables necesarias dependen de la configuración de cada entorno; los secretos deben permanecer en archivos `.env` ignorados por Git.
- Compose no define PostgreSQL; el equipo debe documentar y acordar dónde se ejecuta la base para cada entorno.

## Referencias

- ADR-0001: PostgreSQL como base de datos del proyecto.
- ADR-0002: Python como lenguaje de desarrollo para el backend.
- ADR-0003: FastAPI como framework del backend.
- ADR-0004: Astro como framework del frontend.
- ADR-0005: Bootstrap como framework CSS propuesto para el frontend.
- `compose.yaml`: servicios, red y puertos.
- `src/backend/`: API, conexión de datos y consultas.
- `src/frontend/`: aplicación Astro, cliente HTTP, Nginx y recursos web.
