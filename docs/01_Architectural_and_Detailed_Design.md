<!--
HOW TO USE THIS TEMPLATE
------------------------
1. Copy this file to docs/design/01_Architectural_and_Detailed_Design.md in your team repository.
2. This is v1.0 of work you already started: your Class 11 "Architectural Hypothesis v0.1"
   and your Class 12 "Detailed Design v0.1". Extend them to your whole system. Do not restart.
3. Use YOUR project. Generic examples (e-commerce, food delivery, banking, library) are
   only reference material and cannot be submitted as project artifacts.
4. Fill in every section. If something genuinely does not apply, write "N/A: reason".
   Never invent content to fill a blank.
5. Every diagram needs the table or argument that explains it. A diagram records design
   decisions. It does not create them.
6. Diagrams: Mermaid is preferred because it renders on GitHub. PlantUML or another tool is
   accepted if the exported image is committed and embedded in this file.
   Optionally, also add a JPG of each diagram in docs/design/diagrams/ (the Markdown prevails if they differ).
7. Read Design_Deliverable_1_Example.md for the expected level of detail. Do not copy it.
-->

# [Project Name] — Architectural & Detailed Design v1.0

| | |
| --- | --- |
| **Team** | |
| **Members** | |
| **Status** | Draft / Ready for review |
| **Date** | October 19th, 2026 |
| **Inputs** | `docs/requirements/`, Architectural Hypothesis v0.1 (Class 11), Detailed Design v0.1 (Class 12) |

---

## 1. System Overview & Design Drivers

### System purpose

> The system is intended to provide the end user with a digital platform where they will be able to manage their personal finances by tracking expenses against monthly personal budgets, which are divided into several categories. Moreover, the application will create reports for the user to visualize their financial health, so that they can make informed decisions based on their balance.

**Requirements that shape the structure** *(the ones that most influence the design, not all of them)*

| Requirement / Use Case ID | Why it shapes the structure | Quality attribute, constraint or business rule involved |
| --- | --- | --- |
| REQ-01 | It provides the system with the necessary capabilitities for the user to design their budgets. | BR-01: "For an individual to manage their personal finances, it is necessary to design and create a monthly personal budget." |
| REQ-02 | Tracking an expense is fundamental for the user to know their financial habits. | BR-05: "The user's expenses must be classified into one of three main types: needs, wants and savings (including debt payments or investments), regardless of the category each expense belongs to." |
| REQ-03 | Similar to the REQ-02, but regarding to the user's incomes instead of the expenses. | BR-03: "An income transaction can be recorded regardless of whether or not the end user has already received it." |

---

## 2. Architectural Design

*(Outward-facing: what are the major parts, what is each responsible for, how do they interact?)*

### 2.1 System Context & Boundary

| Outside the system | Type (actor / external system / hardware) | How the system interacts with it |
|---|---|---|
| | | |

### 2.2 Components, Responsibilities & Capabilities

Cover the principal functional scope of your whole system.

```mermaid
flowchart LR
    Actor([User or external actor])
    subgraph SYS["System name"]
        C1["Component 1"]
        C2["Component 2"]
        C3["Component 3"]
    end
    Ext[("External system")]

    Actor --> C1
    C1 -->|"capability requested"| C2
    C2 -->|"capability requested"| C3
    C3 -->|"capability requested"| Ext
```

*(Everything inside `SYS` is what you build and control. Everything outside is what you only interact with. Label each arrow with the capability being requested.)*

| Component | Main responsibility | Requirements / use cases supported | Provided capabilities | Required capabilities | Main dependencies |
|---|---|---|---|---|---|
| | | | | | |

*Checks: is every component named by responsibility, not technology ("the component that persists orders", not "the database")? Does any component exist only to make the diagram look more complex?*

---

## 3. Detailed Design

*(Inward-facing: how is each selected component designed internally?)*

### 3.1 Components selected (at least two)

| Component | Why it was selected (risk, complexity, centrality to the drivers) |
|---|---|
| | |

### 3.2 Class Diagram(s)

```mermaid
classDiagram
    class ClassA {
        -attribute : Type
        +operation(param : Type) ReturnType
    }
    class ClassB {
        -attribute : Type
        +operation() ReturnType
    }
    class ClassC {
        +operation() ReturnType
    }

    ClassA "1" *-- "0..*" ClassB : contains
    ClassA "1" --> "1" ClassC : uses
```

