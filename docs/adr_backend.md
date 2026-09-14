# ADR-000X: Selección del framework de backend para el sistema de finanzas personales

Autores:
Autores:
 - @sabenitez-unal
 - @mguativa
 - @KevinDFH
 - @desainea
 - @JogerUN
Fecha: 2026-09-13

## Estado

Propuesto

## Contexto

Nosotros estamos considerando desarrollar un sistema de finanzas personales que permita registrar ingresos, gastos, cuentas, medios de pago y movimientos programados.

con funciones como:
- Consultar balances.
- Mostrar gráficas.
- Calcular intereses.
- Organizar los movimientos.
- Manejar información de los usuarios.
- Mantener los datos guardados de forma segura.

El frontend estaría separado del backend y podría desarrollarse con HTML, Tailwind CSS y JavaScript.

Para el backend estaríamos considerando utilizar Python, debido a que podría facilitarnos el desarrollo y permitirnos trabajar con diferentes herramientas. También tenenemos como opcion principal ahora PostgreSQL.
La solución debería permitirnos trabajar con una estructura organizada mantener el código con facilidad y tener la posibilidad de agregar nuevas funciones más adelante y tener que revisar aspectos como:

- Seguridad de la información.
- Manejo de usuarios y autenticación.
- Rendimiento.
- Conexión con la base de datos.
- Documentación de la API.
- Facilidad para realizar pruebas.

La necesidad de tomar esta decisión se relaciona con la elección de una tecnología que nos permita construir el backend y conectar el frontend con la base de datos.

## Decisión

Nosotros proponemos utilizar FastAPI por ahora, para desarrollar el backend y crear una API REST para el sistema de finanzas personales.

También estaríamos considerando utilizar SQLAlchemy para trabajar con la base de dato, esta propuesta todavía tendría que validarse mediante pruebas de desarrollo, conexión con la base de datos y revisión de los requisitos del sistema.

## Alternativas consideradas

### Django con Django REST Framework

También podríamos utilizar Django junto con Django REST Framework.

Esta alternativa podría ofrecernos muchas funciones listas para usar, como administración de usuarios, manejo de bases de datos y estructura de proyecto junto sus baterias como el ORM.

Sin embargo, podría ser una opción más grande de lo que necesitaríamos inicialmente y tendríamos que aprender más partes del framewor, es decir una curva de aprendizaje mayor y menos flexibildiad respecto a que tecnologias usar.

### Flask

Flask podría permitirnos crear un backend sencillo y flexible.

El problema sería que tendríamos que agregar y configurar más herramientas por nuestra cuenta para manejar validaciones, documentación, autenticación y estructura del proyecto, no dandonos la suficiente ventaja sobre una FastAPI para ser considerada

### Sanic

Sanic podría ser otra opción para crear APIs con Python y trabajar con operaciones asíncronas pero podría tener menos recursos y ejemplos disponibles para nuestro caso de uso en comparación con otras alternativas.

### Node.js con Express o NestJS

También podríamos utilizar JavaScript o TypeScript en el backend.
Esta opción podría ser útil si quisiéramos manejar el frontend y el backend con tecnologías similares. Sin embargo, nosotros estaríamos considerando Python para el backend, por lo que utilizar Node.js podría implicar cambiar parte del enfoque tecnológico.

### Comparación general

### Comparación general

#### FastAPI

**Posibles ventajas:**

- Documentación automática.
- Validación de datos.
- Estructura para crear APIs.

**Posibles dificultades:**

- Tendríamos que revisar la configuración de autenticación.
- Tendríamos que configurar la conexión con la base de datos.

#### Django + DRF

**Posibles ventajas:**

- Muchas funciones incluidas.
- Estructura completa para desarrollar el backend.

**Posibles dificultades:**

- Podría ser más complejo de lo necesario para nuestro proyecto.

#### Flask

**Posibles ventajas:**

- Es flexible.
- Podría ser sencillo para comenzar.

**Posibles dificultades:**

- Tendríamos que configurar más herramientas manualmente.

#### Sanic

**Posibles ventajas:**

- Tiene un enfoque asíncrono.
- Podría ofrecer un buen rendimiento.

**Posibles dificultades:**

- Podría tener menos recursos disponibles para nuestro caso.

#### Node.js + Express/NestJS

**Posibles ventajas:**

- Permitiría utilizar JavaScript o TypeScript en el backend.

**Posibles dificultades:**

- Cambiaría el enfoque tecnológico que estaríamos considerando.

## Consecuencias

### Posibles consecuencias positivas

- Podríamos desarrollar una API organizada para conectar el frontend con el backend.
- Podríamos aprovechar el uso de Python.
- La documentación automática podría facilitarnos las pruebas y el entendimiento de los endpoints.
- La validación de datos podría ayudarnos a reducir errores al registrar ingresos y gastos.
- Podríamos separar mejor las responsabilidades del sistema.
- Podríamos agregar nuevas funciones en el futuro sin tener que cambiar toda la estructura.
- Podríamos integrar herramientas diversas segun nuestras necesidades.
- Podríamos realizar pruebas de forma más ordenada.

### Posibles consecuencias negativas

- Tendríamos que aprender y configurar FastAPI.
- Tendríamos que definir una estructura clara para las carpetas, rutas, servicios y modelos.
- La autenticación y autorización no quedarían completamente resueltas solo por utilizar FastAPI.
- Tendríamos que revisar la seguridad de los datos y la protección de las rutas.
- Podríamos necesitar más tiempo para configurar la conexión con la base de datos.
- El equipo tendría que familiarizarse con herramientas como SQLAlchemy y analizar nuestras opciones.
- La decisión podría cambiar si durante las pruebas encontramos problemas de rendimiento, mantenimiento o compatibilidad.
- Tendríamos que revisar si PostgreSQL se adapta mejor a las necesidades reales del sistema.
- Perdemos una estructura completa como la que tiene Django

### Medidas que podríamos tomar

Para reducir las posibles dificultades, nosotros podríamos:

- Definir una estructura de carpetas antes de comenzar el desarrollo.
- Crear pruebas para los endpoints principales.
- Revisar la autenticación y autorización.
- Utilizar variables de entorno para manejar información sensible.
- Documentar las decisiones técnicas.
- Probar la conexión con la base de datos.
- Revisar el rendimiento con datos de prueba.
- Utilizar Git para llevar un control de los cambios.
- Considerar Docker para facilitar la configuración del entorno.
- Validar la propuesta antes de marcar el ADR como aceptado.
