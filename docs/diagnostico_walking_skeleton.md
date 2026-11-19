# Diagnóstico y Resolución Técnica: Walking Skeleton End-to-End

**Proyecto:** UN-budget — Gestor de Finanzas  
**Fecha:** 19 de Noviembre de 2026  
**Objetivo:** Lograr el primer flujo funcional end-to-end (*Walking Skeleton*) del sistema:  
`Navegador (Astro + Bootstrap)` &rarr; `Reverse Proxy (Nginx :80)` &rarr; `Backend API (FastAPI :8000)` &rarr; `Base de Datos (PostgreSQL)` &rarr; Respuesta con mensaje `"Hola Mundo"`.

---

## 1. Arquitectura del Flujo Evaluado

El diseño desacoplado del Walking Skeleton comprende 4 capas esenciales:

```
[ Cliente Web / Navegador ]
            │  GET /api
            ▼
[ Reverse Proxy: Nginx (:80) ]
            │  proxy_pass http://backend:8000
            ▼
[ Backend API: FastAPI (:8000) ]
            │  SQLAlchemy (SELECT item FROM item LIMIT 1)
            ▼
[ Base de Datos: PostgreSQL (:5432) ]
```

Cuando el flujo opera con normalidad:
1. El cliente web consulta la ruta relativa `/api`.
2. Nginx intercepta `/api` y lo redirige internamente a la red privada de Docker hacia `http://backend:8000`.
3. FastAPI resuelve el endpoint consultando la tabla `item` mediante SQLAlchemy y el repositorio correspondiente.
4. PostgreSQL retorna la fila persistida con el texto `"Hola Mundo"`.
5. El cliente web actualiza la interfaz marcando todas las capas en verde con la insignia **"Cadena Completa"**.

---

## 2. Diagnóstico de Conectividad con la Base de Datos en Cloud (Google Cloud)

### 2.1. Configuración Suministrada
* **Host:** `34.68.135.148`
* **Puerto:** `5432`
* **Usuario:** `g2_team_5_user`
* **Base de Datos:** `g2-team-5-db`

### 2.2. Pruebas de Red y Transporte Realizadas
Se realizaron pruebas directas de conectividad desde el entorno local hacia el host remoto:

1. **Capa de Red (ICMP / Ping):**
   ```text
   Test-Connection -ComputerName 34.68.135.148
   Resultado: Éxito (RTT medio: 104 ms - 152 ms). PingSucceeded: True.
   ```
   *Conclusión:* La máquina virtual en Google Cloud está encendida y accesible a través de internet.

2. **Capa de Transporte (TCP Socket a puerto 5432):**
   ```text
   Test-NetConnection 34.68.135.148 -Port 5432
   Resultado: TCP connect to (34.68.135.148 : 5432) failed. TcpTestSucceeded: False.
   
   System.Net.Sockets.SocketException (10061):
   "No connection could be made because the target machine actively refused it 34.68.135.148:5432" (WSAECONNREFUSED)
   ```

### 2.3. Causa Raíz Técnica del Fallo en Cloud
El código de error `WSAECONNREFUSED` (10061) confirma que el paquete TCP SYN llegó al servidor en Google Cloud, pero el sistema operativo remoto devolvió inmediatamente un paquete **TCP RST (Rechazo Activo)**.

Esto ocurre por una de las siguientes tres causas en el servidor remoto:
1. **El servicio de PostgreSQL está detenido:** El daemon no se encuentra en ejecución en el servidor (`systemctl status postgresql` caído).
2. **PostgreSQL no está escuchando en interfaces públicas:** En `postgresql.conf`, la directiva `listen_addresses` está configurada como `'localhost'` o `127.0.0.1` en lugar de `'*'`.
3. **Restricción de Firewall / Redes Autorizadas de GCP:** La regla de firewall de Compute Engine o la lista de "Redes autorizadas" de Google Cloud SQL no incluye la IP pública del cliente (o `0.0.0.0/0`), rechazando paquetes en el puerto 5432.

