# REQ-01 — Gestión de Presupuesto Mensual

| | |
|---|---|
| **Status** | In Review |
| **Team / Author(s)** | Kevin Daniel Flórez Hernández, Samuel Benitez Culma |
| **Date** | 2026-10-10 |
| **Linked User Story / AC** | US-01, AC-01.1, AC-01.2 | <!-- A definir con las posteriores secciones -->

---

## 1. Overview

**Requirement Statement**
> El sistema debe permitir al usuario crear, editar y consultar un único presupuesto mensual de gastos expresado exclusivamente en Pesos Colombianos (COP), indicando la cantidad de dinero destinada para cada tipo y categoría dispuesta por el usuario.

**Type:** Functional
*(Perfect Technology Filter: incluso si la tecnología funcionara a velocidad infinita, con memoria ilimitada y costo cero, el usuario aún requeriría definir y consultar sus límites presupuestarios para organizar sus finanzas. El comportamiento de negocio no desaparece, por lo tanto es Funcional.)*

**Source / Evidence**
> Discovery Sheet, Necesidad Identificada Need-01: "El usuario necesita comenzar a organizar mis finanzas personales, por ello deseo construir mi presupuesto de ingresos y gastos personal mensualmente."

**Need**
> Establecer una planificación financiera mensual estructurada por tipos y categorías de gasto que sirva como tope de referencia para el control del dinero.

**Value / Rationale**
> Proveer al usuario una base clara de planificación que le permita comparar su gasto real frente a lo planeado, facilitando la toma de decisiones informadas y promoviendo la disciplina financiera.

---

## 2. Context — A Requirement Rarely Stands Alone

> *Class 10. Fill honestly — "N/A — none identified" is a valid, expected
> answer for several of these.*

### Business Rule(s)

> BR-01 — Para que un usuario pueda gestionar sus finanzas personales en el sistema, es obligatorio contar con un presupuesto mensual de ingresos y gastos activo.

> BR-05 — Todos los gastos categorías presupuestadas deben pertenecer, obligatoriamente, a uno de los siguientes tres tipos: Necesidad; Deseo; Ahorro, Inversión y/o Deuda.

> BR-06 — Todos los montos de dinero se manejan exclusivamente en Pesos Colombianos (COP).

### Constraint(s)

> El presupuesto mensual personal sólo puede diseñarse y planearse utilizando un único tipo de cambio: el Peso Colombiano (COP).

### Assumption(s)

> Quien diseñe su presupuesto mensual *ya cuenta* con una serie de ingresos y gastos mensuales estimados que debe planear.

### Dependenc(ies)

> Es necesaria la autenticación previa de la sesión del usuario.

### Risk(s)

| Risk | Likelihood | Impact | Mitigation (optional) |
| --- | --- | --- | --- |
|El usuario final considera tediosa la planeación de cada categoría y abandona el sistema | Medio | Alto | Ofrecer categorías básicas de gasto que pueden asignarse por defecto, sin perjuicio de que el usuario final pueda modificar o añadir nuevas |

### Open Questions

> ¿Qué debe hacer el sistema en caso de que el usuario final asigne un monto a una categoría de gasto provocando que supere el total de ingresos estimados para el mes correspondiente? ¿una alerta al usuario, un límite de asignación para la categoría o un impedir que se guarde el presupuesto? Pendiente de discusión con el equipo de trabajo.

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

## 5. Traceability & Impact

> *Class 10. Conceptual, not a formal matrix.*

**Backward — why does this requirement exist?**
> Evidence → Need → Requirement. Point to the specific evidence/need entries
> that justify this requirement (from your Discovery Sheet).

**Forward — what will this affect?**
> Requirement → future Design → Implementation → Tests. *(It's fine if Design
> hasn't happened yet — note what you expect this to touch once it does, and
> update this section once Class 11 work begins.)*

**Impact Analysis — if this requirement changes, what else might need to change?**

- [ ] Business Rules
- [ ] Constraints
- [ ] Dependencies
- [ ] Risks
- [ ] Acceptance Criteria
- [ ] Estimate
- [ ] Priority
- [ ] Future Design
- [ ] Future Tests

> Briefly note which of the above are actually likely to be affected, and why.

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
