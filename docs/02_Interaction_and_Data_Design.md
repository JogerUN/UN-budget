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
| --- | --- |
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
| --- | --- | --- | --- |
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
| --- | --- | --- | --- |
| **Main flow, steps 1–4:** User completes and submits expense form | `submitExpense` | `amountCOP`, `date`, `paymentMethod`, `category`, `expenseType` | Handled by `WebApp` (transaction registration capabilitie, **Section 2.2**) |
| **Main flow, step 5:** Coordinate input validation | `recordExpense` | `expense` domain entity | `RegistroGastos.RegistrarGasto(gasto)` (Section **3.2 Class Diagram(s)** - **Transaction & Movement Manager Class Diagram** and **3.4 Behavior of one key operation**) |
| **Main flow, step 6:** Persist valid expense in storage | `save` | `expense` domain entity | `Financial Repository` storage capability (Section **2.2 Components, Responsibilities & Capabilities**) |
| **Main flow, steps 7–9:** Verify category budget limit and detect overrun | `verifyCategoryLimit`, `budgetLimit(isOverrun=True, alert="Overrun detected")` | `userId`, `categoryId`, `amountCOP`; returns overrun boolean=True flag and warning message "Overrun detected" | `Balance Manager` alert on overruns capability (Section **2.2 Components, Responsibilities & Capabilities** and Section **5. Design Decisions & Decision Record** - **Decision A — Architectural**) |
| **Main flow, step 10:** Confirm registered expense with visual overrun alert | Second nested `alt` branch, final message from `Transaction & Movement Manager` to `WebApp` (`RegistrationResult(status=Success, alert=Overrun)`) | `RegistrationResult` containing `status=Success` and `alert=Overrun` payload | Implements Business Rule BR-02 / RN-02 (non-blocking registration with alert, "7. Verificar si se supera el presupuesto" Section **3.4 Behavior of one key operation**) |
| **Alternative flow:** Expense remains within budget limit (no overrun) | `budgetLimit(isOverrun=False, alert=None)`, final message from `Transaction & Movement Manager` to `WebApp` (`RegistrationResult(status=Success, alert=None)`) | Success confirmation payload with empty alert | **Alternative flow** in **REQ-02** - **4.3 Use Case section** and **4. Representations** - **4.2 Acceptance Criteria Scenario 1** |
| **Alternative flow / Edge case:** Category has no budget limit defined | `budgetLimit(isOverrun=False, alert=None)`, final message (`RegistrationResult(status=Success, alert=None)`) | Success confirmation payload without budget comparison | **Exception flow** in **REQ-02** (*Categoría sin límite presupuestario*) |
| **Exception flow 1:** Invalid expense data or missing mandatory fields | First `alt` branch (`RegistrationResult(status=Rejected, error="Invalid data")`) | Validation rejection status and field error description | `RegistroGastos` validation check (Section **3.4 Behavior of one key operation**: *Validar los datos obligatorios y el monto*) |
| **Exception flow 2:** Storage / database persistence failure | Second `alt` branch (`RegistrationResult(status=Failed, error="Storage error")`) | Storage failure status and persistence error message | Non-happy path in Section **3.4 Behavior of one key operation**: (*6. Guardar el gasto en el sistema*) |

*Check each message: does it have a purpose? Is the order correct? Is every important response shown? Are the relevant failure paths covered? Does the interaction satisfy the use case?*

## 2. Data Design

### 2.1 Principal information the system needs

| Information | Needed by (use cases) | Persisted? | Why (or why not) |
| --- | --- | --- | --- |
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
| --- | --- | --- | --- |
| **USER** | End user profile and authentication data. | `id` (UUID) | `email` (Required, Unique), `password_hash` (Required), `first_name` (Required), `last_name` (Required). |
| **BUDGET** | A user's financial plan for a specific month or year. | `id` (UUID) | `user_id` (FK, Required), `currency` (Required, always 'COP'). |
| **CATEGORY** | Classification for expenses (default or custom). | `id` (UUID) | `name` (Unique Key per user), `type` (Enum: Need, Want, Saving/Debt). |
| **CATEGORY_BUDGET** | The specific monetary limit assigned to a category in a budget. | `id` (UUID) | `budget_id` (FK), `category_id` (FK), `allocated_amount` (Required, >= 0). |
| **PAYMETHOD** | Source of money (Bank account, Cash, etc.). | `id` (UUID) | `name` (Unique Key per user), `type` (Enum: Bank, Cash), `is_active` (Boolean). |
| **EXPENSE** | A record of money spent by the user. | `id` (UUID) | `amount_cop` (Required), `record_state` (Enum: Active, Deleted). |
| **INCOME** | A record of money received or expected to be received. | `id` (UUID) | `amount_cop` (Required), `record_state` (Enum: Scheduled, Received, Deleted). |