*(Visibility: `-` private, `+` public. Relationships: `-->` association, `*--` composition (the part cannot exist without the whole), `<|--` generalization (a specialized type of). Add multiplicity in quotes. Use composition or generalization only when their meaning is justified. Do not force them.)*

### 3.3 Class Responsibilities

| Class | Component it belongs to | Responsibility | Key collaborators |
|---|---|---|---|
| | | | |

*(Every class must belong to an identifiable component. Do not replace the component diagram with one large class diagram.)*

### 3.4 Behavior of one key operation

*(The operation you designed in Class 12, or a more important one. At most about 15 lines. Include at least one non-happy path.)*

```text

```

---

## 4. Design Quality — Cohesion, Coupling, Information Hiding

| Question | Your answer, with evidence from your design |
| --- | --- |
| **Cohesion:** do the responsibilities inside each class or component belong together? | Every component is named according to its unique global responsability. Additionally, each class within each component responds to that responsability. |
| **Coupling:** how far does a change in one element spread? Where are the strongest dependencies? | The architectural diagram shows few, if any, relationships between components within the same layer, but more relationships across layers, with communication that follows a logical flow and avoids tight coupling. |
| **Information hiding:** | It is mandatory to hide from the end user the logical flow the system will follow in order to store and retrieve data within the database and its schemas. The operations of each class must also remain hidden. The end user does not need to know how the system executes these tasks and the application could be vulnerable if the end user can gain access to this information. |

**At least one real finding and what you changed or would change:**
> The first draft of the class diagram designed by the team did not satisfy the guidelines given by the professor, since it had low cohesion. For that reason, the team redesigned it to ensure that every class in each component of the system has a single responsibility. As a result, the final diagram shows a modular structure with a considerable number of small but well-defined classes.

---

## 5. Design Decisions & Decision Record

Two decisions are required: one architectural (Class 11 level) and one detailed-design (Class 12 level). Avoid "it is best practice", "it scales" or "it is cleaner" without project evidence.

### Decision A — Architectural

| | |
| --- | --- |
| **Context** (requirement, constraint or problem that motivated it) | |
| **Decision** | |
| **Rationale** (why it is reasonable here) | |
| **Trade-off accepted** | |

### Decision B — Detailed design

| | |
| --- | --- |
| **Context** | |
| **Decision** | |
| **Rationale** | |
| **Trade-off accepted** | |

### ADR

At least one of the two decisions above must also be recorded as an ADR (use `Plantilla_ADR_Nygard`) in `docs/decisions/`.

**ADR file:** `docs/decisions/ADR-XXX-title.md` — records Decision [A / B].

---

## 6. Traceability

| Requirement ID | Use Case | Component(s) | Class(es) |
| --- | --- | --- | --- |
| REQ-01 | *Attached to the REQ-01 document in requirements folder, at the 4.3 section* | Budget Manager | |
| REQ-02 | *Attached to the REQ-02 document in requirements folder, at the 4.3 section* | Transaction & Movement Manager | RegistroGasto, ModificarGasto, EliminarGasto, Gasto, Categoria |
| REQ-03 | *Its User Case has not been defined yet* | Transaction & Movement Manager | RegistrarIngreso, ProgramarIngreso, ModificarIngreso, EliminarIngreso, Ingreso |

*(Every requirement in Section 1 must appear. Every component and class should appear at least once. If an element traces to nothing, ask why it exists.)*

---

## 7. Optional — AI-Assisted Design Reflection

> One design recommendation generated by AI that the team accepted, modified or rejected, and why.

---

## 8. Consistency Checklist

- [ ] Every component in the diagram appears in the responsibilities table, and the other way around.
- [ ] Every class belongs to an identifiable component.
- [ ] Components are named by responsibility, not technology.
- [ ] Nothing inside the system boundary is something you do not control.
- [ ] Provided and required capabilities match across components (what one requires, another provides).
- [ ] Both decisions name a real cost or limitation, and at least one has an ADR.
- [ ] The traceability table has no empty rows and no orphan components or classes.
- [ ] Diagrams render correctly on GitHub (or the exported images are embedded).
