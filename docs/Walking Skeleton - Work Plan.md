# Walking skeleton Hola Mundo: frontend, backend y PostgreSQL en GCP

Nov 14, 2026 · @Tovar GOAT

Un walking skeleton es la versión más pequeña del sistema que ya cruza todas las capas de punta a punta. El "Hola Mundo" no debe estar escrito en el frontend. Debe salir de PostgreSQL, pasar por el backend y mostrarse en el navegador. Así cada capa, cada conexión entre ellas y la ruta de despliegue quedan probadas desde el principio.

## Reparto del trabajo entre cinco personas

El trabajo se divide por capa: una persona por cada contenedor, una para la infraestructura en GCP y una que define los acuerdos entre capas e integra. Cada fila apunta a los pasos numerados de este doc.

| Rol | Responsable | Fases y pasos | Entregable | Necesita de |
| --- | --- | --- | --- | --- |
| Integración y orquestación (líder técnico) | Samuel Benitez. | Fase 0, Fase 1 (pasos 1–3), Fase 5 (pasos 18–23), Fase 6 (pasos 24–25) | Repositorio con estructura, contrato entre capas, archivo Compose, plantilla de `.env` y prueba local de punta a punta | Las imágenes de las personas 2, 3 y 4 |
| Base de datos | Miguel Guativa. | Fase 2 (pasos 4–8) | Servicio PostgreSQL con script de inicialización, fila "Hola Mundo", volumen y healthcheck | Nombres de variables del contrato |
| Backend | David Sainea. | Fase 3 (pasos 9–13) | API con endpoint de salud y endpoint `/api` que lee la tabla, más su Dockerfile | Esquema de la tabla (persona 2) y contrato |
| Frontend y proxy | Joger Muñoz. | Fase 4 (pasos 14–17) | Página que muestra el mensaje, Dockerfile multi-etapa y Nginx con proxy a `/api` | Formato del JSON del contrato |
| Infraestructura y despliegue (GCP) | Kevin Flórez. | Fase 7 (pasos 26–30), Fase 8 (paso 31), Fase 9 (pasos 32–37), Fase 10 (paso 38) | VM con firewall, IP estática y Docker; despliegue verificado y redespliegue automatizado | Compose funcionando en local (persona 1) |

El README (paso 39) lo escriben entre todos: cada persona documenta su capa y la persona 1 lo une.

**El contrato entre capas** es lo primero que fija la persona 1, para que nadie se bloquee esperando a otro: nombres de los servicios en Compose, nombres de las variables de entorno, puertos internos, la ruta `/api` y la forma exacta del JSON del mensaje.

## Orden de trabajo del equipo

Con el contrato fijado al inicio, cuatro de las cinco personas trabajan en paralelo y el equipo solo se sincroniza en dos puntos de integración.

1. **Arranque (todo el equipo, una reunión corta).** La persona 1 presenta la estructura del repositorio y el contrato entre capas. Todos lo revisan y lo aprueban antes de escribir nada.
2. **Trabajo en paralelo.**
   - Persona 2: base de datos con su fila inicial.
   - Persona 3: backend. Mientras la base no esté lista, puede probar contra un PostgreSQL local con el mismo esquema.
   - Persona 4: frontend y Nginx. Mientras el backend no esté listo, puede simular la respuesta de `/api` con el JSON del contrato.
   - Persona 5: crea la VM, el firewall, la IP estática e instala Docker. Esto no depende del código.
   - Persona 1: escribe el archivo Compose y la plantilla de `.env`.
3. **Primera integración: en local.** La persona 1 junta las tres imágenes con Compose y dirige la prueba de humo (paso 25) con las personas 2, 3 y 4 presentes para corregir en el momento.
4. **Segunda integración: en la VM.** La persona 5 despliega, verifica desde fuera y reinicia la VM (pasos 32–37). La persona 1 la acompaña para validar la definición de terminado.
5. **Cierre.** La persona 5 automatiza el redespliegue (paso 38), cada persona completa su parte del README y el equipo revisa juntos la definición de terminado.

Para que el trabajo en paralelo no choque: una rama por persona, cambios integrados con pull requests revisados por la persona 1, y cualquier cambio al contrato se avisa a todo el equipo antes de aplicarlo.

## Fase 0: El flujo que vas a probar

Navegador → (puerto 80) → contenedor del frontend / proxy → (red interna de Docker) → contenedor del backend → (red interna) → contenedor de PostgreSQL

Desde fuera de la VM solo se abre el puerto 80 (y el 22 para SSH). El backend y la base de datos no se exponen al exterior.

## Fase 1: Organizar el repositorio