### 2.3 Data Ownership

| Information | Authoritative owner (component responsible for maintaining it) | Consumed by (uses it without owning it) | Access through |
| --- | --- | --- | --- |
| User account (credentials, profile, session) | User Management (persisted in User Repository) | Budget Management, Account & Payment Method Manager, Transaction Management, Balance Manager | User Management's authentication and profile capability |
| Monthly budget and category limits | Budget Management (persisted in Finance Repository) | Balance Manager, Transaction Management | `getBudget(userId, month, year)` |
| Expense categories and their type | Budget Management (persisted in Finance Repository) | Transaction Management | `getCategories(userId)`. Transactions only reference `categoryId` |
| Payment methods and bank accounts | Account & Payment Method Manager (persisted in Finance Repository) | Transaction Management | Account & Payment Method Manager's payment method validation capability |
| Expenses and incomes | Transaction Management (persisted in Finance Repository) | Balance Manager | Transaction Management's transaction query capability |
| Balances | Balance Manager (not persisted, recomputed on demand per ADR-0006) | Dashboard UI | Balance Manager's metrics capability |

### 2.4 Business rules and invariants enforced in data

### 2.4 Business rules and invariants enforced in data

Each rule is enforced in the component that owns the data (Section 2.3). When the rule can be written as a database constraint, the Finance or User Repository (PostgreSQL, ADR-0001) enforces it as well, as a second line of defense. Rules that depend on calculations or on how the system should behave stay in component logic only, on purpose.

| Business rule or invariant | Where it is enforced (component logic / data constraint / both) | How |
| --- | --- | --- |
| **BR-06** — All monetary amounts are in Colombian Pesos (COP). | Both | `BudgetService` always creates a `Budget` with `currency="COP"` (diagram 1.1, step 3). `BUDGET.currency` is `NOT NULL` with `CHECK (currency = 'COP')`. `EXPENSE` and `INCOME` have no currency column: the amount is stored only as `amount_cop`, so a transaction cannot be stored in another currency. |
| **BR-05** — Every category, and therefore every expense, belongs to exactly one of three types: Need, Want, Saving/Investment/Debt. | Both | `AddCategory` and `ModifyCategory` (Budget Management) reject any other type. `CATEGORY.type` is a `NOT NULL` enum (`Need`, `Want`, `Saving/Debt`). An expense gets its type through `EXPENSE.category_id` (FK, `NOT NULL`), so an expense without a type cannot exist. |
| **REQ-01 (AC-01.2)** — A user has only one budget per month. | Both | `BudgetService` first calls `getBudget(userId, month, year)`. If a budget already exists, it offers to edit it instead of creating a new one. In the database: `UNIQUE (user_id, month, year)` on `BUDGET` *(proposed: this constraint is not yet in the ER diagram)*. |
| **BR-01** — A budget must have at least one category with an allocated amount. | Component logic | `define_monthly_budget` rejects an empty `allocations` map. The class diagram models `Budget "1" *-- "1..*" CategoryBudget`. A row constraint cannot express a minimum number of child rows, so this rule cannot be a database constraint. |
| **BR-04** — The system provides default categories, and the user can add and remove their own; names do not repeat for the same user. | Both | `BudgetRegister` checks the name before `addExpenseCategory`. The UK on `CATEGORY.name` should be the composite `UNIQUE (user_id, name)`, so that two users can each have a category called "Food". |
| **REQ-02** — An expense must have amount, date, payment method, category and type. | Both | `RegistroGastos` returns `status: Rejected, error: InvalidData` when a field is missing (Contract §3). In the database: `NOT NULL` on `user_id`, `category_id`, `paymethod_id`, `amount_cop` and `date`, plus FKs to existing records. |
| The amount of an expense is greater than zero. | Both | Precondition of `recordExpense`: an amount of COP 0 is rejected (testable example in §3). In the database: `CHECK (amount_cop > 0)` on `EXPENSE`. |
| **BR-02** — An expense that exceeds its category's limit is still recorded; the system only alerts the user. | Component logic (on purpose, no data constraint) | The Balance Manager runs `verifyCategoryLimit` **after** `save` and returns `alert=Overrun` without rolling back. There is deliberately **no** constraint comparing the sum of expenses with `allocated_amount`, because such a constraint would block valid transactions. |
| A category without a budget limit does not generate an alert. | Component logic | When there is no `CATEGORY_BUDGET` row for the category in that month, the Balance Manager returns `isOverrun=False, alert=None` (REQ-02, exception flow). |
| **Need-01** — Each user only sees and changes their own financial data. | Both | `BUDGET`, `CATEGORY`, `PAYMETHOD`, `EXPENSE` and `INCOME` have `user_id` as an FK, `NOT NULL`. Every component filters by the authenticated `userId` it receives from User Management. Transaction Management checks that the referenced `categoryId` and `paymethodId` belong to the same user, using `getCategories(userId)` and the payment-method validation capability. A simple FK cannot guarantee this. |
| **REQ-11** — Financial records are never physically deleted (history is preserved). | Both | `EliminarGastos` and `EliminarIngreso` only change `record_state` to `Deleted` and never issue `DELETE`. In the database: `record_state` is a `NOT NULL` enum (`Active`/`Deleted` for `EXPENSE`; `Scheduled`/`Received`/`Deleted` for `INCOME`). The Balance Manager only counts `Active` expenses and `Received` incomes. |
| **BR-03** — An income can be recorded whether or not it has been received. | Both | `ProgramarIngreso` stores it as `Scheduled` with `expected_date`, and `RegistrarIngreso` as `Received` with `actual_date`. In the database: `expected_date` is `NOT NULL`, `actual_date` is nullable, and `CHECK (record_state <> 'Received' OR actual_date IS NOT NULL)` *(proposed)*. |
| User accounts are unique, and passwords are never stored in plain text. | Both | User Management checks the email and hashes the password before persisting. In the database: `USER.email` is `UNIQUE NOT NULL`, and only `password_hash` is stored. |
| Balances are not stored; they are always derived from transactions (ADR-0006). | Component logic | The Balance Manager recalculates them on demand from the transactions. There is no balance column, so no stored value can drift from the actual transactions. |

