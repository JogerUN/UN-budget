# ADR-0001: PostgreSQL como database del stack del proyecto.

<!--
Nombra el archivo con el número consecutivo y un slug corto, por ejemplo:
docs/adr/0001-usar-postgresql-como-base-de-datos-principal.md
Los ADR se numeran en orden y NUNCA se editan después de aceptados para
cambiar la decisión en sí (sí puedes corregir errores de redacción). Si la
decisión cambia, escribes un ADR nuevo y marcas este como reemplazado
(ver "Estado"). Así el repositorio queda como una bitácora histórica de
por qué el sistema es como es.
-->

Autores:

- @sabenitez-unal
Fecha: 2026-09-14

## Estado

<!--
Uno de: Propuesto | Aceptado | Rechazado | Reemplazado por ADR-000Y | Obsoleto
Un ADR "Propuesto" está en discusión. Una vez el equipo decide, pasa a
"Aceptado" (o "Rechazado" si se descarta la propuesta) y ya no se
modifica su contenido de fondo.
-->

Propuesto

## Contexto

<!--
¿Qué problema técnico, restricción o fuerza nos obliga a tomar esta
decisión ahora? Describe la situación de forma neutral y objetiva —
todavía no es el lugar para argumentar a favor de una opción.
Ejemplos de fuerzas en juego: requisitos no funcionales (rendimiento,
seguridad, escalabilidad), restricciones de equipo o de tiempo,
deuda técnica existente, compatibilidad con sistemas ya construidos.
-->

El aplicativo web propuesto para nuestro gestor de finanzar personales requiere de una base de datos
que garantice integridad de los datos -ACID- puesto que trabajaremos con valores contables. Además de ello,
debe permitir precisión numérica en los datos almacenados y que esta base de datos tenga alta facilidad de integración.

Adicionalmente, al ser un proyecto que utilizará el lenguaje de programación Python para su backend y lógica de negocio con la asistencia de la librería FastAPI, la base de datos debe contar, idealmente, con una integración nativa con este framework de APIs REST, permitiendo trabajar con funciones asíncronas de ser necesario, además de poderse manipular mediante ORMs como SQLAlchemy fácilmente -librería que tiene perfecta sincronía con FastAPI-.

Por último, trabajar con un administrador de bases de datos SQL permitirá establecer relaciones entre entidades dentro de la data del programa, clave para manejos de presupuestos, tracking de ingresos y gastos, además de potenciales funcionalidades de Investor Advisor o de integración con chatbots potenciados por IA. Las relaciones entre datos de distintas entidades están claras, lo que motiva a utilizar, como bien se mencionó, bases de datos relacionales.

## Decisión

<!--
Qué vamos a hacer, en una o dos frases claras y en tiempo presente
("Vamos a usar X para Y"). Esta es la sección más corta del documento:
un ADR no es un RFC, no necesita convencer a nadie aquí — la
justificación ya quedó en "Contexto" y las alternativas descartadas
van abajo.
-->

**PostgreSQL** será utilizado como administrador de bases de datos dentro del aplicativo web Un-Budget.

## Alternativas consideradas

<!--
Qué otras opciones se evaluaron y por qué se descartaron. No hace
falta un análisis exhaustivo, basta con dejar constancia de que se
consideraron y el motivo del descarte (costo, madurez, curva de
aprendizaje, no cumple un requisito, etc.).
-->

Se consideró una alternativa adicional: **MySQL**
MySQL es una base de datos SQL muy utilizada en la industria gracias a su simplicidad en manejo, herramientas y sintaxis, pero debido a su integración no nativa con FastAPI en cuanto a programación asíncrona se refiere -es necesario utilizar librerías de terceros que no están totalmente integradas con esta última-, a que no maneja tipos de datos con precisión numérica específica como ENUM o DECIMAL y a que Postgres permite mayor escalabilidad, no fue seleccionada.

## Consecuencias

<!--
¿Qué se vuelve más fácil o más difícil después de esta decisión?
Incluye efectos positivos y negativos por igual — un ADR honesto
también documenta el costo que se está aceptando (deuda técnica
introducida, dependencia nueva, curva de aprendizaje del equipo).
-->

Utilizar PostgreSQL implica una curva de aprendizaje para el equipo un poco más pronunciada, puesto que tiene reglas claras de sintaxis, manejo de usuarios, esquemás, etc. Sin embargo se opta por su escalibilidad y uso reconocido en el sector tecnológico.

### Diferencia con un RFC (referencia rápida)

<!--
Elimina esta sección en el ADR final; queda aquí solo como recordatorio
para quien usa la plantilla.
- Un RFC se escribe ANTES de decidir, para abrir discusión y llegar a
  consenso; es un documento "vivo" mientras dura la deliberación.
- Un ADR registra una decisión YA tomada (o que se está formalizando);
  una vez aceptado, es casi inmutable — si cambia, se escribe un ADR
  nuevo que reemplaza al anterior, no se edita el viejo.
- El RFC suele ser más largo (motivación, métricas, riesgos, preguntas
  abiertas); el ADR es deliberadamente corto: Contexto, Decisión,
  Consecuencias.
- En equipos que usan ambos: el RFC es el proceso de deliberación,
  y al cerrarlo se destila un ADR corto como registro histórico de lo
  que finalmente se decidió.
-->