> **Conclusión sobre Cloud:** Dado que el servidor remoto rechaza activamente las conexiones, ningún ajuste en el cliente local puede forzar al servidor a aceptar la conexión. La solución de este punto depende de la administración del servidor en Google Cloud.

---

## 3. Auditoría de Fallos en el Proyecto Local

Durante la revisión del código y la configuración se detectaron los siguientes errores:

### Fallo 1: Conflicto de precedencia en `compose.yaml` sobre `.env`
* **Descripción:** En Docker Compose, los valores declarados en `environment:` sobreescriben a los declarados en `env_file:`.
* **Detalle:** `compose.yaml` tenía fijado `POSTGRES_HOST: db` en la sección `environment:` del servicio `backend`. Esto provocaba que cualquier intento de apuntar a la IP de Cloud en `src/backend/.env` fuera ignorado silenciosamente por Docker Compose.

### Fallo 2: Falta de archivo `.env` en la raíz del proyecto
* **Descripción:** Compose resuelve variables interpoladas como `${POSTGRES_USER:-postgres}` leyendo el `.env` del directorio de trabajo actual (la raíz). Al estar el archivo ubicado únicamente en `src/backend/.env`, Compose siempre tomaba los valores por defecto locales para el servicio `db`.

### Fallo 3: Excepción de ejecución en `src/backend/app/main.py` (`NameError: name 'Base' is not defined`)
* **Descripción:** En la función `lifespan` de FastAPI, al comprobarse que la base de datos estaba disponible, se invocaba:
  ```python
  Base.metadata.create_all(bind=engine)
  ```
  Sin embargo, el objeto `Base` **no estaba importado** en `main.py`.
* **Impacto:** Si la base de datos local o remota conectaba exitosamente, el backend fallaba inmediatamente al iniciar con `NameError`.

### Fallo 4: Inconsistencia en la configuración de la Base de Datos (`config.py`)
* **Descripción:** La clase `Settings` (`pydantic_settings`) genera la URL dinámicamente mediante `URL.create(...)` leyendo `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD` y `POSTGRES_DB`.
* **Detalle:** En `compose.yaml` se inyectaba una variable `DATABASE_URL` fija con `@db:5432`, la cual no era leída por la aplicación y generaba incongruencias de configuración.

### Fallo 5: Código HTML huérfano en `src/frontend/src/pages/index.astro`
* **Descripción:** Al final del archivo `index.astro`, tras el script de cliente, existía un bloque incompleto `<html lang="en">...</html>` redundante, puesto que el diseño ya utiliza el componente estructural `<BaseLayout>`.

---

## 4. Acciones Implementadas (Plan B: PostgreSQL Local)

Para garantizar la entrega funcional del Walking Skeleton sin depender del servicio caído en Cloud, se ejecutaron las siguientes acciones:

1. **Corrección de `src/backend/app/main.py`:**
   * Se importó `from app.models.prueba import Base`.
   * El ciclo de vida de FastAPI ahora crea las tablas si no existen y gestiona la desconexión limpia del pool de conexiones sin errores.

2. **Reestructuración de `compose.yaml`:**
   * Se parametrizaron las variables del backend: `${POSTGRES_HOST:-db}`, `${POSTGRES_PORT:-5432}`, `${POSTGRES_USER:-postgres}`, etc.
   * Se configuró el healthcheck oficial de PostgreSQL (`pg_isready`) y la dependencia `depends_on: db: condition: service_healthy` para asegurar el orden correcto de arranque.

3. **Estandarización de Variables de Entorno:**
   * Se creó el archivo `.env` en la raíz del proyecto para Docker Compose.
   * Se sincronizó `src/backend/.env` con la configuración del servicio local.
   * Se respaldaron intactas las credenciales del Cloud en `src/backend/.env.cloud` para cuando el profesor reactive el servicio remoto.

