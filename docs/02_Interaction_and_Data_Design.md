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
| **Team** | UN-budget | Grupo 5 - Ingesoft I |
| **Members** | David Esteban Sainea Rubio, sabenitez, Kevin Florez, Miguel Angel Guativa Archila, Joger Ivan Munoz Duenas |
| **Status** | Approved |
| **Date** | 25/10/2026 October 10th, 2026 |
| **Inputs** | `docs/design/01_Architectural_and_Detailed_Design.md`, Use Cases in `docs/requirements/`, Interaction & Contracts Design v0.1 (Class 13) |

---

## 1. Behavior — Selected Use Cases

<!-- Select **two** important use cases from your own project that involve meaningful interaction between components. One of them should be the use case of your capstone requirement.-->

### 1.1 Expenses Regiter — from requirement [REQ-02]

![Sequence diagram](images/sequence_diagram_expenses.png)

*(Participants are actors, components or external systems from Deliverable 1. Show the main successful flow and at least one alternative or exception flow with `alt` / `else` or `opt`. Avoid semicolons inside message text. Activation bars (`activate` / `deactivate`) are optional: use them only if you keep them balanced.)*

| Use Case step or flow | Message(s) in the diagram | Information exchanged | Operation defined in (Deliverable 1) |
|---|---|---|---|
|**Main flow, steps 1–4:** User completes and submits expense form| `submitExpense` | `amountCOP`, `date`, `paymentMethod`, `category`, `expenseType` | Handled by `WebApp` (transaction registration capabilitie, **Section 2.2**)|
| **Main flow, step 5:** Coordinate input validation | `recordExpense` | `expense` domain entity | `RegistroGastos.RegistrarGasto(gasto)` (Section **3.2 Class Diagram(s)** - **Transaction & Movement Manager Class Diagram** and **3.4 Behavior of one key operation**)|
| **Main flow, step 6:** Persist valid expense in storage | `save` | `expense` domain entity | `Financial Repository` storage capability (Section **2.2 Components, Responsibilities & Capabilities**)|
| **Main flow, steps 7–9:** Verify category budget limit and detect overrun | `verifyCategoryLimit`, `budgetLimit(isOverrun=True, alert="Overrun detected")` | `userId`, `categoryId`, `amountCOP`; returns overrun boolean=True flag and warning message "Overrun detected"| `Balance Manager` alert on overruns capability (Section **2.2 Components, Responsibilities & Capabilities** and Section **5. Design Decisions & Decision Record** - **Decision A — Architectural**)|
| **Main flow, step 10:** Confirm registered expense with visual overrun alert | Second nested `alt` branch, final message from `Transaction & Movement Manager` to `WebApp` (`RegistrationResult(status=Success, alert=Overrun)`) | `RegistrationResult` containing `status=Success` and `alert=Overrun` payload | Implements Business Rule BR-02 / RN-02 (non-blocking registration with alert, "7. Verificar si se supera el presupuesto" Section **3.4 Behavior of one key operation**) |
| **Alternative flow:** Expense remains within budget limit (no overrun) | `budgetLimit(isOverrun=False, alert=None)`, final message from `Transaction & Movement Manager` to `WebApp` (`RegistrationResult(status=Success, alert=None)`) | Success confirmation payload with empty alert | **Alternative flow** in **REQ-02** - **4.3 Use Case section** and **4. Representations** - **4.2 Acceptance Criteria Scenario 1**|
| **Alternative flow / Edge case:** Category has no budget limit defined | `budgetLimit(isOverrun=False, alert=None)`, final message (`RegistrationResult(status=Success, alert=None)`) | Success confirmation payload without budget comparison | **Exception flow** in **REQ-02** (*Categoría sin límite presupuestario*)|
| **Exception flow 1:** Invalid expense data or missing mandatory fields | First `alt` branch (`RegistrationResult(status=Rejected, error="Invalid data")`) | Validation rejection status and field error description | `RegistroGastos` validation check (Section **3.4 Behavior of one key operation**: *Validar los datos obligatorios y el monto*)|
| **Exception flow 2:** Storage / database persistence failure | Second `alt` branch (`RegistrationResult(status=Failed, error="Storage error")`) | Storage failure status and persistence error message | Non-happy path in Section **3.4 Behavior of one key operation**: (*6. Guardar el gasto en el sistema*)|

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

Select **one** important interaction from your sequence diagrams and specify the agreement between the two components. Technology (REST, JSON, OpenAPI) is not required.

**Interaction chosen** (from diagram 1.X, message `...`):
>

| Element | Specification |
|---|---|
| **Operation and purpose** | |
| **Input** (parameters and types) | |
| **Output** (successful result and data structure) | |
| **Preconditions** (what the caller must satisfy before invoking) | |
| **Postconditions** (what is guaranteed on successful completion) | |
| **Failure outcomes** (each failure, and what state is left after it) | |
| **Invariants and side effects** (what must stay true, what may change) | |

**Testable examples** *(optional but recommended: concrete values make guarantees checkable)*

| Case | Before | Request | Expected |
|---|---|---|---|
| | | | |

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
