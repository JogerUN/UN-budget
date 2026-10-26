<!--
HOW TO USE THIS TEMPLATE
------------------------
1. Copy this file to docs/design/02_Interaction_and_Data_Design.md in your team repository.
2. This is v1.0 of work you started in Class 13 ("Interaction & Contracts Design v0.1").
   It builds on Deliverable 1 and must stay consistent with it. If making behavior and data
   concrete reveals a problem in Deliverable 1, update Deliverable 1 and say so in Section 4.
3. Use YOUR project. Generic examples are reference material only.
4. Sequence diagrams are derived from the Use Cases in your requirements. Do not invent
   business behavior. If something is not specified, mark it as an assumption or an Open Question.
5. If nothing in your system needs to persist, say so in Section 2.1 with your reasons. Do not
   invent a database.
6. Diagrams: Mermaid is preferred (renders on GitHub). PlantUML or another tool is accepted if
   the exported image is committed and embedded in this file.
   Optionally, also add a JPG of each diagram in docs/design/diagrams/ (the Markdown prevails if they differ).
7. Read Design_Deliverable_2_Example.md for the expected level of detail. Do not copy it.
-->

# [Project Name] — Interaction & Data Design v1.0

| | |
|---|---|
| **Team** | |
| **Members** | |
| **Status** | Draft / Ready for review |
| **Date** | |
| **Inputs** | `docs/design/01_Architectural_and_Detailed_Design.md`, Use Cases in `docs/requirements/`, Interaction & Contracts Design v0.1 (Class 13) |

---

## 1. Behavior — Selected Use Cases

Select **two** important use cases from your own project that involve meaningful interaction between components. One of them should be the use case of your capstone requirement.

### 1.1 [Use Case name] — from requirement [REQ-XX]

```mermaid
sequenceDiagram
    actor User
    participant A as Component A
    participant B as Component B

    User->>A: operation(param)
    A->>B: operation(param)
    alt normal condition
        B-->>A: result
        A-->>User: outcome
    else alternative or failure condition
        B-->>A: failure outcome
        A-->>User: outcome
    end
```

*(Participants are actors, components or external systems from Deliverable 1. Show the main successful flow and at least one alternative or exception flow with `alt` / `else` or `opt`. Avoid semicolons inside message text. Activation bars (`activate` / `deactivate`) are optional: use them only if you keep them balanced.)*

| Use Case step or flow | Message(s) in the diagram | Information exchanged | Operation defined in (Deliverable 1) |
|---|---|---|---|
| Main flow, step 1 | | | |
| Alternative flow | | | |
| Exception | | | |

*Check each message: does it have a purpose? Is the order correct? Is every important response shown? Are the relevant failure paths covered? Does the interaction satisfy the use case?*

### 1.2 [Second Use Case name] — from requirement [REQ-YY]

*(Same structure as 1.1.)*

---

## 2. Data Design

### 2.1 Principal information the system needs

| Information | Needed by (use cases) | Persisted? | Why (or why not) |
|---|---|---|---|
| | | Yes / No | |

*(Data owned by an external system, or recomputable on demand, is often better not persisted. If that is your decision, say so.)*

### 2.2 Data model

Choose the representation that fits your persistence approach and **justify it in one or two sentences**:
>

**Option A — Relational:** an Entity-Relationship diagram with entities, relevant attributes, primary identifiers, relationships, cardinalities and constraints.

```mermaid
erDiagram
    ENTITY_A ||--o{ ENTITY_B : "relationship"
    ENTITY_A {
        int entity_a_id PK
        string attribute
    }
    ENTITY_B {
        int entity_b_id PK
        int entity_a_id FK
        string attribute
    }
```

*(Cardinality: `||` exactly one, `o|` zero or one, `}o` zero or many, `}|` one or many.)*

**Option B — Document-oriented:** collections or document types, structure, identifiers, embedded structures, references and constraints.

```json
{
  "collection_name": {
    "id": "identifier",
    "embedded_structure": [ { "field": "value" } ],
    "reference_to_other_collection": "identifier"
  }
}
```

**Other representation:** allowed if you justify why it suits your project. The goal is not to force a relational or document database. The goal is to design the information the software needs.

| Entity / document type | Meaning in the system | Identifier | Constraints (required, unique, allowed values) |
|---|---|---|---|
| | | | |

### 2.3 Data Ownership

| Information | Authoritative owner (component responsible for maintaining it) | Consumed by (uses it without owning it) | Access through |
|---|---|---|---|
| | | | |