1. **Un solo repositorio** con tres carpetas: frontend, backend y base de datos. En la raíz van el archivo de orquestación (Docker Compose), un archivo de variables de entorno de ejemplo y un README.
2. **Control de versiones desde el día uno.** El despliegue en la VM saldrá de este repositorio o de imágenes construidas a partir de él.
3. **Un `.gitignore` y un `.dockerignore`** para que no entren secretos, dependencias instaladas ni archivos de compilación en las imágenes.

## Fase 2: La capa de datos (PostgreSQL)

4. **Usa la imagen oficial de PostgreSQL** con una versión fija (no "latest"). Así cualquier entorno levanta exactamente lo mismo.
5. **Prepara un script de inicialización** que la imagen ejecute en el primer arranque. Debe crear una tabla mínima (por ejemplo, "mensajes") e insertar una fila con el texto "Hola Mundo". Esa fila es la que el navegador debe mostrar al final.
6. **Configura usuario, contraseña y nombre de la base con variables de entorno.** Nunca las escribas a mano dentro de la imagen.
7. **Monta un volumen con nombre** para los datos, así sobreviven si recreas el contenedor. Ojo: el script de inicialización solo corre cuando el volumen está vacío. Si cambias el script, tienes que borrar el volumen.
8. **Define un healthcheck** que confirme que PostgreSQL ya acepta conexiones, no solo que el proceso arrancó.

## Fase 3: El backend

9. **Elige un framework ligero** del lenguaje que domines (Node/Express, Python/FastAPI, Java/Spring Boot, Go, etc.).
10. **Crea dos endpoints:**
    - Uno de **salud**, que responda si el servicio está vivo y si llega a la base de datos.
    - Uno de **negocio** (por ejemplo, bajo el prefijo `/api`) que consulte la tabla y devuelva el mensaje en JSON.
11. **Lee los datos de conexión de variables de entorno.** El host de la base de datos debe ser el **nombre del servicio en Compose**, no "localhost". Dentro de un contenedor, "localhost" es el propio contenedor. Este es el error más común en este tipo de ejercicio.
12. **Agrega reintentos al conectar.** Aunque haya healthchecks, el backend puede arrancar unos segundos antes de que la base esté lista.
13. **Escribe el Dockerfile del backend:**
    - Imagen base pequeña y con versión fija.
    - Si el lenguaje se compila, usa multi-etapa: una etapa compila y otra solo ejecuta.
    - Copia primero los archivos de dependencias y después el código, para aprovechar la caché de capas.
    - Ejecuta la aplicación con un usuario sin privilegios.
    - Declara el puerto interno.

## Fase 4: El frontend

14. **Haz una página mínima** (React, Vue, Angular o HTML con JavaScript puro). Al cargar, debe pedir el mensaje al endpoint del backend y mostrarlo. Muestra también un texto de error visible si la llamada falla, para que un fallo no se confunda con una página vacía.
15. **Usa rutas relativas para llamar a la API** (por ejemplo, "/api/..."), no una URL absoluta con IP. Así el mismo build funciona en local y en la VM, y evitas problemas de CORS.
16. **Escribe un Dockerfile multi-etapa:**
    - Una etapa con Node instala dependencias y genera los archivos estáticos.
    - Otra etapa con Nginx sirve esos estáticos.
17. **Configura Nginx como proxy inverso.** Que sirva el frontend en "/" y reenvíe todo lo que empiece por "/api" al servicio del backend, usando su nombre en la red de Compose. Así el navegador habla con un solo origen y el backend queda oculto.

> Si tu framework mete variables en tiempo de compilación (por ejemplo, la URL de la API), recuerda que quedan fijas dentro de la imagen. Las rutas relativas del paso 15 evitan este problema.

## Fase 5: Orquestar con Docker Compose

18. **Declara los tres servicios** (db, backend, frontend) en un único archivo Compose.
19. **Crea una red interna compartida.** Docker resuelve los nombres de servicio como hostnames dentro de ella.
20. **Publica solo el puerto 80 del frontend** hacia el host. Ni el backend ni PostgreSQL publican puertos.
21. **Define dependencias con condición de salud.** El backend espera a que la base esté sana y el frontend espera al backend.
22. **Saca las variables a un archivo `.env`.** Versiona solo la plantilla de ejemplo, nunca el archivo real con contraseñas.
23. **Pon una política de reinicio** ("unless-stopped" o similar) para que los servicios se levanten solos si la VM se reinicia.

## Fase 6: Validar en local

24. **Levanta todo con Compose en tu máquina** y comprueba, capa por capa:
    - La base de datos aparece sana y la tabla tiene la fila.
    - El endpoint de salud del backend responde. Pruébalo desde dentro de la red, porque desde fuera no está expuesto.
    - En el navegador, "localhost" muestra "Hola Mundo" traído de la base.
