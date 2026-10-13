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
|---|---|
| **Status** | Draft / Validated / Open Question |
| **Team / Author(s)** | |
| **Date** | |
| **Linked User Story / AC** | |

---

## 1. Overview

**Requirement Statement**
> The system shall [capability/behavior] [under what condition, if applicable].

**Type:** Functional / Non-functional
*(Classified using the Perfect Technology Filter from Class 8: imagine a perfect computer — infinite speed, unlimited memory, zero failures, zero cost. Would this requirement still matter? Yes → likely functional. The limitation disappears with perfect technology → likely non-functional.)*

**Source / Evidence**
> Where did this come from? (stakeholder, interview, workshop, existing system, regulation — reference your Class 8 Discovery Sheet entry if you have one)

**Need**
> What is the underlying need, stated as a goal — not a solution? (e.g. "know when my order will arrive," not "build a GPS map")

**Value / Rationale**
> Why does this requirement matter? What becomes better for the user/business if it's satisfied? *(This is usually the same as the "so that" of your User Story below — write it once and reuse it, don't rewrite it from scratch.)*

---

## 2. Context — A Requirement Rarely Stands Alone

**Business Rule(s)**
> BR-02: Un gasto podrá registrarse exitosamente aun cuando supere el límite presupuestado para su categoría. En estos casos, el sistema no impedirá la transacción, sino que generará una alerta visual de sobrecosto para apoyar la toma de decisiones del usuario.

> BR-04: El sistema proveerá una clasificación por defecto de categorías básicas de gasto (recomendada por expertos), pero otorgará la libertad al usuario de añadir nuevas categorías o eliminar existentes.

> BR-05: Todos los gastos categorías presupuestadas deben pertenecer, obligatoriamente, a uno de los siguientes tres tipos: Necesidad; Deseo; Ahorro, Inversión y/o Deuda.

**Constraint(s)**
> Todo ingreso de gasto nuevo deberá ser en Peso Colombiano (*BR-06*) 

**Assumption(s)**
> El usuario final hice un gasto real en peso colombiano que desea registrar, o en su defecto, hice la conversión del tipo de cambio antes del registro.

**Dependenc(ies)**
> Es necesario un presupuesto previamente diseñado y el usuario final debe estar autenticado en su sesión de usuario.

**Risk(s)**

| Risk | Likelihood | Impact | Mitigation (optional) |
|---|---|---|---|
| El usuario abandona el sistema porque registrar un gasto requiere de muchos pasos para hacerse | Medio-bajo | Alto | Diseñar el sistema de modo que el usuario registre un gasto con no más de tres clicks o toques de pantalla *(REQ-09)* |
| El usuario ingresa un gasto que sobrepasa el presupuesto realizado para la categoría y/o el presupuesto general | Alto | Medio | Continuar con el registro del gasto alertando al usuario final de los sobrecostos sobre el presupuesto planeado que el gasto implica *(BR-02)* |

**Open Questions**
> Está pendiente la discusión con el equipo sobre cómo mostrar los sobrecostos o sobregastos del usuario comparados con el presupuesto planeado, si aplica.

---

## 3. Priority & Estimation

**Priority model used:** MoSCoW / Kano / RICE / WSJF / Value-Effort *(pick the one that fits the decision you're actually making — see Class 10's comparison if you need to decide which)*