4. **Idempotencia en el script SQL de inicialización (`src/db/init.sql`):**
   * Se ajustó el script para insertar `'Hola Mundo'` únicamente si la tabla `item` se encuentra vacía:
     ```sql
     CREATE TABLE IF NOT EXISTS item (
         id SERIAL PRIMARY KEY,
         item VARCHAR(255) NOT NULL,
         fecha DATE NOT NULL DEFAULT CURRENT_DATE
     );

     INSERT INTO item (item)
     SELECT 'Hola Mundo'
     WHERE NOT EXISTS (SELECT 1 FROM item);
     ```

5. **Depuración del Frontend (`index.astro`):**
   * Se eliminó el bloque HTML huérfano al final del archivo.

---

## 5. Pruebas y Verificación del Flujo End-to-End

### 5.1. Estado de los Contenedores
```text
CONTAINER ID   IMAGE                STATUS                   PORTS                NAMES
0d599659bb00   un-budget-backend    Up                       8000/tcp             un-budget-backend-1
e9a9a8285097   postgres:17-alpine   Up 7 seconds (healthy)   5432/tcp             un-budget-db-1
e629dd58101f   un-budget-frontend   Up                       0.0.0.0:80->80/tcp   un-budget-frontend-1
```

### 5.2. Validación de la Petición HTTP (`Reverse Proxy -> Backend -> DB`)
Petición ejecutada contra el puerto 80 expuesto por Nginx:
```http
GET http://localhost/api HTTP/1.1

HTTP/1.1 200 OK
Server: nginx/1.30.7
Content-Type: application/json

{"mensaje":"Hola Mundo"}
```

### 5.3. Validación en Interfaz de Usuario
Al acceder a `http://localhost`:
* **1. Navegador (Astro + Bootstrap):** `Activo`
* **2. Reverse Proxy (Nginx :80):** `OK (Proxy)`
* **3. Backend API (FastAPI):** `OK (200)`
* **4. Base de Datos (PostgreSQL):** `Conectada`
* **Insignia General:** `Cadena Completa`
* **Dato recuperado:** `Hola Mundo`

---

## 6. Procedimiento para Alternar al Cloud en el Futuro

Una vez que el profesor/administrador confirme que el puerto 5432 está escuchando en `34.68.135.148`:
1. Copiar los valores de `src/backend/.env.cloud` en `.env` y `src/backend/.env`.
2. En `compose.yaml`, comentar la sección del servicio `db` y la directiva `depends_on: db` en el backend.
3. Reiniciar los contenedores:
   ```bash
   docker compose down
   docker compose up -d
   ```

---

## 7. Resumen Ejecutivo Rápido

* **¿Qué pasó?**
  El Walking Skeleton no lograba completar el flujo end-to-end porque las peticiones a la base de datos en Google Cloud eran rechazadas, y al intentar levantar la arquitectura en Docker, el sistema presentaba conflictos entre archivos `.env`, configuraciones rígidas en `compose.yaml` y un error de importación en el backend.

* **¿Por qué pasó?**
  1. **En Cloud:** El servidor remoto `34.68.135.148` responde a Ping pero rechaza activamente el puerto `5432` (`WSAECONNREFUSED`), debido a que el servicio PostgreSQL remoto está apagado o restringido por firewall.
  2. **En Local:** En `compose.yaml` la directiva `environment:` anulaba el `.env`; faltaba un `.env` en la raíz; y en `main.py` faltaba importar la clase `Base`, lo que provocaba un `NameError` al conectar la base de datos.

* **¿Qué acciones se tomaron?**
  1. Se comprobó y documentó técnicamente el rechazo de conexión del servidor Cloud.
  2. Se respaldaron las credenciales Cloud en `src/backend/.env.cloud`.
  3. Se corrigió el bug de `Base` en `main.py` y se limpió el frontend en `index.astro`.
  4. Se dinamizó `compose.yaml` y se sincronizaron los archivos `.env` (raíz y backend).
  5. Se implementó el **Plan B**: levantar PostgreSQL local mediante Docker Compose con inicialización SQL automática.
  6. Se validó con éxito el recorrido completo de extremo a extremo, obteniendo respuesta `200 OK` con el mensaje `"Hola Mundo"` servido desde PostgreSQL a través de Nginx y visualizado en Astro.