*(Do not assume every component needs its own database. Sharing information does not mean sharing ownership. No component reads or writes another component's data directly.)*

### 2.4 Business rules and invariants enforced in data

| Business rule or invariant | Where it is enforced (component logic / data constraint / both) | How |
|---|---|---|
| | | |

---

## 3. Interface Contract

**EecordExpense** (from diagram 1.1, message `recordExpense(expense)`):
>

| Element | Specification |
|---|---|
| **Operation and purpose** | recordExpense(expense): Permite registrar un nuevo gasto mediante la validación de sus datos, su almacenamiento en el registro financiero y la comprobación de si supera el límite presupuestario de su categoría |
| **Input** (parameters and types) | expense: Expense, un objeto que contiene los siguientes atributos: amountCOP: Decimal (monto en pesos colombianos), date: Date (fecha del gasto), paymentMethod: PaymentMethod (medio de pago), categoryId: ID (identificador de la categoría) y expenseType: ExpenseType (tipo de gasto: necesidad, deseo o ahorro/inversión/deuda) |
| **Output** (successful result and data structure) | Devuelve un objeto RegistrationResult con los campos status: Success, error: None y alert. El campo alert tendrá el valor Overrun si el gasto supera el límite presupuestario, o None si permanece dentro del límite |
| **Preconditions** (what the caller must satisfy before invoking) | La interfaz debe proporcionar un objeto Expense con todos los campos obligatorios. El monto debe ser mayor que cero, la fecha debe ser válida y deben especificarse el medio de pago, la categoría y el tipo de gasto. Además, la categoría debe existir y ser válida dentro del sistema |
| **Postconditions** (what is guaranteed on successful completion) | Si la operación finaliza exitosamente, el gasto queda almacenado en el registro financiero con su información correspondiente. El sistema comprueba el gasto frente al presupuesto aplicable y devuelve la alerta correspondiente. Si el gasto supera el límite, igualmente se registra y se informa al usuario sin bloquear la transacción |
| **Failure outcomes** (each failure, and what state is left after it) | Datos inválidos: devuelve status: Rejected y error: InvalidData. El gasto no se almacena. Fallo de persistencia: devuelve status: Failed y error: StorageError. El gasto no debe quedar almacenado parcialmente ni generar inconsistencias. En ambos casos, la interfaz informa del error y los registros financieros existentes permanecen sin cambios |
| **Invariants and side effects** (what must stay true, what may change) | Los registros financieros deben permanecer consistentes. Un gasto no debe duplicarse ni quedar guardado parcialmente. Un registro exitoso crea un nuevo gasto y puede generar una alerta de exceso presupuestario. Superar el presupuesto no invalida el gasto ni impide su registro |

**Testable examples** *(optional but recommended: concrete values make guarantees checkable)*

| Case | Before | Request | Expected |
|---|---|---|---|
| Gasto dentro del presupuesto | Presupuesto de la categoría: $500.000 COP | Registrar un gasto de $100.000 COP |	status: Success, alert: None, El gasto queda registrado | 
| Gasto que supera el presupuesto | Presupuesto: $500.000 COP. Gastos acumulados: $450.000 COP | Registrar un gasto de $100.000 COP | status: Success, alert: Overrun, El gasto queda registrado y se muestra una alerta |
| Monto inválido | No existe un nuevo gasto registrado |	Registrar un gasto de $0 COP | status: Rejected, error: InvalidData, El gasto no se registra |
| Información obligatoria faltante | No existe un nuevo gasto registrado |	Registrar un gasto sin especificar el medio de pago |	status: Rejected, error: InvalidData, La interfaz muestra un error de validación |
| Fallo de almacenamiento | El registro financiero no está disponible o falla la operación de guardado |	Enviar una solicitud con datos válidos |	status: Failed, error: StorageError, No queda ningún registro parcial del gasto |
---

## 4. Cross-Consistency & Changes to Deliverable 1

| Check | Result |
|---|---|
| Every participant in a sequence diagram is an actor, a component, a class or an external system from Deliverable 1 | |
| Every message corresponds to a capability, operation or contract | |
| Every entity or document type is reflected in the class diagrams, or the reason it is not is stated | |
| Every persisted information element has exactly one authoritative owner | |
| The contract agrees with the sequence diagram and with the data model (same behavior in all three views) | |

**Changes made to Deliverable 1 because of this deliverable** *(real designs change when behavior and data become concrete. List what you updated, or write "None" and why.)*
>

---

## 5. Open Questions

> Anything unresolved about behavior or data. List it here instead of guessing.

---

## 6. Optional — AI-Assisted Design Reflection

> One design recommendation generated by AI that the team accepted, modified or rejected, and why.

---

## 7. Consistency Checklist

- [ ] Two use cases from the project, each traceable to a Use Case written in the requirements.
- [ ] Each sequence diagram shows the main flow and at least one alternative or exception flow.
- [ ] No business behavior is invented: anything unspecified is marked as an assumption or Open Question.
- [ ] Section 2.1 explains what is NOT persisted as well as what is.
- [ ] The data model has identifiers, relationships and constraints, not only boxes.
- [ ] Every piece of principal information has one authoritative owner, and consumers are listed (Section 2.3).
- [ ] The contract defines input, output, preconditions, postconditions and failure outcomes.
- [ ] Sequence, data model and contract describe the same behavior.
- [ ] Diagrams render correctly on GitHub (or the exported images are embedded).