---

## 3. Interface Contract

**RecordExpense** (from diagram 1.1, message `recordExpense(expense)`):
>

| Element | Specification |
| --- | --- |
| **Operation and purpose** | recordExpense(expense): RegistrationResult. Registers a new expense by validating its information, saving it in the financial registry, and checking whether it exceeds the budget limit assigned to its category |
| **Input** (parameters and types) | expense: Expense, containing amountCOP: Decimal, date: Date, paymentMethod: PaymentMethod, categoryId: ID, and expenseType: ExpenseType (Necessity, Desire, or Savings/Investment/Debt) |
| **Output** (successful result and data structure) | Returns a RegistrationResult containing status: Success, error: None, and alert: Overrun if the expense exceeds the budget limit, or alert: None otherwise |
| **Preconditions** (what the caller must satisfy before invoking) | The caller must provide an Expense object containing all required fields. The amount must be greater than zero, the date must be valid, and the payment method, category, and expense type must be provided. The category must exist and be valid in the system |
| **Postconditions** (what is guaranteed on successful completion) | The expense is stored in the financial registry with its information preserved. The system checks the expense against the applicable category budget and returns the appropriate alert. An expense exceeding the budget is still registered successfully; the alert informs the user without blocking the transaction |
| **Failure outcomes** (each failure, and what state is left after it) | Invalid data: Returns status: Rejected and error: InvalidData. The expense is not stored. Persistence failure: Returns status: Failed and error: StorageError. The expense must not remain partially or inconsistently stored. In both cases, the system communicates the failure to the interface and leaves the existing financial records unchanged |
| **Invariants and side effects** (what must stay true, what may change) | Existing financial records must remain consistent, and an expense must not be duplicated or partially saved. A successful registration creates a new expense record and may trigger an overspending alert. Exceeding the budget does not invalidate the expense or prevent its registration |

**Testable examples** *(optional but recommended: concrete values make guarantees checkable)*

