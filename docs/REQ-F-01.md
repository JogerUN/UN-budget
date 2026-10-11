<!--
HOW TO USE THIS TEMPLATE
------------------------
1. Copy this file and rename it to the requirement's ID, e.g. REQ-01.md.
2. Fill in every section. If a section genuinely does not apply to this
   requirement (not every requirement has a Business Rule or a Constraint),
   write "N/A — none identified" and say why in one line. Never invent
   content to fill a blank cell — that breaks the rule we've followed since
   Class 8: specification is not invention.
3. If something is unknown rather than inapplicable, use the Open
   Questions section instead of guessing.
4. See REQ-07_Example.md (Food Delivery System) for a fully filled-in
   reference before you start.
-->

# [REQ-ID] — [Short Requirement Title]

| | |
| --- | --- |
| **Status** | Draft / Validated / Open Question |
| **Team / Author(s)** | |
| **Date** | |
| **Linked User Story / AC** | |

---

## 1. Overview

### Requirement Statement

> The system shall [capability/behavior] [under what condition, if applicable].

**Type:** Functional / Non-functional
> *Classified using the Perfect Technology Filter from Class 8: imagine a
> perfect computer — infinite speed, unlimited memory, zero failures, zero
> cost. Would this requirement still matter? Yes → likely functional. The
> limitation disappears with perfect technology → likely non-functional.*

### Source / Evidence

> Where did this come from? (stakeholder, interview, workshop, existing system,
> regulation — reference your Class 8 Discovery Sheet entry if you have one)

### Need

