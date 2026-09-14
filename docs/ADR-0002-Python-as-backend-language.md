# ADR-0002: Python como lenguage de desarrollo para el backend.
 
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
 - @JogerUN
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
 
Para el proyecto UN-Budget, plataforma destinada a la gestión, auditoría y seguimiento de las finanzas personales de los usuarios, es necesario seleccionar un lenguaje de programación para el desarrollo del backend.

La decisión estará condicionada por los siguientes factores técnicos y de proyecto:

  - Team learning curve
  - Security ecosistem
  - Database and SQL support
  - Performace
  - API integrations
  - Development Speed (MVP)

El proyecto tiene un propósito académico orientado al aprendizaje de buenas prácticas de ingeniería de software y debe producir un MVP funcional dentro de un semestre académico. A nivel de producto, el sistema gestionará información financiera personal, por lo que requiere considerar aspectos como seguridad, integridad y trazabilidad de los datos, rendimiento y mantenibilidad.

Tambien se tomaron en cuenta temas de seguridad como:
  - Password hashing
  - Session management
  - Input validation
  - SQL injection protection
  - Authorization
  - Secrets management

Por lo tanto, el lenguaje seleccionado deberá ser compatible con las necesidades actuales del MVP y permitir la evolución posterior del sistema hacia funcionalidades más avanzadas, como integraciones externas y servicios de inteligencia artificial. 

Tambien se tomo en cuenta el estado actual del del recurso humano que llevara a acabo el proyecto, buscando resolver preguntas como:
  - Que lenguages de programamcion para el Backend son mas familiares para el equipo?
  - Que tanto tiempo puede disponer el equipo en aprender el fundamento del lenguage para el backend?
  - Con cuales lenguages para ya se cuenta con experiencia para el desarrollo del backend?

## Decisión
 
<!--
Qué vamos a hacer, en una o dos frases claras y en tiempo presente
("Vamos a usar X para Y"). Esta es la sección más corta del documento:
un ADR no es un RFC, no necesita convencer a nadie aquí — la
justificación ya quedó en "Contexto" y las alternativas descartadas
van abajo.
-->

Para el presente proyecto se propone usar **Python** como lenguage de programacion para el desarrollo del backend de UN-Budget.
 
## Alternativas consideradas
 
<!--
Qué otras opciones se evaluaron y por qué se descartaron. No hace
falta un análisis exhaustivo, basta con dejar constancia de que se
consideraron y el motivo del descarte (costo, madurez, curva de
aprendizaje, no cumple un requisito, etc.).
-->
 
A continuación, se expondrán las alternativas consideradas y las principales razones por las cuales fueron descartadas.

Java: Presenta una curva de aprendizaje mayor debido a su tipado estático, verbosidad y la cantidad de conceptos necesarios para trabajar con frameworks empresariales como Spring Boot. Adicionalmente, su mayor consumo de memoria y tiempo de inicialización en determinadas configuraciones puede representar una desventaja para el despliegue de un MVP en servidores con recursos limitados. Aunque ofrece un ecosistema robusto para aplicaciones financieras, estas características pueden incrementar la complejidad y el tiempo de desarrollo del proyecto.

JavaScript/TypeScript con Node.js: Permite desarrollar el backend utilizando tecnologías del mismo ecosistema web que el frontend, facilitando la integración entre ambas capas. Sin embargo, el manejo de valores monetarios requiere establecer mecanismos adicionales para garantizar la precisión de los cálculos, debido al modelo numérico de JavaScript. Considerando que el proyecto requiere una gestión rigurosa de datos y lógica financiera, y que se busca mantener un alcance adecuado para el desarrollo del MVP durante el semestre, se considera una alternativa menos adecuada para el proyecto.

## Consecuencias
 
<!--
¿Qué se vuelve más fácil o más difícil después de esta decisión?
Incluye efectos positivos y negativos por igual — un ADR honesto
también documenta el costo que se está aceptando (deuda técnica
introducida, dependencia nueva, curva de aprendizaje del equipo).
-->
 Tras esta decisión, el equipo podrá desarrollar el MVP de manera más rápida, debido a la experiencia previa con Python y FastAPI. Además, el amplio ecosistema de Python facilita la integración con APIs y servicios externos, así como el desarrollo de funcionalidades relacionadas con análisis de datos, análisis financiero, generación de gráficos e inteligencia artificial. También cuenta con herramientas maduras para la interacción con diferentes motores de bases de datos y para la realización de pruebas.

Como consecuencia negativa, se acepta un rendimiento de ejecución inferior al de lenguajes compilados como Java, C# o Go, especialmente en tareas intensivas de CPU. Sin embargo, esta limitación no representa un impacto significativo para la carga esperada del MVP, cuyo procesamiento estará principalmente relacionado con operaciones de API, consultas a la base de datos y cálculos financieros de complejidad moderada.

Finalmente, aunque Python posee una amplia adopción en análisis financiero, ciencia de datos e inteligencia artificial, no es la opción predominante para determinados sistemas financieros empresariales de gran escala, donde lenguajes como Java o C# tienen una presencia más fuerte.
---
 
<!-- ### Diferencia con un RFC (referencia rápida) -->
 
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