| Case | Before | Request | Expected |
| --- | --- | --- | --- |
| Valid expense within budget | Category budget: COP 500,000. No expense with this ID exists | Record an expense of $100,000 COP | status: Success, alert: None. The expense is stored successfully |
| Valid expense exceeding budget | Category budget: COP 500,000. Existing expenses total COP 450,000 | Record an expense of $100,000 COP | status: Success, alert: Overrun. The expense is stored, and the interface displays an overspending alert |
| Invalid expense amount | No new expense has been stored | Record an expense of $0 COP | status: Rejected, error: InvalidData. No expense is stored |
| Missing required information | No new expense has been stored | Record an expense without specifying the payment method | status: Rejected, error: InvalidData. The interface displays a validation error |
| Persistence failure | The registry is unavailable or the save operation fails | Submit a valid expense | status: Failed, error: StorageError. No partial expense record remains |

---

## 4. Cross-Consistency & Changes to Deliverable 1

| Check | Result |
| --- | --- |
| Every participant in a sequence diagram is an actor, a component, a class or an external system from Deliverable 1 | The original structure of the sequence diagram for expense registration is maintained. Its participants represent the user, the application interface, the Transaction & Movement Manager component, the Balance Manager, and the Finance Repository, whose responsibilities are defined in Deliverable 1. Adding new components was not considered necessary, since the existing structure makes it possible to represent the expense registration, storage, and budget verification flow |
| Every message corresponds to a capability, operation or contract | The messages in the sequence diagram correspond to the capabilities and operations defined in Deliverable 1. For example, submitExpense represents the submission of the form through the interface, recordExpense corresponds to the RegistroGastos.RegistrarGasto(gasto) operation, save represents the storage of the financial transaction, and verifyCategoryLimit corresponds to the Balance Manager's capability to detect budget overruns. In this way, each message has a defined purpose within the process and helps maintain traceability between the components and their responsibilities |
| Every entity or document type is reflected in the class diagrams, or the reason it is not is stated | The design retains the Gasto, Ingreso, and Categoria classes to represent financial transactions and their classification, while the Budget Manager component contains the classes related to budget and category management. The Gasto and Ingreso objects were kept separate because they have specific attributes and behaviors, such as expense classification and the distinction between the expected date and the actual date of an income. However, entities such as USER and PAYMETHOD appear in the data model without an explicit equivalent representation in the current class diagrams. Their incorporation or justification must be documented to ensure consistency between both models |
| Every persisted information element has exactly one authoritative owner | Responsibility for maintaining information is distributed according to the functions of the components. Transaction & Movement Manager manages expenses and income; Budget Manager manages budgets and categories; Account & Payment Method Manager manages accounts and payment methods; and User Management manages profiles and credentials. The repositories are responsible for persisting and retrieving information without replacing the functional responsibilities of these components. This separation helps prevent multiple components from being responsible for the same data. To fully document this decision, the Data Ownership table in Section 2.3 of Deliverable 2 must be completed |
| The contract agrees with the sequence diagram and with the data model (same behavior in all three views) | The recordExpense(expense) contract maintains the same general logic as the sequence diagram and the data model: it receives the expense information, validates the required fields, saves the transaction, and checks whether it exceeds the budget limit for its category. If an overrun occurs, the expense is successfully recorded and an alert is returned without blocking the transaction; if the data is invalid or storage fails, the corresponding result is reported. The separation between domain objects and the components responsible for executing operations is preserved. However, the explicit correspondence of the expenseType attribute with the Gasto class must be verified, and the naming conventions for components and repositories must be standardized across all three models |

---

## 5. Open Questions

> What happens to the expenses of a category the user deletes?
> Must an income be greather than zero?
> What happens to the expenses in case any payment method were delete?

---

## 6. Consistency Checklist

- [x] Two use cases from the project, each traceable to a Use Case written in the requirements.
- [x] Each sequence diagram shows the main flow and at least one alternative or exception flow.
- [x] No business behavior is invented: anything unspecified is marked as an assumption or Open Question.
- [x] Section 2.1 explains what is NOT persisted as well as what is.
- [x] The data model has identifiers, relationships and constraints, not only boxes.
- [x] Every piece of principal information has one authoritative owner, and consumers are listed (Section 2.3).
- [x] The contract defines input, output, preconditions, postconditions and failure outcomes.
- [x] Sequence, data model and contract describe the same behavior.
- [x] Diagrams render correctly on GitHub (or the exported images are embedded).