> What is the underlying need, stated as a goal — not a solution? (e.g. "know
> when my order will arrive," not "build a GPS map")

### Value / Rationale

> Why does this requirement matter? What becomes better for the user/business if
> it's satisfied? *(This is usually the same as the "so that" of your User
> Story below — write it once and reuse it, don't rewrite it from scratch.)*

---

## 2. Context — A Requirement Rarely Stands Alone

> *Class 10. Fill honestly — "N/A — none identified" is a valid, expected
> answer for several of these.*

### Business Rule(s)

> What rule(s) exist in the business/domain, independent of software, that this
> requirement supports or enforces? Remember: Business Rule ≠ Software
> Requirement — not every rule needs one.

### Constraint(s)

> What limits how this requirement can be solved (regulation, existing
> technology, contract, interoperability, organizational policy)? A constraint
> reduces the available design space — it doesn't describe what must be
> satisfied, it describes what limits the solution.

### Assumption(s)

> What are we currently treating as true, without full verification, to keep moving? (Assumption ≠ Fact.)

### Dependenc(ies)

> What does this requirement rely on to be satisfied (another requirement, an
> external system/API, a data source, a third party, an organizational
> process)?

### Risk(s)

> What uncertain event or condition could negatively affect this requirement or
> its delivery? For each risk, note a rough Likelihood and Impact (High /
> Medium / Low) and, if you have one, a brief mitigation note.

| Risk | Likelihood | Impact | Mitigation (optional) |
| --- | --- | --- | --- |
| | | | |

### Open Questions

> Anything still unresolved — ambiguity, a question no stakeholder has answered
> yet, a missing piece of evidence. List it here instead of guessing.

---

## 3. Priority & Estimation

**Priority model used:** MoSCoW / Kano / RICE / WSJF / Value-Effort
*(Pick the one that fits the decision you're actually making — see Class 10's
comparison if you need to decide which.)*

**Priority assigned:**
> Because [the situation/signal from your project], we assigned [priority
> value], accepting the trade-off of [what you're giving up by not prioritizing
> it higher/lower]. We considered [alternative priority] and didn't use it
> because [reason].

**Estimate (confidence):** High / Medium / Low
> How sure are we about the size and shape of this work? *(This is a
> confidence tag, not a technique-based number — named estimation techniques
> like story points are Ingeniería de Software II content, not this course.)*

---

## 4. Representations — Requirement ≠ Representation

> *Class 9. Each representation reveals different information. Fill in all
> three below — for this capstone requirement, all three are required.*

### 4.1 User Story

> As a **[role]**,
> I want **[capability]**,
> so that **[value]**.
> *Check yourself: is the "I want" describing the need, or already prescribing
> a solution?*

### 4.2 Acceptance Criteria

> *At least two scenarios: one normal path, one alternative or exception.*

#### Scenario 1 — [short name]

> **Given** [context]
> **When** [event/stimulus]
> **Then** [observable outcome]

#### Scenario 2 — [short name, alternative or exception]

> **Given** [context]
> **When** [event/stimulus]
> **Then** [observable outcome]

### 4.3 Use Case

| Field | |
| --- | --- |
| **Use Case name** | |
| **Actor** | |
| **Goal** | |
| **Trigger** | |
| **Precondition** | |

#### Main Flow

1.
2.
3.
4.

#### Alternative Flow

> [Condition] → [what happens instead]

#### Exception

> [Condition] → [what happens instead]

#### Postcondition
>

#### Flow Diagram

> *Replace the labels below with your own steps. Keep Main Flow, Alternative,
> and Exception visually distinct — delete whichever branch doesn't apply to
> your use case. This renders automatically on GitHub.*

```mermaid
flowchart TD
    A([Trigger: what starts this use case]) --> B["1. Main flow step"]
    B --> C["2. Main flow step"]
    C --> D{"Decision point, if any"}
    D -- "Normal path" --> G["3. Main flow step"]
    G --> H(["Postcondition / goal reached"])
    D -- "Alternative condition" --> E["ALTERNATIVE: what happens instead"]
    E --> H
    D -- "Exception condition" --> F["EXCEPTION: what happens instead"]
    F --> H

    classDef mainflow fill:#1E2761,color:#ffffff,stroke:#1E2761;
    classDef alt fill:#F2A541,color:#1E2761,stroke:#F2A541;
    classDef exception fill:#B3261E,color:#ffffff,stroke:#B3261E;
    class B,C,G mainflow;
    class E alt;
    class F exception;
```

---

# 5. Traceability & Impact

## Backward Traceability — ¿Por qué existe este requisito?

**Evidencia:** [E-XX] — Evidencia del *Discovery Sheet* que demuestra la necesidad del usuario de planificar y controlar sus gastos mensuales.

**Necesidad:** [N-01] — El usuario necesita comenzar a organizar mis finanzas personales, por ello deseo construir mi presupuesto de ingresos y gastos personal mensualmente.

**Requisito:** El sistema debe permitir a cada usuario crear, editar y consultar un único presupuesto mensual de gastos, expresado exclusivamente en pesos colombianos (COP), asignando montos de dinero a las categorías de gastos disponibles para dicho usuario.

Este requisito existe porque los usuarios necesitan organizar sus gastos mensuales, establecer límites de gasto para diferentes categorías y contar con una referencia para administrar su dinero.

## Forward Traceability — ¿Qué elementos se verán afectados?

**Diseño futuro:**
- Una interfaz para crear y editar el presupuesto mensual.
- Un formulario para asignar montos de dinero a las categorías de gastos.
- Una vista que muestre el presupuesto y los montos asignados a cada categoría.
- Una opción de navegación para acceder al presupuesto mensual del usuario.

**Implementación:**
- Componentes y formularios del frontend para crear, editar y consultar presupuestos.
- Operaciones del backend para guardar, actualizar y consultar la información de los presupuestos.
- Estructuras en la base de datos para relacionar cada presupuesto con su usuario, mes y distribución por categorías.
- Validaciones para garantizar que los montos se manejen exclusivamente en COP y que cada usuario tenga un solo presupuesto por mes.

**Pruebas futuras:**
- Verificar que un usuario pueda crear, editar y consultar un presupuesto mensual.
- Verificar que el sistema no permita crear más de un presupuesto para el mismo mes por usuario.
- Verificar que los montos se manejen exclusivamente en COP.
- Verificar que se puedan asignar montos a las categorías de gastos disponibles.

Estos elementos son previsiones iniciales y deberán actualizarse cuando comience el diseño detallado y la implementación.

## Impact Analysis — ¿Qué más podría cambiar si este requisito se modifica?

- **Reglas de negocio:** Si cambia la restricción de un presupuesto por mes, el periodo del presupuesto o las categorías disponibles para cada usuario, podrían modificarse las reglas para crear y editar presupuestos.

- **Restricciones:** Si se cambia el requisito para permitir monedas distintas al COP o cambiar el periodo mensual se debe modificar el diseño e implementación del sistema para permitir más tipos de monedas o periodicidades.

- **Dependencias:** El presupuesto depende de las categorías de gastos disponibles por lo que el requisito puede abarcar más o menos categorías a futuro.

- **Riesgos:** Modificar la distribución de ingresos por categorías podría generar presupuestos duplicados, asignaciones inconsistentes o dificultades para comparar los gastos planeados con los gastos reales.

- **Criterios de aceptación:** Los cambios en el periodo del presupuesto, la moneda o la asignación por categorías requerirían revisar las condiciones que determinan si el requisito se ha cumplido.

- **Estimación:** Si cambia el requisito, en términos de trabajo adicional se puede requerir más tiempo de desarrollo si se amplía el requisito para permitir varios presupuestos por mes, múltiples monedas o reglas de distribución más complejas.

- **Prioridad:** Si cambia el requisito, la prioridad del mismo no cambiaría radicalmente respecto a otros requisitos, puesto que el requisito sigue siendo esencial para el proyecto, sin embargo, La prioridad de las funcionalidades del sistema que se deben desarrollar a partir de este requisito podrían cambiar.

- **Diseño futuro:** Los cambios podrían afectar los formularios del presupuesto, la interfaz de distribución por categorías, el resumen del presupuesto y la navegación, es decir, podría tener que modificarse el diseño de front y backend principalmente.

- **Pruebas futuras:** Los casos de prueba tendrían que actualizarse para cubrir las nuevas reglas, validaciones o comportamientos introducidos por los cambios.

Se considerará que lo que más probabilidades tiene de cambiar son las restricciones y las dependencias del requisito, y si eso cambia, se debería modificar los criterios de aceptación, la estimación del trabajo requerido, el diseño y las pruebas futuras.

---

## 6. Validation — Quality Gate

> *Class 9 + Class 10. Self-audit before you commit this file. Check honestly —
> a "no" here means the requirement isn't ready yet, not that you should force
> a checkmark.*

- [ ] **Valid?** Does it reflect a real, evidenced need — not an invented one?
- [ ] **Clear / Unambiguous?** Is there only one reasonable interpretation?
- [ ] **Atomic?** Is this one independently testable expectation, not several bundled together?
- [ ] **Necessary?** Does removing it actually break something real?
- [ ] **Feasible?** Can this realistically be built with what the team has?
- [ ] **Verifiable?** Can you demonstrate, concretely, whether it's satisfied?
- [ ] **Consistent?** Does it conflict with any other requirement in your set?
- [ ] **Complete enough?** Are there important functions or constraints still missing?
- [ ] **Traceable?** Can every part of this document be traced back to real evidence — not invented to fill a section?

> If any box is unchecked, say what's missing and whether it becomes an Open
> Question or sends you back to Class 8 (re-elicit) or Class 9 (re-specify).