**Priority assigned:**
> Because [the situation/signal from your project], we assigned [priority value], accepting the trade-off of [what you're giving up by not prioritizing it higher/lower]. We considered [alternative priority] and didn't use it because [reason].

**Estimate (confidence):** High / Medium / Low
> How sure are we about the size and shape of this work? *(This is a confidence tag, not a technique-based number — named estimation techniques like story points are Ingeniería de Software II content, not this course.)*

---

## 4. Representations — Requirement ≠ Representation

### 4.1 User Story

Historia de usuario 1 

> Como usuario de la aplicación, quiero registrar los gastos que realizo, para mantener un seguimiento actualizado de mi dinero.

Historia de usuario 2

> Como usuario de la aplicación, quiero recibir una alerta visual cuando mis gastos superen el presupuesto asignado a una categoría, para identificar los sobrecostos y tomar decisiones sobre mis finanzas.

Historia de usuario 3 

> Como usuario de la aplicación, quiero poder registrar un gasto aunque supere el presupuesto disponible de su categoría, para llevar un control real de mis gastos sin que la aplicación me impida registrar una transacción.

### 4.2 Acceptance Criteria

#### Historia de usuario 1 

**Escenario 1: Registro de un gasto dentro del presupuesto**

> **Dado** que el usuario tiene un presupuesto mensual configurado y una categoría disponible.
> **Cuando** registra un gasto válido cuyo monto acumulado no supera el límite de esa categoría.
> **Entonces** el sistema guarda el gasto y actualiza el total acumulado de la categoría.

**Escenario 2: Registro de un gasto que supera el presupuesto**

> **Dado** que el usuario tiene un presupuesto mensual configurado y una categoría cuyo límite está establecido.
> **Cuando** registra un gasto válido que hace que el total acumulado de esa categoría supere su límite.
> **Entonces** el sistema guarda el gasto, actualiza el total acumulado y muestra una alerta visual de sobrecosto.

#### Historia de usuario 2 

**Escenario 1: Se genera una alerta**

> **Dado** que una categoría tiene un límite presupuestado definido.
> **Cuando** el registro de un gasto hace que el total acumulado supere ese límite.
> **Entonces** el sistema muestra una alerta visual que informa que se ha excedido el presupuesto de la categoría.

**Escenario 2: No se supera el límite**

> **Dado** que una categoría tiene un límite presupuestado definido.
> **Cuando** el usuario registra un gasto y el total acumulado permanece dentro del límite.
> **Entonces** el sistema guarda el gasto sin mostrar una alerta de sobrecosto.

#### Historia de usuario 3 

**Escenario 1: El gasto supera el límite**

> **Dado** que los datos del gasto cumplen con las validaciones del sistema, pero su registro supera el presupuesto de la categoría.
> **Cuando** el usuario confirma la operación.
> **Entonces** el sistema permite registrar el gasto y muestra la alerta correspondiente, sin bloquear la transacción por el exceso presupuestario.

**Escenario 2: Los datos del gasto son inválidos**

> **Dado** que el usuario intenta registrar un gasto.
> **Cuando** los datos ingresados no cumplen con las reglas de validación del sistema.
> **Entonces** el sistema informa el error y solicita corregir los datos antes de guardar el gasto.

### 4.3 Use Case

| Field |  |
|---|---|
| **Use Case name** | Registro de gastos y control de sobrecostos |
| **Actor** | Usuario de la aplicación |
| **Goal** | Registrar los gastos realizados y conocer si superan el límite de su categoría presupuestaria. |
| **Trigger** | El usuario selecciona la opción para registrar un nuevo gasto. |
| **Precondition** | El usuario ha accedido a la aplicación y dispone de una categoría a la cual asociar el gasto. Para generar una alerta de sobrecosto, la categoría debe tener un límite presupuestario definido. |

#### Main Flow

1. El usuario accede a la sección de registro de gastos.
2. El sistema muestra el formulario para ingresar la información del gasto.
3. El usuario ingresa el monto, selecciona la categoría y completa los demás datos requeridos.
4. El usuario confirma el registro.
5. El sistema valida los datos ingresados.
6. Si los datos son válidos, el sistema registra el gasto.
7. El sistema actualiza el total acumulado de la categoría correspondiente.
8. El sistema compara el total acumulado con el límite presupuestado de la categoría.
9. Si el límite ha sido superado, el sistema muestra una alerta visual de sobrecosto.
10. El sistema confirma que el gasto fue registrado correctamente.

#### Alternative Flow

> El usuario registra un gasto válido, el sistema actualiza el total acumulado de la categoría, el sistema verifica que el total no supera el límite presupuestado, el sistema confirma el registro sin mostrar una alerta de sobrecosto.

#### Exception

> **Datos inválidos:** el sistema informa los errores y solicita corregirlos antes de guardar el gasto.
> 
> **Categoría sin límite presupuestario:** el sistema permite registrar el gasto, pero no puede determinar si existe un sobrecosto respecto a un límite que no está definido.
>
> **Error al guardar:** si ocurre un problema que impide guardar el gasto, el sistema informa que el registro no se completó y evita mostrarlo como una transacción registrada exitosamente.

#### Postcondition

El gasto queda registrado y el total acumulado de su categoría se actualiza. Si el total supera el límite presupuestado, el usuario recibe una alerta visual de sobrecosto. El exceso presupuestario no impide completar una transacción válida.

#### Flow Diagram

```mermaid
flowchart TD
    A([Inicio]) --> B[Acceder al registro de gastos]
    B --> C[Ingresar monto, categoría y datos]
    C --> D[Confirmar registro]
    D --> E{¿Los datos son válidos?}

    E -- No --> F[Mostrar errores de validación]
    F --> C

    E -- Sí --> G[Registrar el gasto]
    G --> H[Actualizar total de la categoría]
    H --> I{¿La categoría tiene límite presupuestado?}

    I -- No --> J[Confirmar registro]
    I -- Sí --> K{¿El total supera el límite?}

    K -- No --> J
    K -- Sí --> L[Mostrar alerta visual de sobrecosto]
    L --> J

    J --> M([Fin])
```

---

## 5. Traceability & Impact

*(Class 10. Conceptual, not a formal matrix.)*

**Backward — why does this requirement exist?**
> Evidence → Need → Requirement. Point to the specific evidence/need entries that justify this requirement (from your Discovery Sheet).

**Forward — what will this affect?**
> Requirement → future Design → Implementation → Tests. *(It's fine if Design hasn't happened yet — note what you expect this to touch once it does, and update this section once Class 11 work begins.)*

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

*(Class 9 + Class 10. Self-audit before you commit this file. Check honestly — a "no" here means the requirement isn't ready yet, not that you should force a checkmark.)*

- [ ] **Valid?** Does it reflect a real, evidenced need — not an invented one?
- [ ] **Clear / Unambiguous?** Is there only one reasonable interpretation?
- [ ] **Atomic?** Is this one independently testable expectation, not several bundled together?
- [ ] **Necessary?** Does removing it actually break something real?
- [ ] **Feasible?** Can this realistically be built with what the team has?
- [ ] **Verifiable?** Can you demonstrate, concretely, whether it's satisfied?
- [ ] **Consistent?** Does it conflict with any other requirement in your set?
- [ ] **Complete enough?** Are there important functions or constraints still missing?
- [ ] **Traceable?** Can every part of this document be traced back to real evidence — not invented to fill a section?

> If any box is unchecked, say what's missing and whether it becomes an Open Question or sends you back to Class 8 (re-elicit) or Class 9 (re-specify).
