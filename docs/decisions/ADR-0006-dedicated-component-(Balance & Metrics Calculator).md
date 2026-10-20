# ADR-0006: Centralize balance and financial metrics in an dedicated component (Balance & Metrics Calculator)
 
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
Fecha: 2026-10-19
 
## Estado
 
 Accepted
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

Under requirement **REQ-06** (*Comparative Analysis and Visualization - Dashboard*), the system must present an interactive visual dashboard comparing planned monthly budgets against actual expenses, computing deviations and category trends in real time. In addition, **REQ-04** and business rule **RN-02** require detecting and warning about budget overruns without blocking valid transaction. Finally, **REQ-11** demands accounting data integrity. 

The system architecture partitions concerns across presentation, domain logic, and persistence layers. Raw transactional entries and budgets reside in the persistence layer (`Financial & Transactional Registry`). The presentation layer (`Metrics & Dashboard Viewer`) requires aggregated, chart-ready datasets rather than raw record streams. Executing aggregations and financial calculations directly inside client-side components or allowing the UI to query the database directly would duplicate business logic across devices, degrade performance, and risk financial calculation inconsistencies.


## Decisión
 
<!--
Qué vamos a hacer, en una o dos frases claras y en tiempo presente
("Vamos a usar X para Y"). Esta es la sección más corta del documento:
un ADR no es un RFC, no necesita convencer a nadie aquí — la
justificación ya quedó en "Contexto" y las alternativas descartadas
van abajo.
-->
We establish an isolated domain logic component named **Balance & Metrics Calculator** to retrieve raw records from `Financial & Transactional Registry`, execute all balance, total, and deviation calculations, and deliver structured summary models exclusively to `Metrics & Dashboard Viewer`.

The presentation layer (`Metrics & Dashboard Viewer`) is strictly restricted to requesting processed summaries from `Balance & Metrics Calculator` and is prohibited from directly querying the persistence layer or executing transactional aggregation math.
 
## Alternativas consideradas
 
<!--
Qué otras opciones se evaluaron y por qué se descartaron. No hace
falta un análisis exhaustivo, basta con dejar constancia de que se
consideraron y el motivo del descarte (costo, madurez, curva de
aprendizaje, no cumple un requisito, etc.).
-->
1. **Client-Side Aggregation (`Metrics & Dashboard Viewer`):**
   * *Description:* The client frontend downloads raw transaction lists directly from the API and computes sums, category percentages, and budget overruns in the browser.
   * *Reason for Rejection:* Transmitting hundreds of individual transaction records over the wire increases network bandwidth and battery consumption on mobile devices, violating **REQ-09** (usability/agility) and **REQ-10** (efficient synchronization).

2. **Direct Database Views / Stored Procedures:**
   * *Description:* Aggregate balances directly through PostgreSQL views or stored procedures exposed directly to the API endpoints.
   * *Reason for Rejection:* This tightly couples presentation queries to the relational database schema, leaking persistence details and limiting unit testability of financial business logic independently of the database engine.

## Consecuencias
 
<!--
¿Qué se vuelve más fácil o más difícil después de esta decisión?
Incluye efectos positivos y negativos por igual — un ADR honesto
también documenta el costo que se está aceptando (deuda técnica
introducida, dependencia nueva, curva de aprendizaje del equipo).
-->
### Positive
* **Single Source of Truth:** All balance equations, category aggregations, and overrun criteria reside in one centralized component, ensuring consistent metrics across all client views.
* **Network & Mobile Performance:** Network payloads are minimized; the client receives only lightweight summary structures needed for rendering charts.
* **Information Hiding & Low Coupling:** The presentation layer is decoupled from PostgreSQL table structures and database entities, interacting solely through clean data contracts (DTOs). Schema migrations in `Financial & Transactional Registry` do not propagate to `Metrics & Dashboard Viewer`.
* **Testability:** Financial metric calculation and budget comparison logic can be thoroughly unit-tested without needing mock databases or UI renderers.

### Negative (Accepted Trade-offs)
* **Transformation Overhead:** Introduces intermediate processing hops, requiring explicit Data Transfer Objects (DTOs) and mapper functions to translate database entities into view-specific models.
* **Boilerplate Maintenance:** Any new metric or chart visualization requires updating both the calculation logic in `Balance & Metrics Calculator` and the corresponding transfer contracts.
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