25. **Haz la prueba de humo de la cadena completa:** cambia el texto de la fila en PostgreSQL y recarga. Si el cambio aparece, las tres capas están conectadas de verdad.

## Fase 7: Preparar la VM en Google Cloud

26. **Crea o revisa la instancia de Compute Engine.** Para este ejercicio basta un tipo pequeño (e2-small o e2-medium), con una imagen de Ubuntu LTS o Debian y al menos 20 GB de disco.
27. **Revisa las reglas de firewall de la VPC.** Deben permitir HTTP (80) y SSH (22). Lo más sencillo es marcar la casilla "Permitir tráfico HTTP" en la instancia, que le asigna la etiqueta de red correspondiente. Si luego usas HTTPS, abre también el 443.
28. **Asigna una IP externa estática** (reserva una), para que la dirección no cambie al reiniciar.
29. **Entra por SSH** (desde la consola, con gcloud o con tu llave) e **instala Docker Engine y el plugin de Compose** desde el repositorio oficial de Docker, no el paquete viejo de la distribución.
30. **Agrega tu usuario al grupo de Docker** y vuelve a iniciar sesión, para no usar sudo en cada comando. Verifica que el servicio de Docker arranque solo con el sistema.

## Fase 8: Llevar el proyecto a la VM

Tienes dos caminos. Elige uno:

- **Opción A (la más simple): construir en la VM.** Clonas el repositorio en la VM (por HTTPS o con una deploy key de solo lectura) y Compose construye las imágenes ahí mismo. Es ideal para un walking skeleton.
- **Opción B (la más cercana a producción): usar un registro.** Construyes las imágenes en tu máquina o en un pipeline de CI, las etiquetas con una versión o el hash del commit, las subes a Artifact Registry de Google y en la VM solo las descargas. Para eso, la cuenta de servicio de la VM necesita permiso de lectura sobre el registro y Docker debe estar autenticado contra él.

> Si construyes en un Mac con Apple Silicon (ARM) y la VM es x86, compila las imágenes para la plataforma amd64. Si no, los contenedores fallarán al arrancar con un error de formato de ejecutable.

31. **Crea el `.env` real directamente en la VM**, con contraseñas fuertes y permisos de lectura solo para tu usuario. No lo subas al repositorio.

## Fase 9: Desplegar y verificar en la VM

32. **Levanta los servicios en segundo plano** con Compose y revisa que los tres estén "running" y los healthchecks en "healthy".
33. **Revisa los logs de cada servicio.** Confirma que el backend conectó a la base y que Nginx no muestra errores de upstream.
34. **Verifica desde dentro de la VM** que el puerto 80 responde con la página y que la ruta "/api" devuelve el JSON.
35. **Verifica desde fuera:** abre la IP externa de la VM en el navegador y debe aparecer "Hola Mundo". Si no carga, revisa en este orden: regla de firewall y etiqueta de red, puerto publicado en Compose, logs de Nginx.
36. **Repite la prueba de humo** (cambiar el texto en la base y recargar) para confirmar la cadena completa en el entorno real.
37. **Reinicia la VM** y comprueba que todo vuelve a levantarse solo.

## Fase 10: Cerrar el incremento

38. **Automatiza el redespliegue mínimo.** Puede ser un script en la VM que haga pull, rebuild y up, o un pipeline (por ejemplo, GitHub Actions) que construya, suba a Artifact Registry y despliegue por SSH. Si el despliegue es repetible, el esqueleto camina.
39. **Documenta en el README** cómo levantarlo en local, cómo desplegarlo, qué variables hacen falta y cómo verificar cada capa.

### Definición de terminado

- [ ] El texto mostrado viene de PostgreSQL, no del frontend.
- [ ] Los tres servicios corren en contenedores orquestados por Compose.
- [ ] Solo el puerto 80 está expuesto. La base y el backend son internos.
- [ ] Los secretos están en un `.env` fuera del control de versiones.
- [ ] Los datos persisten en un volumen.
- [ ] El sistema sobrevive a un reinicio de la VM.
- [ ] El despliegue se repite con uno o dos comandos documentados.

### Errores típicos a evitar

- Usar "localhost" para comunicar contenedores entre sí.
- Exponer PostgreSQL a internet.
- Olvidar la regla de firewall o la etiqueta de red de la VM.
- Construir imágenes para la arquitectura equivocada (ARM vs x86).
- Esperar que el script de inicialización vuelva a correr con un volumen que ya tiene datos.

## Siguientes incrementos

Con esto validado, los siguientes incrementos (HTTPS con un dominio, migraciones de base de datos, CI/CD completo, monitoreo) se construyen sobre una base que ya sabes que funciona de punta a punta.
