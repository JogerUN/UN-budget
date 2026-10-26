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

### 1.1 Define Monthly Budget — from requirement [REQ-01]
---

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Frontend UI
    participant BS as BudgetService
    participant BR as BudgetRegister
    participant DB as DefineBudget
    participant B as Budget
    participant Repo as FinancialRegistryRepository

    User->>UI: Submit monthly budget allocations (COP)
    activate UI
    UI->>BS: define_monthly_budget(user_id, month, year, allocations)
    activate BS

    BS->>BR: get_categories(user_id)
    activate BR
    BR-->>BS: categories_list
    deactivate BR

    alt Invalid month (<1 or >12) or negative allocation amount
        BS-->>UI: ValueError: Invalid budget parameters
        UI-->>User: Display validation error message
    else Valid parameters
        BS->>B: create(user_id, month, year, currency="COP")
        activate B
        B-->>BS: budget_instance
        deactivate B

        BS->>DB: define_budget(budget_instance)
        activate DB
        DB-->>BS: success
        deactivate DB

        alt Action execution failed
            BS-->>UI: RuntimeError: Action failed
            UI-->>User: Display execution error
        else Action executed successfully
            BS->>Repo: save(budget_instance)
            activate Repo
            Repo-->>BS: saved_budget
            deactivate Repo

            BS-->>UI: Budget created successfully
            UI-->>User: Display monthly budget overview in COP
        end
    end

    deactivate BS
    deactivate UI
```
| Use Case Step / Flow | Message(s) in the Diagram | Information Exchanged | Operation defined in (Deliverable 1) |
|---|---|---|---|
| **Main Flow - Step 1** | `define_monthly_budget(user_id, month, year, allocations)` | User ID, month, year, category allocation map in COP | `BudgetService.define_monthly_budget` |
| **Main Flow - Step 2** | `get_categories(user_id)` | Category validation request | `BudgetRegister.get_categories` |
| **Main Flow - Step 3** | `Budget(user_id, month, year, currency="COP")` | Budget entity initialization parameters | `Budget.__init__` |
| **Main Flow - Step 4** | `define_budget(budget_instance)` | Configured Budget domain object | `DefineBudget.define_budget` |
| **Main Flow - Step 5** | `save(budget_instance)` | Validated Budget domain entity | `FinancialRegistryRepository.save` |
| **Alternative Flow (Input Validation Error)** | `ValueError: Invalid budget parameters` | Exception message raised when allocations are empty, month is not between 1-12, or amount < 0 | Input validation checks in `define_monthly_budget` |
| **Exception Path (Execution Error)** | `RuntimeError: Action execution failed` | Exception message raised when `DefineBudget.define_budget` returns false | Execution check block in `define_monthly_budget` |


### 1.2 Expenses Regiter — from requirement [REQ-02]

![Sequence diagram](images/sequence_diagram_expenses.png)

---

| Use Case Step / Flow | Message(s) in the Diagram | Information Exchanged | Operation defined in (Deliverable 1) |
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

## 2. Data Design

### 2.1 Principal information the system needs

| Information | Needed by (use cases) | Persisted? | Why (or why not) |
|---|---|---|---|
| **User Profile & Credentials** (`USER`) | Need-01, REQ-01 | Yes | To authenticate users and guarantee that each person only accesses their own financial data. |
| **Budgets & Limits** (`BUDGET`, `CATEGORY_BUDGET`) | REQ-01, REQ-06 | Yes | Required to maintain the monthly planning and compare limits against actual spending over time. |
| **Categories** (`CATEGORY`) | REQ-01, REQ-02, REQ-07 | Yes | Needed to classify transactions (RN-05) and persist custom categories created by the user (RN-04). |
| **Payment Methods** (`PAYMETHOD`) | REQ-02, REQ-05 | Yes | Essential to track the source of funds (e.g., Cash, Bank Accounts) when recording a transaction. |
| **Financial Transactions** (`EXPENSE`, `INCOME`) | REQ-02, REQ-03, REQ-04, REQ-06 | Yes | Core accounting data (REQ-11). They use soft deletion (`record_state`) instead of hard deletion to preserve historical data for the Balance Manager. |

### 2.2 Data model

Choose the representation that fits your persistence approach and **justify it in one or two sentences**:
> **Option A — Relational:** We chose a Relational representation (Entity-Relationship) to strictly enforce data integrity (REQ-11). By linking expenses, incomes, and budgets directly to a `USER`, `CATEGORY`, and `PAYMETHOD` through Foreign Keys (FK), we prevent orphaned financial records and ensure consistent metric calculations. Furthermore, a many-to-many intermediate table (`CATEGORY_BUDGET`) allows a single budget to hold multiple limits and categories to evolve independently across months.

![Entity-Relationship Data Model](./02_data_model.jpg)

| Entity / document type | Meaning in the system | Identifier | Constraints (required, unique, allowed values) |
|---|---|---|---|
| **USER** | End user profile and authentication data. | `id` (UUID) | `email` (Required, Unique), `password_hash` (Required), `first_name` (Required), `last_name` (Required). |
| **BUDGET** | A user's financial plan for a specific month or year. | `id` (UUID) | `user_id` (FK, Required), `currency` (Required, always 'COP'). |
| **CATEGORY** | Classification for expenses (default or custom). | `id` (UUID) | `name` (Unique Key per user), `type` (Enum: Need, Want, Saving/Debt). |
| **CATEGORY_BUDGET** | The specific monetary limit assigned to a category in a budget. | `id` (UUID) | `budget_id` (FK), `category_id` (FK), `allocated_amount` (Required, >= 0). |
| **PAYMETHOD** | Source of money (Bank account, Cash, etc.). | `id` (UUID) | `name` (Unique Key per user), `type` (Enum: Bank, Cash), `is_active` (Boolean). |
| **EXPENSE** | A record of money spent by the user. | `id` (UUID) | `amount_cop` (Required), `record_state` (Enum: Active, Deleted). |
| **INCOME** | A record of money received or expected to be received. | `id` (UUID) | `amount_cop` (Required), `record_state` (Enum: Scheduled, Received, Deleted). |

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
